.PHONY: build_start_local down_local

# Docker build and start the local docker stack
build_start_local:
	docker compose -f docker-compose.yml build --no-cache && docker compose -f docker-compose.yml up --force-recreate  $(c)
# Stop the local docker stack
down_local:
	docker compose -f docker-compose.yml down $(c)

