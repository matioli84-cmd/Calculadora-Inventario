import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Custos de Inventário", page_icon="⚖️", layout="centered")

st.title("⚖️ Estimativa Profissional de Custos de Inventário")
st.write("Simule de forma detalhada os custos com impostos, cartório e honorários advocatícios para o seu caso.")

# --- ENTRADAS DE DADOS DESMEMBRADAS ---
st.subheader("1. Detalhamento do Patrimônio (R$)")

col_b1, col_b2 = st.columns(2)

with col_b1:
    v_imoveis = st.number_input("Imóveis (Casas, Apartamentos, Terrenos):", min_value=0.0, value=400000.0, step=10000.0, format="%.2f")
    v_moveis = st.number_input("Bens Móveis (Veículos, Máquinas, Joias):", min_value=0.0, value=50000.0, step=5000.0, format="%.2f")

with col_b2:
    v_financeiro = st.number_input("Aplicações Financeiras e Contas (CDB, Ações, Poupança):", min_value=0.0, value=50000.0, step=5000.0, format="%.2f")
    v_previdencia = st.number_input("Previdência Privada (VGBL / PGBL):", min_value=0.0, value=0.0, step=5000.0, format="%.2f", help="A previdência privada (VGBL/PGBL) não integra a herança para fins de cobrança do ITCMD na maioria das jurisdições.")

# Patrimônio Total Bruto e Patrimônio Tributável
patrimonio_total = v_imoveis + v_moveis + v_financeiro + v_previdencia
patrimonio_tributavel = v_imoveis + v_moveis + v_financeiro

st.divider()
st.subheader("2. Região e Situação Familiar")

uf = st.selectbox("Estado de localização dos bens/inventário:", [
    "SP - São Paulo", "RJ - Rio de Janeiro", "MG - Minas Gerais", 
    "PR - Paraná", "SC - Santa Catarina", "RS - Rio Grande do Sul", "Outros"
])

estado_civil = st.selectbox("Estado civil do falecido:", [
    "Solteiro(a) / Divorciado(a) / Viúvo(a)", 
    "Casado(a) / União Estável"
])

meacao = False
if estado_civil == "Casado(a) / União Estável":
    regime = st.selectbox("Regime de Bens do Casamento/União:", [
        "Comunhão Parcial de Bens", 
        "Comunhão Universal de Bens", 
        "Separação Total de Bens"
    ])
    if regime in ["Comunhão Parcial de Bens", "Comunhão Universal de Bens"]:
        meacao = st.checkbox("Aplicar 50% de meação do cônjuge sobre os bens comuns (Reduz a base de cálculo tributável)", value=True)

via = st.radio("Tipo de Inventário pretendido:", ["Extrajudicial (Cartório)", "Judicial"])

# --- CÁLCULOS DA REGRA DE NEGÓCIO ---

# 1. Ajuste de Meação sobre o patrimônio tributável
if meacao:
    base_itcmd = patrimonio_tributavel / 2
    nota_meacao = "💡 **Meação aplicada:** 50% do patrimônio tributável foi deduzido como meação do cônjuge e não sofre incidência do ITCMD."
else:
    base_itcmd = patrimonio_tributavel
    nota_meacao = "💡 **Sem dedução de meação:** 100% do patrimônio tributável entra na base do ITCMD."

# 2. Alíquota de ITCMD por Estado
if "SP" in uf:
    aliquota_itcmd = 0.04
elif "RJ" in uf:
    aliquota_itcmd = 0.08 if base_itcmd > 400000 else 0.05
elif "MG" in uf:
    aliquota_itcmd = 0.05
else:
    aliquota_itcmd = 0.04

v_itcmd = base_itcmd * aliquota_itcmd

# 3. Honorários Advocatícios (baseados no patrimônio total gerido)
v_honorarios = patrimonio_total * 0.08

# 4. Custas do Cartório / Processuais
v_cartorio = patrimonio_tributavel * 0.015 if via == "Extrajudicial (Cartório)" else patrimonio_tributavel * 0.02

v_total = v_itcmd + v_honorarios + v_cartorio

# --- RESUMO PROFISSIONAL DOS RESULTADOS ---
st.divider()
st.subheader("📊 Resumo da Estimativa de Custos")

if v_previdencia > 0:
    st.success(f"✅ **Economia Fiscal:** R$ {v_previdencia:,.2f} alocados em Previdência Privada foram totalmente isentos do ITCMD e custas do inventário.")

st.info(nota_meacao)

col1, col2 = st.columns(2)

with col1:
    st.metric("Patrimônio Total Declarado", f"R$ {patrimonio_total:,.2f}")
    st.metric("Base TRIBUTÁVEL para ITCMD", f"R$ {base_itcmd:,.2f}")
    st.metric("Imposto ITCMD Estimado", f"R$ {v_itcmd:,.2f}")

with col2:
    st.metric("Honorários Advocatícios (Est.)", f"R$ {v_honorarios:,.2f}")
    st.metric("Custas Cartorárias / Judiciais", f"R$ {v_cartorio:,.2f}")
    st.metric("CUSTO TOTAL ESTIMADO", f"R$ {v_total:,.2f}")

st.divider()

# Chamada de Captação no WhatsApp
st.subheader("📲 Gostaria de agendar uma análise detalhada do seu inventário?")
st.write("Fale com a nossa equipa especializada para elaborar o planeamento sucessório e reduzir o impacto fiscal.")

link_whatsapp = "https://wa.me/5500000000000"  # Substitua pelo seu número de WhatsApp com DDD
st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:5px; font-size:18px; font-weight:bold; cursor:pointer;">Atendimento via WhatsApp</button></a>', unsafe_allow_html=True)
