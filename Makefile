
api-dev:
	uvicorn  api:app --host '0.0.0.0' --port 4033 --reload

api-test:
	nohup uvicorn api:app --host '0.0.0.0' --port 4033 --workers 2 >> api_test.log 2>&1 &

api-pro:
	nohup uvicorn api:app --host '0.0.0.0' --port 4033 --workers 4 --limit-concurrency 1000 --backlog 4096 >> api_pro.log  2>&1 &


points-dev:
	python3 -u points.py --env test

points-test:
	nohup python3 -u points.py --env test >> points_test.log 2>&1 &

points-pro:
	nohup python3 -u points.py --env pro >> points_pro.log 2>&1 &


bot-dev:
	python3 -u bot.py

bot-test:
	nohup python3 -u bot.py >> bot_test.log 2>&1 &

bot-pro:
	nohup python3 -u bot.py >> bot_pro.log 2>&1 &

