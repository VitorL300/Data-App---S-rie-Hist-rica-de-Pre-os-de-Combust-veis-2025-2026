# Data App - Série Histórica de Preços de Combustíveis (2025-2026)

Uma aplicação interativa para análise exploratória de dados (EDA) e visualização da evolução dos preços da gasolina ao longo dos anos de 2025 e 2026.

## Funcionalidades Principais

* **Visualização de Dados:** Gráficos interativos que demonstram a flutuação dos preços da gasolina.
* **Análise Exploratória (EDA):** Ferramentas para compreender padrões, tendências e anomalias nos dados históricos.
* **Interface Dinâmica:** Painel de controlo (dashboard) interativo gerado a partir do ficheiro `app.py`.

## Tecnologias Utilizadas

* **Python**
* **Streamlit / Pandas** *(Ajuste consoante as bibliotecas exatas que usou no `app.py`)*
* **Git e GitHub** para controlo de versões

## Estrutura do Repositório

* `app.py`: Código principal da aplicação web.
* `.gitignore`: Ficheiro de configuração que impede o envio de dados sensíveis ou ficheiros pesados.
* `data/`: Pasta designada para o armazenamento da base de dados local.

> **Nota sobre os Dados:** O ficheiro original da base de dados (`gasolina_unique.csv`) possui cerca de 200 MB e não está incluído neste repositório devido aos limites de tamanho do GitHub. Para correr o projeto, é necessário descarregar a base de dados original e colocá-la na pasta `data/`.

## Como Executar Localmente

1. **Clone este repositório para a sua máquina:**
```bash
git clone https://github.com/VitorL300/Data-App---S-rie-Hist-rica-de-Pre-os-de-Combust-veis-2025-2026.git

```


2. **Aceda à pasta do projeto:**
```bash
cd Data-App---S-rie-Hist-rica-de-Pre-os-de-Combust-veis-2025-2026

```


3. **Configure a base de dados:**
Crie uma pasta chamada `data` (caso não exista) e coloque o ficheiro `gasolina_unique.csv` no seu interior.
4. **Execute a aplicação:**
```bash
python app.py

```


*(Se estiver a utilizar o Streamlit, substitua o comando por `streamlit run app.py`)*

---

*Sinta-se à vontade para editar os nomes das bibliotecas ou adicionar um tópico sobre as variáveis de ambiente, caso volte a utilizar chaves de API num futuro ficheiro de testes.*
