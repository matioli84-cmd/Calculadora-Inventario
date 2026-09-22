import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Custos de Inventário", 
    page_icon="⚖️", 
    layout="centered"
)

# --- INJEÇÃO DE CSS PERSONALIZADO (TEMA XP INVESTIMENTOS) ---
st.markdown("""
    <style>
    /* Fundo principal e cor de texto geral */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Cor dos títulos e subtítulos */
    h1, h2, h3, h4, label, .stMarkdown {
        color: #FFFFFF !important;
    }
    
    /* Destaque para o título principal com o tom Ouro XP */
    h1 {
        font-weight: 700;
        color: #C5A059 !important;
        border-bottom: 2px solid #C5A059;
        padding-bottom: 10px;
    }

    /* Estilização dos campos de entrada de número e seleção */
    .stNumberInput input, .stSelectbox select {
        background-color: #121212 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }
    
    .stNumberInput input:focus {
        border-color: #C5A059 !important;
    }

    /* Estilização do Botão Primário (Calcular) - Estilo Ouro XP */
    div.stButton > button:first-child {
        background-color: #C5A059 !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #E2B866 !important;
        color: #000000 !important;
        box-shadow: 0px 4px 15px rgba(197, 160, 89, 0.4);
    }

    /* Métrica / Destaques de Resultados */
    [data-testid="stMetricValue"] {
        color: #C5A059 !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #CCCCCC !important;
    }

    /* Caixas de Alerta / Sucesso */
    .stAlert {
        background-color: #121212 !important;
        border: 1px solid #C5A059 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("⚖️ Estimativa de Custos de Inventário")
st.write("Simule com precisão os custos com impostos (ITCMD), taxas de cartório e honorários advocatícios para a sua gestão patrimonial.")

# --- SEÇÃO 1: PATRIMÔNIO ---
st.subheader("PATRIMÔNIO")

v_imoveis = st.number_input("Imóveis (R$)", min_value=0.0, value=0.0, step=10000.0, format="%.2f")
v_veiculos = st.number_input("Veículos (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f")
v_saldo = st.number_input("Saldo em conta e poupança (R$)", min_value=0.0, value=0.0, step=1000.0, format="%.2f")
v_investimentos = st.number_input("Investimentos (Renda Fixa, Ações, Fundos) (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f")
v_cotas = st.number_input("Cotas de empresas / Participações societárias (R$)", min_value=0.0, value=0.0, step=10000.0, format="%.2f")
v_previdencia = st.number_input("Previdência Privada (PGBL / VGBL) (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f", help="A Previdência Privada é isenta de ITCMD na grande maioria dos Estados.")
v_seguro = st.number_input("Seguro de Vida (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f", help="Seguros de vida não entram no inventário e não sofrem tributação de ITCMD.")

patrimonio_total = v_imoveis + v_veiculos + v_saldo + v_investimentos + v_cotas + v_previdencia + v_seguro
patrimonio_tributavel = v_imoveis + v_veiculos + v_saldo + v_investimentos + v_cotas

st.divider()

# --- SEÇÃO 2: IMPOSTO DE HERANÇA (ITCMD) ---
st.subheader("IMPOSTO DE HERANÇA (ITCMD)")

opcao_itcmd = st.radio(
    "Escolha a forma de definição do ITCMD:",
    ["Não sei (usaremos a média nacional de 5%)", "Sei a alíquota ou estado de localização dos bens"]
)

if "Não sei" in opcao_itcmd:
    aliquota_itcmd = 0.05
    st.caption("Alíquota calculada com base na média nacional de 5,00%.")
else:
    uf_selecionada = st.selectbox(
        "Selecione o Estado (UF) do inventário:",
        ["SP - São Paulo (4%)", "RJ - Rio de Janeiro (5% a 8%)", "MG - Minas Gerais (5%)", 
         "PR - Paraná (4%)", "SC - Santa Catarina (1% a 8%)", "RS - Rio Grande do Sul (3% a 6%)", "Outro Estado (Digitar % manualmente)"]
    )
    
    if "SP" in uf_selecionada or "PR" in uf_selecionada:
        aliquota_itcmd = 0.04
    elif "RJ" in uf_selecionada:
        aliquota_itcmd = 0.08 if patrimonio_tributavel > 400000 else 0.05
    elif "MG" in uf_selecionada:
        aliquota_itcmd = 0.05
    elif "Outro" in uf_selecionada:
        aliq_manual = st.number_input("Informe a alíquota do seu Estado (%):", min_value=0.0, max_value=8.0, value=4.0, step=0.5)
        aliquota_itcmd = aliq_manual / 100
    else:
        aliquota_itcmd = 0.05

st.divider()

# --- SEÇÃO 3: SITUAÇÃO FAMILIAR E INVENTÁRIO ---
st.subheader("REGIME DE BENS E TIPO DE INVENTÁRIO")

estado_civil = st.selectbox("Estado civil do falecido:", ["Solteiro(a) / Divorciado(a) / Viúvo(a)", "Casado(a) / União Estável"])

meacao = False
if estado_civil == "Casado(a) / União Estável":
    regime = st.selectbox("Regime de Bens:", ["Comunhão Parcial de Bens", "Comunhão Universal de Bens", "Separação Total de Bens"])
    if regime in ["Comunhão Parcial de Bens", "Comunhão Universal de Bens"]:
        meacao = st.checkbox("Aplicar 50% de meação do cônjuge sobre os bens tributáveis", value=True)

via = st.radio("Tipo de Inventário pretendido:", ["Extrajudicial (Cartório)", "Judicial"])

# --- CÁLCULO DAS REGRAS ---
if meacao:
    base_itcmd = patrimonio_tributavel / 2
else:
    base_itcmd = patrimonio_tributavel

v_itcmd = base_itcmd * aliquota_itcmd
v_honorarios = patrimonio_total * 0.08
v_cartorio = patrimonio_tributavel * 0.015 if via == "Extrajudicial (Cartório)" else patrimonio_tributavel * 0.02
v_total = v_itcmd + v_honorarios + v_cartorio

# --- AÇÃO & EXIBIÇÃO DE RESULTADOS ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("CALCULAR ESTIMATIVA", type="primary", use_container_width=True):
    st.divider()
    st.subheader("📊 Resumo Executivo dos Custos")
    
    if v_previdencia > 0 or v_seguro > 0:
        st.success(f"✅ **Eficiência Fiscal:** R$ {(v_previdencia + v_seguro):,.2f} alocados em Previdência/Seguro não entram no inventário e estão isentos de ITCMD.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Patrimônio Total Declarado", f"R$ {patrimonio_total:,.2f}")
        st.metric("Base TRIBUTÁVEL do ITCMD", f"R$ {base_itcmd:,.2f}")
        st.metric("Imposto ITCMD Estimado", f"R$ {v_itcmd:,.2f}")

    with col2:
        st.metric("Honorários Advocatícios (Est.)", f"R$ {v_honorarios:,.2f}")
        st.metric("Custas (Cartório/Judicial)", f"R$ {v_cartorio:,.2f}")
        st.metric("CUSTO TOTAL ESTIMADO", f"R$ {v_total:,.2f}")

    st.divider()
    st.subheader("📲 Fale com um Especialista")
    st.write("Agende uma consulta para realizar o planejamento sucessório com máxima economia fiscal.")
    
    link_whatsapp = "https://wa.me/5500000000000"  # Substitua pelo seu número com DDD
    st.markdown(f'''
        <a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
            <button style="
                width:100%; 
                height:52px; 
                background-color:#25D366; 
                color:white; 
                border:none; 
                border-radius:6px; 
                font-size:18px; 
                font-weight:bold; 
                cursor:pointer;
                box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3);">
                Atendimento via WhatsApp
            </button>
        </a>
    ''', unsafe_allow_html=True)
