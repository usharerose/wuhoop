.PHONY: run clean-containers

run: clean-containers
	docker compose up --build -d

clean-containers:
	docker compose down --remove-orphans
