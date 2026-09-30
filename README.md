# Data App - Série Histórica de Preços de Combustíveis (2025-2026)

<img width="1920" height="800" alt="Captura de Tela (299)" src="https://github.com/user-attachments/assets/1e22d86f-86f1-4024-bd30-cd9a3ab35e21" />

<img width="1920" height="816" alt="Captura de Tela (300)" src="https://github.com/user-attachments/assets/df8e5998-6ea7-4d23-9ec9-fbaed5d90cf1" />

<img width="1920" height="816" alt="Captura de Tela (301)" src="https://github.com/user-attachments/assets/a2bd89f1-fb7b-4b4f-9905-2d18ce700455" />

<img width="1920" height="804" alt="Captura de Tela (302)" src="https://github.com/user-attachments/assets/fb419583-d5d0-41e6-b31b-b63a153771af" />



Uma aplicação web interativa desenvolvida com **Streamlit** para análise exploratória de dados (EDA) e visualização da evolução dos preços da gasolina ao longo dos anos de 2025 e 2026.

🚀 **Aplicação Online:** [Clique aqui para aceder ao Dashboard no Streamlit Cloud](https://data-app-combustiveis-25-26.streamlit.app) *(substitua pelo link real da sua app, caso seja diferente)*

## 🌟 Funcionalidades Principais
* **Visualização de Dados:** Gráficos interativos (Plotly) que demonstram a flutuação dos preços.
* **Análise Exploratória (EDA):** Ferramentas para compreender padrões e tendências nos dados históricos.
* **Assistente de IA:** Integração com LangChain e OpenAI para interagir com o *dataframe* de forma inteligente.
* **Interface Dinâmica:** Painel de controlo interativo e responsivo.

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Streamlit** (Criação da interface Web)
* **Pandas** (Manipulação e análise de dados)
* **Plotly** (Criação de gráficos interativos)
* **LangChain & OpenAI** (Agente de IA para análise do *dataframe*)
* **Git & GitHub** (Controlo de versões e *deploy*)

## 📂 Estrutura do Repositório
* `app.py`: Código principal da aplicação web.
* `requirements.txt`: Lista de todas as dependências e bibliotecas necessárias para correr o projeto e fazer o *deploy*.
* `reduzir_dados.py`: Script utilizado para gerar uma amostra mais leve da base de dados original.
* `data/gasolina_amostra.csv`: Base de dados reduzida (5.000 linhas) utilizada para demonstração no *deploy*.
* `.gitignore`: Ficheiro de configuração para evitar o envio da base de dados completa e ficheiros sensíveis.

## ⚠️ Nota sobre os Dados (Deploy vs Local)
Devido aos limites de armazenamento do GitHub, o ficheiro de dados original (`gasolina_unique.csv`, com cerca de 200 MB) **não está incluído** neste repositório. 
A versão online da aplicação corre utilizando uma amostra de 5.000 linhas (`gasolina_amostra.csv`). 

Se desejar correr o projeto localmente com a base de dados completa:
1. Descarregue o ficheiro original e coloque-o na pasta `data/`.
2. No ficheiro `app.py`, altere a função de leitura para: `df = pd.read_csv('data/gasolina_unique.csv', ...)`

## 💻 Como Executar Localmente

1. **Clone este repositório para a sua máquina:**
   ```bash
   git clone [https://github.com/VitorL300/Data-App---S-rie-Hist-rica-de-Pre-os-de-Combust-veis-2025-2026.git](https://github.com/VitorL300/Data-App---S-rie-Hist-rica-de-Pre-os-de-Combust-veis-2025-2026.git)
