.PHONY: activate
activate:
	source ../venv/bin/activate

.PHONY: start-api-dev
start-api-dev:
	HCJWTENABLE=1 uvicorn  humancoin_api:app --host '0.0.0.0' --port 4033 --reload

.PHONY: start-api-test
start-api-test:
	HCJWTENABLE=1 nohup uvicorn humancoin_api:app --host '0.0.0.0' --port 4033 --workers 2 >> api_test.log 2>&1 &

.PHONY: start-api-pro
start-api-pro:
	HCJWTENABLE=1 nohup uvicorn humancoin_api:app --host '0.0.0.0' --port 4033 --workers 4 --limit-concurrency 1000 --backlog 4096 >> api_pro.log  2>&1 &


.PHONY: start-points-dev
start-points-dev:
	python3 -u humancoin_points.py --env test

.PHONY: start-points-test
start-points-test:
	nohup python3 -u humancoin_points.py --env test >> points_test.log 2>&1 &

.PHONY: start-points-pro
start-points-pro:
	nohup python3 -u humancoin_points.py --env pro >> points_pro.log 2>&1 &


.PHONY: start-bot-dev
start-bot-dev:
	python3 -u humancoin_bot.py

.PHONY: start-bot-test
start-bot-test:
	nohup python3 -u humancoin_bot.py >> bot_test.log 2>&1 &

.PHONY: start-bot-pro
start-bot-pro:
	nohup python3 -u humancoin_bot.py >> bot_pro.log 2>&1 &



.PHONY: stop-api
stop-api:
	ps aux | grep python3 | grep humancoin_api | awk '{print $2}' | xargs kill

.PHONY: stop-bot
stop-bot:
	ps aux | grep python3 | grep humancoin_bot | awk '{print $2}' | xargs kill

.PHONY: stop-points
stop-points:
	ps aux | grep python3 | grep humancoin_points | awk '{print $2}' | xargs kill

.PHONY: stop-all
stop-all:
	ps aux | grep python3 | grep humancoin_ | awk '{print $2}' | xargs kill
