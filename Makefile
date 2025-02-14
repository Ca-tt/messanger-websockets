serverr:
	pipenv run uvicorn server.main:app --reload

guiapp:
	py gui/main.py

black:
	black src/

production:
	uvicorn server.main:app --host 0.0.0.0 --port 8000