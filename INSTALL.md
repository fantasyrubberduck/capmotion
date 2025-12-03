# 📥 Instal·lació del projecte Motion Capture

Aquest document descriu els passos necessaris per instal·lar i executar el projecte de **detecció de moviment i gravació automàtica** amb Docker, OpenCV i FFmpeg.

---

## 🔧 Requisits previs

- **Docker** (>= 20.10)
- **Docker Compose** (>= 1.29)
- **Python 3.9+** (si vols executar els tests fora de Docker)
- **FFmpeg** (ja inclòs dins el contenidor, només necessari si vols provar localment)

---

## 🐧 Instal·lació en Linux / macOS

1. Clona el repositori:
   ```bash
   git clone https://github.com/fantasyrubberduck/capmotion.git
   cd capmotion
   ```

2. Construeix les imatges Docker:
   ```bash
   make build
   ```

3. Arrenca els serveis:
   ```bash
   make up
   ```

---

## 🪟 Instal·lació en Windows amb WSL

Si utilitzes **WSL (Windows Subsystem for Linux)** i vols accedir a dispositius USB (per exemple, webcams locals), cal instal·lar prèviament **usb-ipd-win**.

📌 Guia oficial: [usb-ipd-win WSL support](https://github.com/dorssel/usbipd-win/wiki/WSL-support)

### Passos:

1. Instal·la `usb-ipd-win` a Windows:
   ```powershell
   winget install dorssel.usbipd-win
   ```

2. Connecta el dispositiu USB al WSL:
   ```powershell
   usbipd list
   usbipd attach --wsl --busid <BUSID>
   ```

3. Comprova que el dispositiu és visible dins WSL:
   ```bash
   lsusb
   ```

4. Un cop el dispositiu estigui disponible, pots arrencar el projecte amb:
   ```bash
   make up
   ```

---

## 🧪 Execució de tests

Per executar els tests automàtics amb `pytest`:

```bash
pytest -v tests/
```

---

## ✅ Notes finals

- Els clips es guarden a la carpeta `output/`.
- Pots afegir més càmeres duplicant serveis al `docker-compose.yml`.
- En entorns WSL, assegura’t que el dispositiu USB està **adjunt amb usb-ipd-win** abans d’arrencar els contenidors.
