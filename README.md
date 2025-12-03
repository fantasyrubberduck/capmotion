# 🎥 Motion Capture amb Docker, OpenCV i FFmpeg

[![CI Tests](https://github.com/fantasyrubberduck/capmotion/actions/workflows/tests.yml/badge.svg)](https://github.com/fantasyrubberduck/capmotion/actions/workflows/tests.yml)
![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green)
[![Codecov Coverage](https://codecov.io/gh/fantasyrubberduck/capmotion/branch/main/graph/badge.svg)](https://codecov.io/gh/fantasyrubberduck/capmotion)

---

## 📌 Descripció
Aquest projecte permet **capturar automàticament fragments de vídeo quan es detecta moviment** en una font de càmera (webcam local o càmera IP via RTSP).  
Està pensat per ser **portable, escalable i fàcil d’integrar en CI/CD**, utilitzant Docker i Docker Compose.

---

## 🚀 Quick Start

```bash
# 1. Clona el repositori
git clone https://github.com/fantasyrubberduck/capmotion.git
cd capmotion

# 2. Construeix les imatges Docker
make build

# 3. Arrenca els serveis (webcam + ipcam)
make up
```

📌 Els clips es guarden automàticament a la carpeta `output/`.

---

### 🔧 Notes especials per WSL
Si utilitzes **WSL (Windows Subsystem for Linux)** i vols accedir a dispositius USB (per exemple, webcams locals), cal instal·lar prèviament **usb-ipd-win**.  
Guia oficial: [usb-ipd-win WSL support](https://github.com/dorssel/usbipd-win/wiki/WSL-support)

---

## 🚀 Funcionalitats
- Detecció de moviment amb **OpenCV** (comparació de frames i contorns).
- Gravació automàtica de clips en **MP4** amb **FFmpeg**.
- Suport per **múltiples càmeres** (webcam + IP cam) via `docker-compose`.
- Mode **headless** (sense dependències gràfiques).
- Tests automàtics amb **pytest**:
  - Unit tests (mock) per validar la lògica de detecció.
  - Tests d’integració amb FFmpeg per comprovar la gravació.
- Workflow de **GitHub Actions** amb matriu de versions de Python i cobertura amb Codecov.

---

## 📂 Estructura del projecte
```
project/
 ├── Dockerfile
 ├── docker-compose.yml
 ├── Makefile
 ├── requirements.txt
 ├── motion_capture.py
 ├── tests/
 │    ├── test_motion_capture.py
 │    └── test_motion_detection.py
 └── output/   # carpeta on es guarden els clips
```

---

## 🐳 Ús amb Docker

### Construir la imatge
```bash
make build
```

### Arrencar tots els serveis en segon pla
```bash
make up
```

### Arrencar en primer pla (foreground)
```bash
make up-fg
```

### Arrencar només webcam
```bash
make webcam
```

### Arrencar només IP cam en primer pla
```bash
make ipcam-fg
```

### Veure logs
```bash
make logs
```

---

## ⚙️ Configuració de càmeres
Les fonts de vídeo es defineixen amb la variable d’entorn `CAMERA_SOURCE`:

- **Webcam local**: `/dev/video0`
- **Càmera IP (RTSP)**: `rtsp://user:password@IP:554/stream`

Exemple al `docker-compose.yml`:
```yaml
environment:
  - CAMERA_SOURCE=rtsp://user:password@192.168.1.50:554/stream
```

---

## 🧪 Tests

### Executar tests locals
```bash
pytest -v tests/
```

### Tipus de tests
- **Unit tests (mock)**: comproven la lògica de detecció de moviment amb frames sintètics.
- **Integration tests**: validen que FFmpeg genera clips correctes.

---

## 🔄 CI/CD amb GitHub Actions
El workflow `.github/workflows/tests.yml` executa automàticament:
- Els tests en **Python 3.9, 3.10 i 3.11**.
- Instal·lació de dependències i FFmpeg.
- Validació en cada `push` o `pull request`.
- Reporta cobertura de tests a **Codecov**.

---

## 🌐 Escalabilitat
- Afegir més càmeres duplicant serveis al `docker-compose.yml`.
- Integració fàcil amb pipelines de CI/CD.
- Possibilitat d’extensió amb notificacions o processament avançat (per ex. reconeixement d’actors).

---

## 📜 Llicència
Aquest projecte utilitza **programari lliure** sota llicència MIT.
