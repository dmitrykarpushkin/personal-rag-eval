"""End-to-end answer eval: same question, same answering model, different ways of finding the context.

Systems
  rag:<retriever>  top-8 chunks from a retriever (with path + date headers) -> model, no tools
  agentic-grep     the model gets Grep/Glob/Read over the notebook folder and searches by itself
                   (how a coding agent "searches notes" today)
  full-context     the whole notebook pasted into the prompt (~60k tokens)

Scoring is mechanical (no LLM judge):
  answerable   -> correct if every answer regex matches the answer text
  unanswerable -> correct if the model says NOT_FOUND
  citation     -> at least one cited path is a gold note
The answering model runs through the `claude` CLI (`claude -p`), so this needs a logged-in Claude Code.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(os.environ.get("PRAG_CORPUS", ROOT / "corpus")).resolve()
TAG = os.environ.get("PRAG_TAG", "")  # results suffix, e.g. "-xl"
sys.path.insert(0, str(ROOT / "src"))
from prag import retrieve, store  # noqa: E402
from run_retrieval import load_gold  # noqa: E402

MODEL = "claude-sonnet-5-5"
MODELS = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-5-5"}  # "<system>@haiku" picks a model
TOP_CHUNKS = 8
TODAY = "2026-09-30"
FULL_SYSTEM_FILE = str(ROOT / f"eval/results/.full_context_system{TAG}.txt")

INSTRUCTIONS = f"""You are a personal assistant answering a question about your user's own notes (the user is Mara).
Today is {TODAY}. Notes can be outdated: when notes disagree, trust the most recent one.
Answer only from the notes. If the notes do not contain the answer, answer exactly NOT_FOUND.
Reply with one JSON object and nothing else:
{{"answer": "<short answer with the key facts, in English; in Russian only if the question is in Russian>", "sources": ["<note path>", ...]}}"""


def claude(prompt: str, system: str, tools: str = "", cwd: str = "/tmp", max_turns: int | None = None,
           system_file: str | None = None, model: str = MODEL) -> dict:
    cmd = ["claude", "-p", "--model", model, "--tools", tools, "--strict-mcp-config", "--setting-sources", "",
           "--no-session-persistence", "--output-format", "json"]
    cmd += ["--system-prompt-file", system_file] if system_file else ["--system-prompt", system]
    if max_turns:
        cmd += ["--max-turns", str(max_turns)]
    if tools:
        cmd += ["--allowedTools", tools]
    t = time.perf_counter()
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd, timeout=600)
    wall = time.perf_counter() - t
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"result": "", "error": (p.stderr or p.stdout)[-500:], "wall_s": wall}
    u = d.get("usage") or {}
    return {"result": d.get("result") or "", "wall_s": wall, "cost_usd": d.get("total_cost_usd"),
            "turns": d.get("num_turns"),
            "input_tokens": (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
            + (u.get("cache_creation_input_tokens") or 0),
            "cached_tokens": u.get("cache_read_input_tokens") or 0,
            "output_tokens": u.get("output_tokens")}


def parse(text: str) -> tuple[str, list[str]]:
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            return str(d.get("answer", "")), [str(s) for s in d.get("sources") or []]
        except json.JSONDecodeError:
            pass
    return text.strip(), []


def context_block(hits: list[dict]) -> str:
    return "\n\n".join(f"### {h['path']} (date: {h['created']}; {h['title']})\n{h['body']}" for h in hits)


def full_corpus() -> str:
    parts = []
    for p in sorted((CORPUS).rglob("*.md")):
        parts.append(f"### {p.relative_to(CORPUS)}\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def score(q: dict, answer: str, sources: list[str]) -> dict:
    abstained = "NOT_FOUND" in answer
    if q["answerable"]:
        correct = (not abstained) and all(re.search(p, answer, re.I) for p in q["answer_patterns"])
    else:
        correct = abstained
    norm = [s.removeprefix("corpus/").lstrip("./") for s in sources]
    cited_gold = any(s in q["gold_notes"] for s in norm) if q["answerable"] else None
    return {"correct": correct, "abstained": abstained, "cited_gold": cited_gold}


def prepare(system: str, q: dict, conn, corpus_text: str) -> dict:
    """Build the model call for one (system, question). Retrieval happens here, serially."""
    system = system.split("@")[0]
    question = q["question"]
    if system.startswith("rag:"):
        hits, secs = retrieve.run(system[4:], conn, CORPUS, question, TOP_CHUNKS)
        return {"prompt": f"Notes:\n\n{context_block(hits[:TOP_CHUNKS])}\n\nQuestion: {question}",
                "retrieval_s": round(secs, 2), "retrieved": retrieve.notes_ranked(hits[:TOP_CHUNKS])}
    if system == "agentic-grep":
        return {"prompt": f"The notes are markdown files in the current folder. Search them with your tools.\n\n"
                          f"Question: {question}", "tools": "Grep,Glob,Read", "cwd": str(CORPUS),
                "max_turns": 20}
    if system == "full-context":
        # The notebook goes into the system prompt so prompt caching kicks in after the first question.
        # Instructions are repeated after the notes: smaller models lose the output format 100k tokens back.
        return {"prompt": f"{INSTRUCTIONS}\n\nQuestion: {question}", "system_file": FULL_SYSTEM_FILE}
    raise ValueError(system)


def ask(system: str, q: dict, prep: dict) -> dict:
    r = claude(prep["prompt"], INSTRUCTIONS, tools=prep.get("tools", ""), cwd=prep.get("cwd", "/tmp"),
               max_turns=prep.get("max_turns"), system_file=prep.get("system_file"),
               model=MODELS[system.split("@")[1]] if "@" in system else MODEL)
    answer, sources = parse(r.get("result", ""))
    extra = {k: prep[k] for k in ("retrieval_s", "retrieved") if k in prep}
    return {"id": q["id"], "category": q["category"], "system": system, "question": q["question"], "answer": answer,
            "sources": sources, **extra, **{k: v for k, v in r.items() if k != "result"},
            **score(q, answer, sources)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", default="rag:hybrid+rerank,rag:hybrid,agentic-grep,full-context")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=f"answers{TAG}.jsonl")
    a = ap.parse_args()
    qs = load_gold()[: a.limit or None]
    corpus_text = full_corpus()
    Path(FULL_SYSTEM_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(FULL_SYSTEM_FILE).write_text(INSTRUCTIONS + "\n\nNotes:\n\n" + corpus_text)
    out = ROOT / "eval/results" / a.out
    done = set()
    if out.exists():
        done = {(r["id"], r["system"]) for r in map(json.loads, out.open())}
    conn = store.connect()
    jobs = [(s, q) for s in a.systems.split(",") for q in qs if (q["id"], s) not in done]
    print(f"{len(jobs)} runs; retrieving...", flush=True)
    preps = [prepare(s, q, conn, corpus_text) for s, q in jobs]
    with open(out, "a") as fh, ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(lambda jp: ask(jp[0][0], jp[0][1], jp[1]), zip(jobs, preps)):
            fh.write(json.dumps(r, ensure_ascii=False) + "\n"); fh.flush()
            print(r["system"], r["id"], r["correct"], r.get("error", ""), flush=True)


if __name__ == "__main__":
    main()
