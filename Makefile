export PYTHONPATH := src

up:            ## start Postgres + pgvector
	docker compose up -d --wait

index:         ## chunk, embed and index corpus/
	python -m prag.cli index corpus --reset

goldset:       ## rebuild eval/goldset.jsonl from spec/world.yaml and check it against corpus/
	python eval/build_goldset.py

eval-retrieval:
	python eval/run_retrieval.py

eval-answers:  ## needs a logged-in `claude` CLI
	python eval/run_answers.py

report:
	python eval/report.py
