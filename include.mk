.PHONY: run-demo
run-demo:
	@$(VENV_EXECUTABLE_FOLDER)/gunicorn yafowil.demo:app -t 3600 -b 127.0.0.1:8000
