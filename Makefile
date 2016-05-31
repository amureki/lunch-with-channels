requirements:
	pip-compile --upgrade --rebuild --no-annotate --no-header requirements.in > /dev/null
	pip-compile --upgrade --rebuild --no-annotate --no-header requirements_test.in > /dev/null


clean:
	find . -type f -name "*.py[cod]" -delete
	find . -type d -name "__pycache__" -delete

tests: clean
	py.test
