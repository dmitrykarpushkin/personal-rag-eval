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

corpus-xl:     ## main notebook + 2024-2025 archive, for the scaling run
	rm -rf corpus-xl && mkdir corpus-xl && cp -r corpus/. corpus-xl/ && cp -rn archive/. corpus-xl/
