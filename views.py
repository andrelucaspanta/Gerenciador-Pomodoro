import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from models import Tarefa

class AppDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Pomodoro V3 - Profissional")
        self.geometry("1050x750")
        self.configure(bg="white")
        
        # Variáveis de Controle
        self.tempo_restante = 25 * 60  
        self.timer_rodando = False
        
        # Conexão com Banco de Dados
        self.db = Database()
        self.lista_tarefas = self.db.carregar_tarefas()

        # Layout Principal
        self.menu_lateral = tk.Frame(self, bg="#3b3b98", width=230)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False) 

        self.conteudo = tk.Frame(self, bg="white")
        self.conteudo.pack(side="right", expand=True, fill="both")

        self.criar_menu()
        self.mostrar_tela_tarefas() # Tela inicial

    def criar_menu(self):
        tk.Label(self.menu_lateral, text="MENU", fg="white", bg="#3b3b98", 
                 font=("Arial", 16, "bold")).pack(pady=30)
        
        botoes = [
            ("📋 Minhas Tarefas", self.mostrar_tela_tarefas),
            ("➕ Nova Tarefa", self.mostrar_tela_cadastro),
            ("⏱️ Pomodoro", self.mostrar_tela_pomodoro),
            ("📊 Relatórios", self.mostrar_tela_relatorio),
            ("⚙️ Configurações", self.mostrar_tela_configuracoes),
            ("ℹ️ Sobre", self.mostrar_tela_sobre)
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(self.menu_lateral, text=texto, command=comando, 
                            bg="#5758bb", fg="white", font=("Arial", 11, "bold"),
                            relief="flat", pady=15, padx=20, cursor="hand2", 
                            anchor="w", bd=0, activebackground="#3b3b98", activeforeground="white")
            btn.pack(fill="x", padx=10, pady=2)

    def limpar_tela(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    # --- ABA 1: MINHAS TAREFAS ---
    def mostrar_tela_tarefas(self):
        self.limpar_tela()
        tk.Label(self.conteudo, text="Gerenciamento de Tarefas", font=("Arial", 24, "bold"), bg="white", fg="#3b3b98").pack(pady=20)
        
        if not self.lista_tarefas:
            tk.Label(self.conteudo, text="Nenhuma tarefa cadastrada.", font=("Arial", 12), bg="white", fg="gray").pack(pady=50)
        else:
            for tarefa in self.lista_tarefas:
                card = tk.Frame(self.conteudo, bg="#f8f9fa", highlightbackground="#dee2e6", highlightthickness=1, padx=20, pady=15)
                card.pack(fill="x", padx=40, pady=8)
                
                info_texto = f"📌 {tarefa['titulo']} | Categoria: {tarefa['categoria']}"
                tk.Label(card, text=info_texto, bg="#f8f9fa", font=("Arial", 11, "bold")).pack(side="left")
                
                cor_prio = "red" if tarefa['prioridade'] == "Alta" else "orange" if tarefa['prioridade'] == "Média" else "green"
                tk.Label(card, text=tarefa['prioridade'], bg="#f8f9fa", fg=cor_prio, font=("Arial", 10, "bold")).pack(side="right")

    # --- ABA 2: NOVA TAREFA ---
    def mostrar_tela_cadastro(self):
        self.limpar_tela()
        tk.Label(self.conteudo, text="Cadastrar Nova Tarefa", font=("Arial", 24, "bold"), bg="white", fg="#3b3b98").pack(pady=30)
        
        form_container = tk.Frame(self.conteudo, bg="white")
        form_container.pack()

        estilo_label = {"bg": "white", "font": ("Arial", 10, "bold"), "fg": "#2d3436"}

        tk.Label(form_container, text="Título da Tarefa:", **estilo_label).grid(row=0, column=0, sticky="w", pady=(10,0))
        self.ent_titulo = tk.Entry(form_container, width=50, font=("Arial", 12), bd=1, relief="solid")
        self.ent_titulo.grid(row=1, column=0, pady=(5, 15))

        tk.Label(form_container, text="Categoria (ex: Trabalho, Estudo):", **estilo_label).grid(row=2, column=0, sticky="w", pady=(10,0))
        self.ent_categoria = tk.Entry(form_container, width=50, font=("Arial", 12), bd=1, relief="solid")
        self.ent_categoria.grid(row=3, column=0, pady=(5, 15))

        tk.Label(form_container, text="Grau de Prioridade:", **estilo_label).grid(row=4, column=0, sticky="w", pady=(10,0))
        self.combo_prioridade = ttk.Combobox(form_container, values=["Alta", "Média", "Baixa"], state="readonly", width=48, font=("Arial", 11))
        self.combo_prioridade.set("Média")
        self.combo_prioridade.grid(row=5, column=0, pady=(5, 25))

        tk.Button(self.conteudo, text="SALVAR TAREFA", command=self.salvar_tarefa_logica, 
                  bg="#44bd32", fg="white", font=("Arial", 12, "bold"), width=30, pady=12, relief="flat", cursor="hand2").pack(pady=20)

    def salvar_tarefa_logica(self):
        titulo = self.ent_titulo.get()
        categoria = self.ent_categoria.get()
        prioridade = self.combo_prioridade.get()
        
        if titulo.strip() == "":
            messagebox.showwarning("Aviso", "O título não pode estar vazio!")
            return
            
        nova_tarefa = Tarefa(titulo, categoria, prioridade)
        self.lista_tarefas.append(nova_tarefa.to_dict())
        self.db.salvar_tarefas(self.lista_tarefas) # Salva no banco de dados
        messagebox.showinfo("Sucesso", f"Tarefa '{titulo}' salva com sucesso!")
        self.mostrar_tela_tarefas()

    # --- ABA 3: POMODORO ---
    def mostrar_tela_pomodoro(self):
        self.limpar_tela()
        tk.Label(self.conteudo, text="Timer Pomodoro", font=("Arial", 24, "bold"), bg="white", fg="#e74c3c").pack(pady=30)
        
        self.label_timer = tk.Label(self.conteudo, text="25:00", font=("Arial", 80, "bold"), bg="white", fg="#2d3436")
        self.label_timer.pack(pady=40)
        
        botoes_timer = tk.Frame(self.conteudo, bg="white")
        botoes_timer.pack()
        
        tk.Button(botoes_timer, text="INICIAR", command=self.iniciar_pomodoro, bg="#3b3b98", fg="white", font=("Arial", 11, "bold"), width=15, pady=10).pack(side="left", padx=10)
        tk.Button(botoes_timer, text="PAUSAR", command=self.pausar_pomodoro, bg="#f39c12", fg="white", font=("Arial", 11, "bold"), width=15, pady=10).pack(side="left", padx=10)

    def iniciar_pomodoro(self):
        if not self.timer_rodando:
            self.timer_rodando = True
            self.atualizar_timer()

    def pausar_pomodoro(self):
        self.timer_rodando = False

    def atualizar_timer(self):
        if self.timer_rodando and self.tempo_restante > 0:
            self.tempo_restante -= 1
            mins, segs = divmod(self.tempo_restante, 60)
            self.label_timer.config(text=f"{mins:02d}:{segs:02d}")
            self.after(1000, self.atualizar_timer)
        elif self.tempo_restante <= 0:
            self.timer_rodando = False
            messagebox.showinfo("Fim!", "Hora de descansar!")

    # --- ABA 4: RELATÓRIOS (CORRIGIDA COM GRÁFICO) ---
    def mostrar_tela_relatorio(self):
        self.limpar_tela()
        tk.Label(self.conteudo, text="Resumo de Produtividade", font=("Arial", 24, "bold"), bg="white", fg="#3b3b98").pack(pady=20)
        
        if not self.lista_tarefas:
            tk.Label(self.conteudo, text="Nenhuma tarefa para exibir no gráfico.", font=("Arial", 12), bg="white", fg="gray").pack(pady=50)
            return

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        # Contagem
        contagem = {"Alta": 0, "Média": 0, "Baixa": 0}
        for t in self.lista_tarefas:
            prio = t.get("prioridade", "Média")
            if prio in contagem:
                contagem[prio] += 1

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.bar(contagem.keys(), contagem.values(), color=['#e74c3c', '#f1c40f', '#2ecc71'])
        ax.set_title("Tarefas por Prioridade")
        
        canvas = FigureCanvasTkAgg(fig, master=self.conteudo)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    # --- ABA 5: CONFIGURAÇÕES (COMPLETA) ---
    def mostrar_tela_configuracoes(self):
        self.limpar_tela()
        tk.Label(self.conteudo, text="Configurações", font=("Arial", 24, "bold"), bg="white", fg="#3b3b98").pack(pady=30)
        
        f1 = tk.LabelFrame(self.conteudo, text=" Interface e Sons ", bg="white", font=("Arial", 11, "bold"), padx=20, pady=15)
        f1.pack(padx=60, fill="x", pady=10)
        
        tk.Checkbutton(f1, text="Ativar Notificações Sonoras", bg="white", font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(f1, text="Modo Escuro (Beta)", bg="white", font=("Arial", 10)).pack(anchor="w")

        f2 = tk.LabelFrame(self.conteudo, text=" Ajustes de Tempo (Minutos) ", bg="white", font=("Arial", 11, "bold"), padx=20, pady=15)
        f2.pack(padx=60, fill="x", pady=10)
        
        tk.Label(f2, text="Tempo de Foco:", bg="white").grid(row=0, column=0, sticky="w")
        s1 = tk.Scale(f2, from_=5, to=60, orient="horizontal", bg="white", length=350, highlightthickness=0)
        s1.set(25)
        s1.grid(row=0, column=1, padx=20)

        tk.Button(self.conteudo, text="SALVAR PREFERÊNCIAS", bg="#3b3b98", fg="white", font=("Arial", 11, "bold"), 
                  width=30, pady=12, relief="flat", cursor="hand2").pack(pady=30)

    # --- ABA 6: SOBRE ---
    def mostrar_tela_sobre(self):
        self.limpar_tela()
        tk.Label(self.conteudo, text="Sobre o Sistema", font=("Arial", 24, "bold"), bg="white", fg="#3b3b98").pack(pady=30)
        
        texto_sobre = (
            "Gerenciador de Tarefas & Pomodoro v3.0\n\n"
            "Desenvolvido para fins acadêmicos.\n"
            "Tecnologias: Python, Tkinter, JSON.\n\n"
            "© 2026 Todos os direitos reservados."
        )
        tk.Label(self.conteudo, text=texto_sobre, font=("Arial", 13), bg="white", justify="center").pack(pady=20)

if __name__ == "__main__":
    app = AppDesktop()
    app.mainloop()