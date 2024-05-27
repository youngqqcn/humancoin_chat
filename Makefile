
api-test:
	uvicorn api:app --host '0.0.0.0' --port 8000 --reload

api-pro:
	uvicorn api:app --host '0.0.0.0' --port 8000

points-test:
	python3 points.py --env test

points-pro:
	python3 points.py --env pro