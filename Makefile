# Nom del projecte
PROJECT_NAME=motion-capture

# Compose
COMPOSE=docker compose

# Build general
build:
    $(COMPOSE) build

# Arrencada en segon pla (detached)
up:
    $(COMPOSE) up -d

# Arrencada en primer pla (foreground)
up-fg:
    $(COMPOSE) up

# Aturar serveis
down:
    $(COMPOSE) down

# Logs en temps real
logs:
    $(COMPOSE) logs -f

# Reiniciar ràpidament
restart: down up

# Estat dels serveis
ps:
    $(COMPOSE) ps

# Neteja completa
clean:
    $(COMPOSE) down -v --remove-orphans
    docker system prune -f

# --- Objectius per càmera ---

# Webcam en segon pla
webcam:
    $(COMPOSE) up -d webcam

# Webcam en primer pla
webcam-fg:
    $(COMPOSE) up webcam

# IP cam en segon pla
ipcam:
    $(COMPOSE) up -d ipcam

# IP cam en primer pla
ipcam-fg:
    $(COMPOSE) up ipcam

# Aturar només webcam
webcam-down:
    $(COMPOSE) stop webcam

# Aturar només ipcam
ipcam-down:
    $(COMPOSE) stop ipcam
