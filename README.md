Descrição do Projeto
Este é um sistema desktop completo para gestão de produtividade, que combina uma lista de tarefas (To-Do List) com a técnica Pomodoro. O software permite o cadastro de atividades com diferentes níveis de prioridade, monitorização de tempo e visualização de desempenho através de relatórios gráficos.

 Tecnologias e Bibliotecas Utilizadas
Python 3.x: Linguagem base do projeto.

Tkinter: Interface gráfica (GUI).

JSON: Persistência de dados para armazenamento das tarefas.

Matplotlib (v3.8.0 ou superior): Geração de gráficos estatísticos na aba de Relatórios.

 Estrutura de Arquivos
O projeto segue o princípio da separação de responsabilidades para garantir um código limpo e organizado:

models.py: Contém a classe Tarefa (Lógica de objetos).

database.py: Responsável por salvar e ler os dados no arquivo JSON (Persistência).

views.py: Arquivo principal que contém toda a interface gráfica e navegação (Interface).

tarefas.json: Arquivo gerado automaticamente para guardar as tuas informações.

 Como Executar o Projeto
Certifica-te de ter o Python instalado.

Instala a biblioteca de gráficos via terminal:

Bash

pip install matplotlib
Executa o arquivo principal:

Bash

python views.py
 Funcionalidades Principais
Dashboad: Menu lateral intuitivo para navegação rápida.

Gestão de Tarefas: Cadastro com título, categoria e prioridade.

Timer Pomodoro: Cronómetro regressivo com alertas de conclusão.

Relatórios Visuais: Gráfico de barras que mostra a distribuição de tarefas por prioridade.

Configurações: Personalização do tempo de foco e notificações sonoras.