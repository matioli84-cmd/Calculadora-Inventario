import streamlit as st

# Configuração visual da página
st.set_page_config(page_title="Calculadora de Custos de Inventário", page_icon="⚖️", layout="centered")

st.title("⚖️ Estimativa de Custos de Inventário")
st.write("Simule os custos com impostos, cartório e honorários para o seu planejamento sucessório.")

# --- SEÇÃO 1: PATRIMÔNIO (Campos do modelo de referência) ---
st.subheader("PATRIMÔNIO")

v_imoveis = st.number_input("Imóveis (R$)", min_value=0.0, value=0.0, step=10000.0, format="%.2f")
v_veiculos = st.number_input("Veículos (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f")
v_saldo = st.number_input("Saldo em conta e poupança (R$)", min_value=0.0, value=0.0, step=1000.0, format="%.2f")
v_investimentos = st.number_input("Investimentos (renda fixa, ações, fundos) (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f")
v_cotas = st.number_input("Cotas de empresas / participações societárias (R$)", min_value=0.0, value=0.0, step=10000.0, format="%.2f")
v_previdencia = st.number_input("Previdência privada (PGBL / VGBL) (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f", help="Isento de ITCMD na maioria das jurisdições.")
v_seguro = st.number_input("Seguro de vida (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f", help="Não entra em inventário nem sofre incidência de ITCMD.")

# Agrupamento dos valores
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
    st.caption("A alíquota aplicada será a média de 5,00%.")
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

# --- SEÇÃO 3: SITUAÇÃO FAMILIAR E TIPO DE INVENTÁRIO ---
st.subheader("REGIME E TIPO DE INVENTÁRIO")

estado_civil = st.selectbox("Estado civil do falecido:", ["Solteiro(a) / Divorciado(a) / Viúvo(a)", "Casado(a) / União Estável"])

meacao = False
if estado_civil == "Casado(a) / União Estável":
    regime = st.selectbox("Regime de Bens:", ["Comunhão Parcial de Bens", "Comunhão Universal de Bens", "Separação Total de Bens"])
    if regime in ["Comunhão Parcial de Bens", "Comunhão Universal de Bens"]:
        meacao = st.checkbox("Aplicar 50% de meação do cônjuge sobre os bens tributáveis", value=True)

via = st.radio("Tipo de Inventário pretendido:", ["Extrajudicial (Cartório)", "Judicial"])

# --- CÁLCULO FINAL DA ESTIMATIVA ---
if meacao:
    base_itcmd = patrimonio_tributavel / 2
else:
    base_itcmd = patrimonio_tributavel

v_itcmd = base_itcmd * aliquota_itcmd
v_honorarios = patrimonio_total * 0.08  # Média de honorários advocatícios
v_cartorio = patrimonio_tributavel * 0.015 if via == "Extrajudicial (Cartório)" else patrimonio_tributavel * 0.02
v_total = v_itcmd + v_honorarios + v_cartorio

# --- BOTAO DE CÁLCULO & RESULTADOS ---
if st.button("CALCULAR ESTIMATIVA", type="primary", use_container_width=True):
    st.divider()
    st.subheader("📊 Resultado da Estimativa de Custos")
    
    if v_previdencia > 0 or v_seguro > 0:
        st.success(f"✅ **Benefício Fiscal:** R$ {(v_previdencia + v_seguro):,.2f} alocados em Previdência e Seguro de Vida não entram na base de cálculo do ITCMD e inventário.")

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
    st.subheader("📲 Quer analisar o seu caso em detalhes?")
    link_whatsapp = "https://wa.me/5500000000000"  # Substitua pelo seu número com DDD
    st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:5px; font-size:18px; font-weight:bold; cursor:pointer;">Falar com Especialista no WhatsApp</button></a>', unsafe_allow_html=True)
