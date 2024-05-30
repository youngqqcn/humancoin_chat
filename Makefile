
start-api-dev:
	HCJWTENABLE=1 uvicorn  humancoin_api:app --host '0.0.0.0' --port 4033 --reload

start-api-test:
	HCJWTENABLE=1 nohup uvicorn humancoin_api:app --host '0.0.0.0' --port 4033 --workers 2 >> api_test.log 2>&1 &

start-api-pro:
	HCJWTENABLE=1 nohup uvicorn humancoin_api:app --host '0.0.0.0' --port 4033 --workers 4 --limit-concurrency 1000 --backlog 4096 >> api_pro.log  2>&1 &


start-points-dev:
	python3 -u humancoin_points.py --env test

start-points-test:
	nohup python3 -u humancoin_points.py --env test >> points_test.log 2>&1 &

start-points-pro:
	nohup python3 -u humancoin_points.py --env pro >> points_pro.log 2>&1 &


start-bot-dev:
	python3 -u humancoin_bot.py

start-bot-test:
	nohup python3 -u humancoin_bot.py >> bot_test.log 2>&1 &

start-bot-pro:
	nohup python3 -u humancoin_bot.py >> bot_pro.log 2>&1 &



stop-api:
	ps aux | grep python3 | grep humancoin_api | awk '{print $2}' | xargs kill

stop-bot:
	ps aux | grep python3 | grep humancoin_bot | awk '{print $2}' | xargs kill

stop-points:
	ps aux | grep python3 | grep humancoin_points | awk '{print $2}' | xargs kill

stop-all:
	ps aux | grep python3 | grep humancoin_ | awk '{print $2}' | xargs kill
