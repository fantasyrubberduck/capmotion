# Makefile per Motion Capture

# Variables
DOCKER_COMPOSE = docker compose
SERVICE = motion-capture

# Construir imatges
build:
	$(DOCKER_COMPOSE) build

# Arrencar serveis
up:
	$(DOCKER_COMPOSE) up -d

# Arrencada en primer pla (foreground)
up-fg:
    $(DOCKER_COMPOSE) up

# Aturar serveis
down:
	$(DOCKER_COMPOSE) down

# Reiniciar ràpidament
restart: down up

# Veure logs (stderr inclòs)
logs:
	$(DOCKER_COMPOSE) logs -f $(SERVICE)

# Estat dels serveis
ps:
    $(DOCKER_COMPOSE) ps
	
# Executar tests amb cobertura
test:
	pytest -v --cov=$(SERVICE) --cov-report=xml --cov-report=term-missing tests/

# Logs en temps real
logs:
    $(DOCKER_COMPOSE) logs -f

# Netejar tot
clean:
    $(DOCKER_COMPOSE) down -v --remove-orphans
    docker system prune -f
	rm -rf output/*.mp4 coverage.xml
