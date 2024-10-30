test:
	PYTHONPATH=src python -m coverage run -m unittest discover
	PYTHONPATH=src python -m coverage report -m
