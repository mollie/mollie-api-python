.venv:
	uv venv --python 3.12
	uv pip install black

fix-codestyle: .venv
	.venv/bin/black mollie

clean:
	rm -rf .venv
