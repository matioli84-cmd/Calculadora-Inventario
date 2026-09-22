import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Custos de Inventário", page_icon="⚖️", layout="centered")

st.title("⚖️ Estimativa de Custos de Inventário")
st.write("Simule os custos com impostos, cartório e honorários para o seu caso.")

# --- ENTRADAS DE DADOS ---
st.subheader("1. Dados do Patrimônio e Família")

patrimonio = st.number_input("Valor total dos bens (R$):", min_value=0.0, value=500000.0, step=10000.0, format="%.2f")

uf = st.selectbox("Estado de localização dos imóveis/bens:", [
    "SP - São Paulo", "RJ - Rio de Janeiro", "MG - Minas Gerais", 
    "PR - Paraná", "SC - Santa Catarina", "RS - Rio Grande do Sul", "Outros"
])

estado_civil = st.selectbox("Estado civil do falecido:", [
    "Solteiro(a) / Divorciado(a) / Viúvo(a)", 
    "Casado(a) / União Estável"
])

# Lógica de Meação segundo Regime de Bens
meacao = False
if estado_civil == "Casado(a) / União Estável":
    regime = st.selectbox("Regime de Bens:", [
        "Comunhão Parcial de Bens", 
        "Comunhão Universal de Bens", 
        "Separação Total de Bens"
    ])
    if regime in ["Comunhão Parcial de Bens", "Comunhão Universal de Bens"]:
        meacao = st.checkbox("Os bens foram adquiridos durante o casamento? (Aplica 50% de meação)", value=True)

via = st.radio("Tipo de Inventário pretendido:", ["Extrajudicial (Cartório)", "Judicial"])

# --- CÁLCULO DAS REGRAS ---
if meacao:
    base_itcmd = patrimonio / 2
    meacao_texto = "50% do valor do patrimônio é referente à meação do cônjuge (não incide ITCMD)."
else:
    base_itcmd = patrimonio
    meacao_texto = "100% do patrimônio entra na base de cálculo da herança."

# Tabela de Alíquotas ITCMD (Exemplo de alíquotas médias por estado)
if "SP" in uf:
    aliquota_itcmd = 0.04
elif "RJ" in uf:
    aliquota_itcmd = 0.08 if base_itcmd > 400000 else 0.05
elif "MG" in uf:
    aliquota_itcmd = 0.05
else:
    aliquota_itcmd = 0.04

v_itcmd = base_itcmd * aliquota_itcmd
v_honorarios = patrimonio * 0.08  # Média de 8% de honorários
v_cartorio = patrimonio * 0.015 if via == "Extrajudicial (Cartório)" else patrimonio * 0.02

v_total = v_itcmd + v_honorarios + v_cartorio

# --- EXIBIÇÃO DOS RESULTADOS ---
st.divider()
st.subheader("📊 Resultado da Estimativa")

st.info(meacao_texto)

col1, col2 = st.columns(2)
with col1:
    st.metric("Base de Cálculo do ITCMD", f"R$ {base_itcmd:,.2f}")
    st.metric("Imposto ITCMD Estimado", f"R$ {v_itcmd:,.2f}")
    st.metric("Custas (Cartório/Judicial)", f"R$ {v_cartorio:,.2f}")

with col2:
    st.metric("Valor do Patrimônio Total", f"R$ {patrimonio:,.2f}")
    st.metric("Honorários Advocatícios (Est.)", f"R$ {v_honorarios:,.2f}")
    st.metric("CUSTO TOTAL ESTIMADO", f"R$ {v_total:,.2f}")

st.divider()

# Chamada para ação / Captação de Lead
st.subheader("📲 Quer analisar o seu caso em detalhes?")
st.write("Fale diretamente com nossa equipe especializada para planejar o inventário com economia fiscal.")

link_whatsapp = "https://wa.me/5500000000000"  # Coloque seu número aqui
st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:5px; font-size:18px; font-weight:bold;">Falar no WhatsApp</button></a>', unsafe_allow_html=True)
