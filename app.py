import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import timedelta
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import os


# CSS 

st.set_page_config(page_title="Dashboard Combustíveis", layout="wide")

custom_css = """
<style>
    /* Importação das Fontes Syne e DM Sans */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:ital,opsz,wght@0,17..18,400..700;1,17..18,400..700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* Tipografia Global */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    
    h1 { 
        font-family: 'Syne', sans-serif !important; 
    }
    
    h2, h3, h4, h5, h6 { 
        font-family: 'Google Sans', sans-serif !important; 
    }

    /* Fundo da Tela Principal (Mesh Gradient adaptado) */
    .stApp {
        background-color: #030712;
        background-image: 
            radial-gradient(ellipse 80vw 55vh at 5% 0%, rgba(0,212,170,.08) 0%, transparent 60%),
            radial-gradient(ellipse 60vw 50vh at 95% 5%, rgba(56,189,248,.07) 0%, transparent 55%),
            radial-gradient(ellipse 70vw 45vh at 50% 100%, rgba(167,139,250,.05) 0%, transparent 60%);
        color: rgba(255,255,255,.92);
    }
    
    /* Remove cor de fundo do header nativo */
    [data-testid="stHeader"] { background: transparent !important; }

    /* Fundo da Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(11,22,40,.97), rgba(5,13,26,.98)) !important;
        border-right: 1px solid rgba(255,255,255,.07) !important;
    }

    /* Título Principal com Gradiente Textual */
    .stApp h1 {
        background: linear-gradient(120deg, #00d4aa 0%, #38bdf8 60%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
        padding-bottom: 0.5rem;
    }

    /* Subtítulos */
    .stApp h3 {
        color: rgba(255,255,255,.92) !important;
        margin-top: 2rem !important;
    }

    /* Cartões de Métricas (Glassmorphism) */
    [data-testid="stMetric"] {
        border-radius: 22px;
        padding: 20px 18px 16px;
        background: linear-gradient(135deg, rgba(255,255,255,.055) 0%, rgba(255,255,255,.025) 100%);
        border: 1px solid rgba(255,255,255,.07);
        box-shadow: 0 1px 0 rgba(255,255,255,.07) inset, 0 4px 12px rgba(0,0,0,.30);
        transition: transform 240ms cubic-bezier(.2,.9,.2,1), box-shadow 240ms cubic-bezier(.2,.9,.2,1), border-color 240ms cubic-bezier(.2,.9,.2,1);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: rgba(0,212,170,.28);
        box-shadow: 0 1px 0 rgba(255,255,255,.09) inset, 0 20px 50px rgba(0,0,0,.45), 0 0 30px rgba(0,212,170,.07);
    }
    
    [data-testid="stMetricLabel"] { 
        font-family: 'Syne', sans-serif; 
        font-size: 0.72rem !important;
        font-weight: 700;
        text-transform: uppercase; 
        letter-spacing: 1.2px; 
        color: rgba(255,255,255,.50) !important; 
        justify-content: center;
    }
    
    [data-testid="stMetricValue"] { 
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.85rem !important; 
        font-weight: 700 !important; 
        color: rgba(255,255,255,.95) !important; 
        letter-spacing: -0.5px;
    }

    /* Containers dos Gráficos (Glass Card) */
    [data-testid="stPlotlyChart"] {
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,.07);
        background: rgba(255,255,255,.025);
        box-shadow: 0 12px 30px rgba(0,0,0,.30);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: transform 240ms cubic-bezier(.2,.9,.2,1), border-color 240ms cubic-bezier(.2,.9,.2,1);
        padding: 1.5rem;
        overflow-y: hidden;
    }

    [data-testid="stPlotlyChart"]:hover {
        transform: translateY(-2px);
        border-color: rgba(0,212,170,.20);
        overflow-y: hidden;
    }

    /* Ajuste visual das tags do filtro MultiSelect */
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(0, 212, 170, 0.15) !important;
        border: 1px solid rgba(0, 212, 170, 0.3) !important;
        border-radius: 16px;
    }
    .stMultiSelect [data-baseweb="tag"] span {
        color: #00d4aa !important;
        font-family: 'DM Sans', sans-serif;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# LIMPEZA DE DADOS 

colunas_uteis = [
    'Regiao - Sigla',
    'Estado - Sigla',
    'Municipio',
    'Revenda',
    'Produto',
    'Data da Coleta',
    'Valor de Venda',
    'Bandeira'
]

@st.cache_data
def load_data():
    df = pd.read_csv('data/gasolina_unique.csv', usecols=colunas_uteis, sep=';', decimal=',', low_memory=False)
    df = df.dropna(how='all')
    df['Data da Coleta'] = pd.to_datetime(df['Data da Coleta'], format='%d/%m/%Y', errors='coerce')
    df['Valor de Venda'] = pd.to_numeric(df['Valor de Venda'].astype(str).str.replace(',','.'), errors='coerce')
    df = df.dropna(subset=['Data da Coleta', 'Valor de Venda'])
    df['Ano'] = df['Data da Coleta'].dt.year.astype('int')
    return df

df = load_data()

# SIDEBAR / FILTROS 

st.sidebar.title("Controles")
st.sidebar.markdown("---")
st.sidebar.header("Filtros")

anos_unicos = sorted(df['Ano'].unique())
anos_selecionados = st.sidebar.multiselect("Selecione o(s) ano(s):", options=anos_unicos, default=anos_unicos)

produtos_unicos = sorted(df['Produto'].unique())
produtos_selecionados = st.sidebar.multiselect("Selecione o(s) produto(s):", options=produtos_unicos, default=produtos_unicos)

bandeiras_unicas = sorted(df['Bandeira'].unique())
bandeiras_selecionadas = st.sidebar.multiselect("Selecione a(s) bandeira(s):", options=bandeiras_unicas, default=bandeiras_unicas)

df_filtrado = df.copy()

if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['Ano'].isin(anos_selecionados)]
if produtos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['Produto'].isin(produtos_selecionados)]
if bandeiras_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['Bandeira'].isin(bandeiras_selecionadas)]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados. Por favor, altere sua seleção.")
    st.stop()
    
st.sidebar.markdown("---")
st.sidebar.header("Inteligência Artificial")
api_key = st.sidebar.text_input("Groq API Key (Começa com gsk_)", type="password").strip()


# CARTÕES KPI

st.markdown("### Resumo dos Indicadores")

preco_medio = df_filtrado['Valor de Venda'].mean()
total_postos = df_filtrado['Revenda'].nunique()

df_estado_barato = df_filtrado.groupby('Estado - Sigla')['Valor de Venda'].mean().reset_index()
estado_mais_barato = df_estado_barato.loc[df_estado_barato['Valor de Venda'].idxmin()]
sigla_estado_barato = estado_mais_barato['Estado - Sigla']
preco_estado_barato = estado_mais_barato['Valor de Venda']

df_estado_caro = df_filtrado.groupby('Estado - Sigla')['Valor de Venda'].mean().reset_index()
estado_mais_caro = df_estado_caro.loc[df_estado_caro['Valor de Venda'].idxmax()]
sigla_estado_caro = estado_mais_caro['Estado - Sigla']
preco_estado_caro = estado_mais_caro['Valor de Venda']

variacao_preco = 0.15 

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(label="Preço Médio (Geral)", value=f"R$ {preco_medio:.2f}", delta=f"R$ {variacao_preco:.2f}", delta_color="inverse")
with kpi2:
    st.metric(label="Total de Postos", value=f"{total_postos:,}".replace(",", "."))
with kpi3:
    st.metric(label="Estado Mais Barato", value=sigla_estado_barato, delta=f"R$ {preco_estado_barato:.2f} (média)", delta_color="off")
with kpi4:
    st.metric(label="Estado Mais Caro", value=sigla_estado_caro, delta=f"R$ {preco_estado_caro:.2f} (média)", delta_color="off")
with kpi5:
    st.metric(label="Volume de Coletas", value=f"{len(df_filtrado):,}".replace(",", "."))

# Abas
tab1, tab2, tab3 = st.tabs(['Análise de Mercado', 'Chatbot', 'Dados Brutos'])
st.divider()

with tab1:
    
    # ÁREA PRINCIPAL DA APLICAÇÃO 
    
    st.title("Análise de Preços de Combustíveis")

    df_media_diaria = df_filtrado.groupby(['Data da Coleta', 'Produto'])['Valor de Venda'].mean().reset_index()
    fig = px.line(df_media_diaria, x='Data da Coleta', y='Valor de Venda', color='Produto', labels={'Valor de Venda': 'Preço Médio (R$)', 'Data da Coleta': 'Data'}, title='Preço Médio Diário por Combustível')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        df_bandeiras = df_filtrado.groupby('Bandeira').agg(vol_vendas=('Valor de Venda', 'count'), preco_medio=('Valor de Venda', 'mean'), qtd_postos=('Revenda', 'nunique')).reset_index()
        st.subheader("Dispersão: Volume de Vendas vs. Valor de Venda por Bandeira")
        fig = px.scatter(df_bandeiras, x='vol_vendas', y='preco_medio', size='qtd_postos', color='Bandeira', hover_name='Bandeira', labels={'vol_vendas': 'Volume de Vendas', 'preco_medio': 'Valor Médio (R$)', 'qtd_postos': 'Postos'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 Bandeiras (Postos)")
        df_top_bandeiras = df_filtrado.groupby('Bandeira').agg(Qtd_Postos=('Revenda', 'nunique')).reset_index().sort_values(by='Qtd_Postos', ascending=False).head(10)
        fig_barras = px.bar(df_top_bandeiras.sort_values(by='Qtd_Postos', ascending=True), x='Qtd_Postos', y='Bandeira', orientation='h', text='Qtd_Postos', color='Qtd_Postos', color_continuous_scale='Blues', template='plotly_dark')
        fig_barras.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_barras.update_traces(textposition='outside') 
        st.plotly_chart(fig_barras, use_container_width=True)

    st.subheader("Preço Médio por Estado")
    df_estado = df_filtrado.groupby(['Estado - Sigla', 'Produto'])['Valor de Venda'].mean().reset_index().sort_values(by='Valor de Venda')
    fig = px.bar(df_estado, x='Estado - Sigla', y='Valor de Venda', color='Produto', barmode='group', labels={'Estado - Sigla': 'Estado', 'Valor de Venda': 'Preço Médio (R$)'})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)



# CHATBOT DE INSIGHTS COM GROQ

with tab2:
    st.markdown("### Converse com os dados filtrados")
    st.caption("A IA analisará os dados gratuitamente usando Llama 3.1 70B via Groq.")

    # 1. INICIALIZAÇÃO CRÍTICA DO SESSION STATE 
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "agent_memory" not in st.session_state:
        st.session_state.agent_memory = ""

    # 2. Exibição das mensagens antigas
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "code_figure" in msg and msg["code_figure"]:
                try:
                    exec(msg["code_figure"])
                    if 'fig' in locals():
                        st.plotly_chart(locals()['fig'], use_container_width=True)
                except Exception:
                    pass 

    # 3. Caixa de chat e lógica de execução
    if prompt := st.chat_input("Ex: Faça um top 5 de combustíveis mais vendidos."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            if not api_key.startswith("gsk_"):
                st.error("⚠️ Cole a chave da Groq (começa com gsk_) na barra lateral e aperte Enter.")
                st.stop()
                
            with st.spinner("Analisando dados (Isso leva poucos segundos na Groq)..."):
                try:
                    llm = ChatOpenAI(
                        api_key=api_key, 
                        base_url="https://api.groq.com/openai/v1", 
                        model="qwen/qwen3.8-27b", 
                        temperature=0,
                        max_tokens=800
                    )

                    PREFIX = """
                    Você é um analista de dados especialista em Python, Pandas e Plotly.
                    Você tem acesso a um dataframe chamado `df` com mais de 1.2 milhão de linhas.

                    REGRAS DE SOBREVIVÊNCIA DE DADOS (CRÍTICO):
                    1. NUNCA tente imprimir o dataframe inteiro (`print(df)`) ou colunas inteiras.
                    2. NUNCA tente retornar valores únicos de colunas com alta cardinalidade.
                    3. SEMPRE que for inspecionar dados, use `.head(5)`.
                    4. Se o usuário pedir um ranking, SEMPRE limite usando `.head(10)`.

                    INSTRUÇÕES PARA GRÁFICOS:
                    Se o usuário pedir um gráfico, crie a figura (fig) usando plotly.express (px) e SALVE no disco como HTML usando EXATAMENTE: 
                    fig.write_html('temp_fig.html')
                    NUNCA use fig.show().

                    CONTEXTO RECENTE:
                    {memory}
                    """
                    current_prefix = PREFIX.replace("{memory}", st.session_state.agent_memory)

                    
                    agent = create_pandas_dataframe_agent(
                        llm, 
                        df_filtrado, 
                        verbose=True, 
                        allow_dangerous_code=True, 
                        agent_type="openai-tools", 
                        prefix=current_prefix
                    )
                    
                    # Chama o agente DENTRO do bloco try, após ele ser definido
                    resposta_agente = agent.invoke(prompt)
                    insight = resposta_agente["output"]
                    
                    st.markdown(insight)
                    
                    chart_code_to_save = None
                    if os.path.exists('temp_fig.html'):
                         import streamlit.components.v1 as components
                         with open('temp_fig.html', 'r', encoding='utf-8') as f:
                             html_data = f.read()
                             components.html(html_data, height=500, scrolling=True)
                         os.remove('temp_fig.html')
                         st.info("💡 Dica: Gráficos gerados no chat são temporários na exibição atual.")

                    # Atualiza a memória corretamente
                    st.session_state.agent_memory += f"\nUsuário: {prompt}\nIA: {insight}"
                    
                    if len(st.session_state.agent_memory) > 1500:
                         st.session_state.agent_memory = st.session_state.agent_memory[-1000:]
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": insight
                    })
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro durante a análise: {e}")

# DADOS BRUTOS
with tab3:
    st.markdown(f'{len(df):,} Records')
    st.dataframe(df.sort_values('Data da Coleta', ascending=False), use_container_width=True, height=500)