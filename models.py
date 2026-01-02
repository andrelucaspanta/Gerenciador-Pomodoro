class Tarefa:
    def __init__(self, titulo, categoria, prioridade, status="Pendente"):
        self.titulo = titulo
        self.categoria = categoria
        self.prioridade = prioridade
        self.status = status

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "categoria": self.categoria,
            "prioridade": self.prioridade,
            "status": self.status
        }