"""Render the two README charts as static SVG from eval/results/*.jsonl (no plotting deps)."""
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, BG = "#1f1f1e", "#5f5e58", "#e6e5df", "#ffffff"
FONT = 'font-family="Inter, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"'


def load(tag=""):
    rows = [json.loads(l) for l in (ROOT / f"eval/results/answers{tag}.jsonl").open()]
    out = {}
    for s in {r["system"] for r in rows}:
        rs = [r for r in rows if r["system"] == s]
        out[s] = {"acc": st.mean(r["correct"] for r in rs), "cost": st.mean(r.get("cost_usd") or 0 for r in rs),
                  "tok": st.median(r.get("input_tokens") or 0 for r in rs)}
    return out


def family(s):
    return BLUE if s.startswith("agent") else ORANGE if s.startswith("full") else AQUA


def scatter(d, path):
    """Two aligned bar panels (accuracy | cost per question), one row per system: no dual axis, no label clashes."""
    systems = ["full-context", "agent+search", "agentic-grep", "rag:hybrid+rerank", "rag:hybrid", "rag:dense"]
    W, T, rowh, bh = 760, 92, 30, 16
    H = T + rowh * len(systems) + 30
    L1, W1 = 160, 300        # accuracy panel
    L2, W2 = 520, 200        # cost panel
    A = lambda v: L1 + v * W1  # noqa: E731
    C = lambda v: L2 + v / 0.05 * W2  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="20" y="24" font-size="15" font-weight="600" fill="{INK}">Correct answers and cost per question</text>',
         f'<text x="20" y="42" font-size="12" fill="{INK2}">119 questions, 333-note notebook, answering model Claude Sonnet 5.5; cost at API list prices with prompt caching</text>',
         f'<text x="{L1}" y="{T-14}" font-size="12" font-weight="600" fill="{INK}">correct</text>',
         f'<text x="{L2}" y="{T-14}" font-size="12" font-weight="600" fill="{INK}">USD per question</text>']
    for v in [0, 0.25, 0.5, 0.75, 1.0]:
        o.append(f'<line x1="{A(v):.1f}" x2="{A(v):.1f}" y1="{T-6}" y2="{H-26}" stroke="{GRID}"/>'
                 f'<text x="{A(v):.1f}" y="{H-10}" font-size="11" fill="{INK2}" text-anchor="middle">{v:.0%}</text>')
    for v in [0, 0.025, 0.05]:
        o.append(f'<line x1="{C(v):.1f}" x2="{C(v):.1f}" y1="{T-6}" y2="{H-26}" stroke="{GRID}"/>'
                 f'<text x="{C(v):.1f}" y="{H-10}" font-size="11" fill="{INK2}" text-anchor="middle">${v:.3f}</text>')
    for i, s in enumerate(systems):
        p = d[s]
        y = T + i * rowh
        c = family(s)
        o.append(f'<text x="{L1-10}" y="{y+12}" font-size="12" fill="{INK}" text-anchor="end">{s}</text>')
        o.append(f'<rect x="{L1}" y="{y}" width="{A(p["acc"])-L1:.1f}" height="{bh}" rx="3" fill="{c}"><title>{s}: {p["acc"]:.1%} correct</title></rect>'
                 f'<text x="{A(p["acc"])+6:.1f}" y="{y+12}" font-size="11" fill="{INK2}">{p["acc"]:.0%}</text>')
        o.append(f'<rect x="{L2}" y="{y}" width="{C(p["cost"])-L2:.1f}" height="{bh}" rx="3" fill="{c}"><title>{s}: ${p["cost"]:.3f} per question</title></rect>'
                 f'<text x="{C(p["cost"])+6:.1f}" y="{y+12}" font-size="11" fill="{INK2}">${p["cost"]:.3f}</text>')
    for i, (c, name) in enumerate([(BLUE, "agent with tools"), (ORANGE, "whole notebook in prompt"), (AQUA, "one-shot RAG")]):
        x = 20 + i * 180
        o.append(f'<rect x="{x}" y="54" width="10" height="10" rx="2" fill="{c}"/>'
                 f'<text x="{x+15}" y="63" font-size="12" fill="{INK}">{name}</text>')
    o.append("</svg>")
    path.write_text("\n".join(o))


def tokens(d1, dx, path):
    systems = ["full-context", "agentic-grep", "agent+search", "rag:hybrid+rerank"]
    W, H, L, R, T = 720, 270, 150, 40, 70
    bh, gap = 14, 2
    mx = 300_000
    X = lambda v: L + v / mx * (W - L - R)  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="20" y="24" font-size="15" font-weight="600" fill="{INK}">Input tokens per question as the notebook grows</text>',
         f'<text x="20" y="42" font-size="12" fill="{INK2}">median; 333 notes (~39k words) vs 1,138 notes (~103k words)</text>']
    for v in [0, 100_000, 200_000, 300_000]:
        o.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{T-8}" y2="{H-40}" stroke="{GRID}"/>')
        o.append(f'<text x="{X(v):.1f}" y="{H-24}" font-size="11" fill="{INK2}" text-anchor="middle">{v//1000}k</text>')
    for i, s in enumerate(systems):
        y = T + i * 48
        o.append(f'<text x="{L-10}" y="{y+bh+5}" font-size="12" fill="{INK}" text-anchor="end">{s}</text>')
        for j, (d, c, lab) in enumerate([(d1, BLUE, "333 notes"), (dx, ORANGE, "1,138 notes")]):
            v = d[s]["tok"]
            yy = y + j * (bh + gap)
            w = max(X(v) - L, 2)
            o.append(f'<rect x="{L}" y="{yy}" width="{w:.1f}" height="{bh}" rx="3" fill="{c}"><title>{s}, {lab}: {v:,.0f} tokens</title></rect>')
            o.append(f'<text x="{L+w+6:.1f}" y="{yy+11}" font-size="11" fill="{INK2}">{v/1000:.0f}k</text>')
    for i, (c, name) in enumerate([(BLUE, "333 notes"), (ORANGE, "1,138 notes")]):
        o.append(f'<rect x="{W-R-200+i*100}" y="50" width="10" height="10" rx="2" fill="{c}"/>'
                 f'<text x="{W-R-185+i*100}" y="59" font-size="12" fill="{INK}">{name}</text>')
    o.append("</svg>")
    path.write_text("\n".join(o))


if __name__ == "__main__":
    d1, dx = load(), load("-xl")
    scatter(d1, ROOT / "docs/accuracy-cost.svg")
    tokens(d1, dx, ROOT / "docs/tokens-scale.svg")
    print("ok")
