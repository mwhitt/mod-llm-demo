train_setup:
	python -m venv .venv
	. .venv/bin/activate

generate_data:
	generate_allowed_data
	generate_disallowed

generate_allowed:
	uv run python main.py generate-allowed

generate_disallowed:
	uv run python main.py generate-disallowed

setup:
	uv venv && uv sync

serve:
	export VLLM_CPU_KVCACHE_SPACE=20; uv run vllm serve "mwhitt/mod-llm-demo"

eval:
	uv run python main.py run-eval
