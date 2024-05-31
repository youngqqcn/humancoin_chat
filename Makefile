check-venv:
	@if [ -z "$$VIRTUAL_ENV_PROMPT" ]; then \
		echo "venv is not activated" ; \
		exit 1; \
	fi

start-api-dev: check-venv
	HCJWTENABLE=1 uvicorn  humancoin_api:app --host '0.0.0.0' --port 4033 --reload

start-api-test: check-venv
	HCJWTENABLE=1 nohup uvicorn humancoin_api:app --host '0.0.0.0' --port 4033 --workers 2 >> api_test.log 2>&1 &

start-api-pro: check-venv
	HCJWTENABLE=1 nohup uvicorn humancoin_api:app --host '0.0.0.0' --port 4033 --workers 4 --limit-concurrency 1000 --backlog 4096 >> api_pro.log  2>&1 &

start-points-dev: check-venv
	python3 -u humancoin_points.py --env test

start-points-test: check-venv
	nohup python3 -u humancoin_points.py --env test >> points_test.log 2>&1 &

start-points-pro: check-venv
	nohup python3 -u humancoin_points.py --env pro >> points_pro.log 2>&1 &


start-bot-dev: check-venv
	python3 -u humancoin_bot.py

start-bot-test: check-venv
	nohup python3 -u humancoin_bot.py >> bot_test.log 2>&1 &

start-bot-pro: check-venv
	nohup python3 -u humancoin_bot.py >> bot_pro.log 2>&1 &



.PHONY: stop-api
stop-api:
	@ps aux | grep python3 | grep humancoin_api | awk '{print $$2}' | xargs kill

.PHONY: stop-bot
stop-bot:
	@ps aux | grep python3 | grep humancoin_bot | awk '{print $$2}' | xargs kill

.PHONY: stop-points
stop-points:
	@ps aux | grep python3 | grep humancoin_points | awk '{print $$2}' | xargs kill

.PHONY: stop-all
stop-all:
	@ps aux | grep python3 | grep humancoin_ | awk '{print $$2}' | xargs kill
