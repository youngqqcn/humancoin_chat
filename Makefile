
api-dev:
	uvicorn api:app --host '0.0.0.0' --port 4033 --reload

api-test:
	nohup uvicorn api:app --host '0.0.0.0' --port 4033 >> api_test.log 2>&1 &

api-pro:
	nohup uvicorn api:app --host '0.0.0.0' --port 4033 >> api_pro.log  2>&1 &


points-dev:
	python3 points.py --env test

points-test:
	nohup python3 points.py --env test >> points_test.log 2>&1 &

points-pro:
	nohup python3 points.py --env pro >> points_pro.log 2>&1 &


bot-dev:
	python3 bot.py

bot-test:
	nohup python3 bot.py >> bot_test.log 2>&1 &

bot-pro:
	nohup python3 bot.py >> bot_pro.log 2>&1 &

