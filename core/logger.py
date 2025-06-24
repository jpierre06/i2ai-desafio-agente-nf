import os
import json
from datetime import datetime

def save_chat_log(question: str, answer: str, code: str, save_dir: str = "./logs"):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    filename = f"historico_chat_{timestamp}.json"
    filepath = os.path.join(save_dir, filename)

    os.makedirs(save_dir, exist_ok=True)

    log_data = {
        timestamp: [
            {"pergunta": question},
            {"resposta": answer},
            {"codigo_python": code}
        ]
    }

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return f"❌ Ocorreu um erro ao salvar o histórico do chat: {str(e)}"
