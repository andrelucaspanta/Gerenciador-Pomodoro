import json
import os

class Database:
    def __init__(self, arquivo="tarefas.json"):
        self.arquivo = arquivo

    def salvar_tarefas(self, tarefas):
        try:
            with open(self.arquivo, "w", encoding="utf-8") as f:
                json.dump(tarefas, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False

    def carregar_tarefas(self):
        if not os.path.exists(self.arquivo):
            return []
        
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return []