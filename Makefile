env_setup:
	cp .env.example .env
build:
	@docker-compose -f ${PWD}/docker-compose.yml build
up:
	@docker-compose -f ${PWD}/docker-compose.yml up -d
restart:
	@docker-compose -f ${PWD}/docker-compose.yml restart
down:
	@docker-compose -f ${PWD}/docker-compose.yml down
remove_all_containers:
	@docker rm -f $$(docker ps -a -q)
remove_all_images:
	@docker rmi -f $$(docker images -a -q)
remove_all_volumes:
	@docker volume rm $$(docker volume ls -q)
remove_everything:
	make remove_all_containers && make remove_all_images && make remove_all_volumes
run_tests:
	@docker compose run --rm api_server pytest
coverage:
	@docker compose run --rm api_server pytest --cov
coverage_html_report:
	@docker compose run --rm api_server coverage html