DC = docker compose
APP = docker_compose.yaml
APP_SERVICE = app
ENV = --env-file .env

.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${DC} -f ${APP} logs -f

.PHONY: app-test
app-test:
	${DC} -f ${APP} exec ${APP_SERVICE} pytest

.PHONY: app-down
app-down:
	${DC} -f ${APP} down
