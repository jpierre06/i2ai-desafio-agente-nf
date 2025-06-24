import os
import shutil
import zipfile
import pandas as pd
from datetime import datetime
from pathlib import Path

# Caminhos base
UNPROCESSED_DIR = Path("./data/stage/unprocessed")
PROCESSED_DIR = Path("./data/stage/processed")
ITEMS_DIR = Path("./data/csv/items")
HEADS_DIR = Path("./data/csv/heads")
LOG_DIR = Path("./logs")

# Criar diretórios se não existirem
for path in [PROCESSED_DIR, ITEMS_DIR, HEADS_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)

def is_item_csv(file_bytes: bytes) -> bool:
    """Verifica se o CSV contém a coluna 'NÚMERO PRODUTO'"""
    try:
        df = pd.read_csv(pd.io.common.BytesIO(file_bytes), nrows=1)
        cols = [col.strip().upper() for col in df.columns]
        return "NÚMERO PRODUTO" in cols
    except Exception:
        return False

def process_zip_files():
    zip_files = list(UNPROCESSED_DIR.glob("*.zip"))
    if not zip_files:
        print("Nenhum arquivo ZIP para processar.")
        return

    for zip_path in zip_files:
        log_entries = []
        success = True
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                for name in z.namelist():
                    if not name.lower().endswith(".csv"):
                        continue

                    file_bytes = z.read(name)
                    destination_dir = ITEMS_DIR if is_item_csv(file_bytes) else HEADS_DIR
                    out_path = destination_dir / name
                    with open(out_path, "wb") as f_out:
                        f_out.write(file_bytes)

                    log_entries.append(f"[OK] {name} → {destination_dir}")

            # Mover ZIP para processed
            shutil.move(str(zip_path), PROCESSED_DIR / zip_path.name)

        except Exception as e:
            log_entries.append(f"[ERRO] {zip_path.name}: {str(e)}")
            success = False

        # Gerar log
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"processamento_{zip_path.stem}_{timestamp}.log"
        log_path = LOG_DIR / log_filename

        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(f"Arquivo ZIP: {zip_path.name}\n")
            log_file.write(f"Data: {timestamp}\n")
            log_file.write("\n".join(log_entries))
            log_file.write("\nStatus: " + ("SUCESSO" if success else "FALHA"))

        print(f"Processamento de '{zip_path.name}': {'ok' if success else 'falhou'}")

if __name__ == "__main__":
    process_zip_files()
