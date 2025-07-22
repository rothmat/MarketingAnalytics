import os
import json
from datetime import datetime
from core.logger import log

def save_output(data: dict, filetype: str = "json") -> str:
    """
    Speichert Agentenoutput automatisch in /outputs/{date}/{timestamp}_output.{json/csv}
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    # 🔁 Ordner erstellen
    output_dir = os.path.join("outputs", date_str)
    os.makedirs(output_dir, exist_ok=True)

    # 📄 Dateiname
    filename = f"{time_str}_output.{filetype}"
    filepath = os.path.join(output_dir, filename)

    try:
        if filetype == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif filetype == "txt":
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(str(data))
        else:
            raise ValueError("Nur json oder txt erlaubt.")
        log.success(f"💾 Output gespeichert: {filepath}")
        return filepath
    except Exception as e:
        log.error(f"❌ Fehler beim Speichern: {e}")
        return ""
