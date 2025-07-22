from loguru import logger
import os
from datetime import datetime

# 🔄 Erstelle Log-Verzeichnis, falls nicht vorhanden
log_dir = os.path.join("memory", "logs")
os.makedirs(log_dir, exist_ok=True)

# 📁 Log-Dateiname mit Tagesdatum
log_filename = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y-%m-%d')}.log")

# 🧠 Konfiguration: Konsole + Datei
logger.remove()  # Entfernt default logger
logger.add(log_filename, level="INFO", rotation="10 MB", encoding="utf-8")
logger.add(lambda msg: print(msg, end=""), level="DEBUG")  # Konsole

# 📦 Optional: eigene Shortcut-Funktionen
log = logger
