serverr:
	pipenv run uvicorn server.main:app --reload

guiapp:
	py gui/main.py

black:
	black src/