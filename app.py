import streamlit as st
import streamlit.components.v1 as components
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from streamlit_lottie import st_lottie

# Nova função ultra-segura para carregar Lottie do seu próprio PC
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None # Se não achar o arquivo, não quebra o app!
    
lottie_robot = load_lottiefile("robot_ia.json")

# Configuração da página
st.set_page_config(page_title="Respiração do Futuro", page_icon="robot-assistant.png", layout="centered")


# --- INICIALIZAÇÃO DA MEMÓRIA DO APP (Placar Expandido) ---
if 'diag_saudavel' not in st.session_state: st.session_state.diag_saudavel = 0
if 'diag_asma' not in st.session_state: st.session_state.diag_asma = 0
if 'diag_gripe' not in st.session_state: st.session_state.diag_gripe = 0
if 'quiz_tentativas' not in st.session_state: st.session_state.quiz_tentativas = 0
if 'quiz_acertos_totais' not in st.session_state: st.session_state.quiz_acertos_totais = 0

# --- INJEÇÃO DE CSS (Visual Premium, Tipografia e Glassmorphism) ---
st.markdown("""
    <style>
    /* 1. Importando a fonte moderna Nunito do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* 2. Fundo com degradê: Branco no topo (esconde o Lottie) e azul suave no fundo */
    .stApp {
        background: linear-gradient(180deg, #ffffff 30%, #e6f2fa 100%);
    }

    /* 3. Sidebar com cor sólida moderna e fonte branca */
    [data-testid="stSidebar"] {
        background-color: #2e3b4e;
    }
    [data-testid="stSidebar"] * {
        color: rgba(255, 255, 255, 0.9) !important;
    }
            
    /* Deixa o fundo das animações Lottie e iframes transparente */
    iframe {
        background-color: transparent !important;
        border: none !important;
    }

    /* 4. Botões Super Arredondados e com Sombra (Estilo Mobile) */
    .stButton>button {
        background: linear-gradient(90deg, #1CAAD9 0%, #158ab3 100%);
        color: white !important;
        border-radius: 50px;
        font-weight: 800;
        font-size: 16px;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(28, 170, 217, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(28, 170, 217, 0.6);
    }

    /* 5. Caixas de Alerta (info, success, error) com Glassmorphism */
    div[data-testid="stAlert"] {
        border-radius: 20px;
        border: none;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        padding: 15px;
    }

    /* 6. Ocultar menu padrão do Streamlit (hambúrguer e rodapé) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}

    /* 7. Mantém as animações do título e do certificado */
    @keyframes respiracao {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .texto-respirando {
        animation: respiracao 4s infinite ease-in-out;
        color: #1CAAD9; text-align: center; font-size: 34px;
        font-weight: 900; margin-bottom: 25px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .certificado {
        border: 3px solid #1CAAD9; border-radius: 25px; padding: 30px;
        text-align: center; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
        box-shadow: 0 15px 35px rgba(28, 170, 217, 0.2); margin-top: 20px;
        animation: aparecer 1s ease-in-out;
    }
    @keyframes aparecer {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
            
    /* 8. Cards de Métricas Estilizados (Dashboard) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(28, 170, 217, 0.15);
    }
    div[data-testid="stMetricValue"] {
        color: #1CAAD9;
        font-size: 2.5rem !important;
        font-weight: 900;
    }

    /* 9. Animações de Pulmão (Experimento da Asma) */
    .pulmao-normal {
        animation: resp-normal 3s infinite ease-in-out;
        font-size: 60px; text-align: center; margin-bottom: 10px;
    }
    .pulmao-asma {
        animation: resp-asma 1s infinite ease-in-out;
        font-size: 60px; text-align: center; margin-bottom: 10px; opacity: 0.8;
    }
    @keyframes resp-normal { 
        0% {transform: scale(1);} 50% {transform: scale(1.3);} 100% {transform: scale(1);} 
    }
    @keyframes resp-asma { 
        0% {transform: scale(1);} 50% {transform: scale(1.08);} 100% {transform: scale(1);} 
    }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.image("robot-assistant.png", width=120) 
st.sidebar.title("Respiração do Futuro")
st.sidebar.info("Navegue pelas abas para acompanhar nossa apresentação!")

pagina = st.sidebar.radio(
    "Escolha a etapa:",
    ["1. Caminho do Ar", "2. Pulmão 3D", "3. Experimento da Asma", "4. IA de Diagnóstico", "5. Quiz Interativo 🎮", "📊 Dashboard da Feira"]
)

# --- ASSINATURA E DISCLAIMER NO MENU LATERAL ---
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: rgba(255,255,255,0.7); font-size: 13px; line-height: 1.5;'>Projeto integrante da<br><b>Mostra de Ciências 2026</b> 🧪</div>", unsafe_allow_html=True)

# Expansor de Créditos e Contato Técnico
with st.sidebar.expander("ℹ️ Sobre o Desenvolvimento"):
    st.caption(
        "Toda a pesquisa científica, roteiro de apresentação, idealização do projeto e a lógica "
        "médica por trás do algoritmo de triagem foram **100% desenvolvidos pelas alunas da equipe**."
    )
    st.caption(
        "A interface gráfica e o código-fonte foram estruturados por um desenvolvedor voluntário, "
        "atuando apenas como uma ponte tecnológica para materializar as excelentes ideias do grupo."
    )
    st.write("---")
    st.markdown("<p style='font-size: 14px; margin-bottom: 0;'><b>👨‍💻 Desenvolvedor:</b></p>", unsafe_allow_html=True)
    st.caption("👤 Guilherme Fernandes Meireles - Ex Aluno")
    st.caption("🎓 Estudante de Ciência da Computação")
    st.caption("💼 https://github.com/Beneguen75")
    
# --- ESTAÇÃO 1: O Caminho do Ar ---
if pagina == "1. Caminho do Ar":
    st.markdown("<div class='texto-respirando'>🌬️ O Caminho do Ar</div>", unsafe_allow_html=True)
    st.write("Navegue pelas abas abaixo para acompanhar a viagem do oxigênio:")
    tab1, tab2, tab3, tab4 = st.tabs(["👃 Nariz", "🗣️ Faringe", "🪈 Traqueia", "🌿 Brônquios"])
    
    with tab1:
        st.info("**Nariz:** Por onde o ar entra e é filtrado, aquecido e umedecido.")
        components.iframe("https://sketchfab.com/models/4d0361eccbff4ef5a66f79e508703c3a/embed", height=350)
    with tab2:
        st.info("**Faringe:** Canal que liga o nariz à traqueia.")
        components.iframe("https://sketchfab.com/models/b262c70bf9bd49c2a5428581b754f24b/embed", height=350)
    with tab3:
        st.info("**Traqueia:** Tubo que leva o ar em direção aos pulmões.")
        components.iframe("https://sketchfab.com/models/8458de63d0734776aa901615cf1f15ca/embed", height=350)
    with tab4:
        st.info("**Brônquios:** Canais que distribuem o ar para dentro dos pulmões.")
        components.iframe("https://sketchfab.com/models/c0ca6af6c6a1449084341a96eea515ea/embed", height=350)

# --- ESTAÇÃO 2: Pulmão 3D ---
elif pagina == "2. Pulmão 3D":
    st.markdown("<div class='texto-respirando'>🫁 Pulmão em 3D</div>", unsafe_allow_html=True)
    st.write("Gire, aproxime e explore o sistema respiratório usando a tecnologia!")
    st.info("**Pulmões:** Onde ocorre a troca de gases (oxigênio entra, gás carbônico sai).")
    components.iframe("https://sketchfab.com/models/b32c41dffc274a57aeffd45bc4ffc75a/embed", height=500)

# --- ESTAÇÃO 3: Experimento da Asma ---
elif pagina == "3. Experimento da Asma":
    st.markdown("<div class='texto-respirando'>🎈 Teste da Asma</div>", unsafe_allow_html=True)
    st.write("Observe o nosso pulmão artificial na mesa e veja a diferença na passagem do ar:")
    
    col1, col2 = st.columns(2)
    with col1:
        # Chama a animação do pulmão calmo e profundo
        st.markdown("<div class='pulmao-normal'>🫁</div>", unsafe_allow_html=True)
        st.success("🟢 **Canudo Largo**\n\n✔️ **Respiração Normal**\n\nO ar passa livremente, como em pulmões saudáveis. É fácil encher a bexiga.")
    with col2:
        # Chama a animação do pulmão rápido e curto
        st.markdown("<div class='pulmao-asma'>🫁</div>", unsafe_allow_html=True)
        st.error("🔴 **Canudo Fino**\n\n❌ **Respiração Dificultada**\n\nA asma estreita as vias aéreas. O ar luta para passar e causa muito cansaço.")

# --- ESTAÇÃO 4: IA de Diagnóstico (CHAT + LOTTIE) ---
elif pagina == "4. IA de Diagnóstico":
    st.markdown("<div class='texto-respirando'>🤖 Triagem Virtual</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if lottie_robot:
            st_lottie(lottie_robot, height=150, key="robot_ia")
        else:
            st.markdown("<h1 style='text-align: center; font-size: 80px; margin: 0;'>🤖</h1>", unsafe_allow_html=True)
            
    with col2:
        st.info("🧠 **Bio-Adaptação em Ação!**\n\nNosso sistema imita as conexões do cérebro humano para cruzar sintomas e alertar sobre obstruções respiratórias.")
    
    st.write("---")
    
    sintomas = st.multiselect(
        "Quais sintomas o visitante está sentindo?",
        ["Falta de ar", "Chiado no peito ao respirar", "Tosse seca", "Febre", "Dor de garganta", "Espirros constantes", "Nariz entupido"]
    )
    
    if st.button("Iniciar Consulta com a IA 🩺"):
        if len(sintomas) == 0:
            st.warning("Selecione pelo menos um sintoma para o robô analisar.")
        else:
            st.toast('Processando tensores...', icon='📡')
            
            # 1. Mensagem do Usuário
            with st.chat_message("user", avatar="👤"):
                st.write(f"**Paciente relata:** {', '.join(sintomas)}.")
            
            time.sleep(1)
            
            # 2. Mensagem da IA
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Analisando padrões biomédicos..."):
                    time.sleep(2) 
                
                risco_asma = 0
                risco_infeccao = 0
                
                if "Falta de ar" in sintomas: risco_asma += 50
                if "Chiado no peito ao respirar" in sintomas: risco_asma += 40
                if "Tosse seca" in sintomas: risco_asma += 10
                if "Febre" in sintomas: risco_infeccao += 45
                if "Dor de garganta" in sintomas: risco_infeccao += 35
                if "Espirros constantes" in sintomas: risco_infeccao += 10
                if "Nariz entupido" in sintomas: risco_infeccao += 10

                st.write("Análise concluída. Veja os resultados abaixo:")
                
                # Gráfico de Velocímetro
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = risco_asma,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Nível de Obstrução", 'font': {'size': 16}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "rgba(0,0,0,0)"}, 
                        'bgcolor': "white",
                        'steps': [
                            {'range': [0, 30], 'color': "#2ecc71"}, 
                            {'range': [30, 70], 'color': "#f1c40f"},
                            {'range': [70, 100], 'color': "#e74c3c"} 
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': risco_asma
                        }
                    }
                ))
                fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)

                if risco_asma >= 70:
                    st.session_state.diag_asma += 1
                    st.error("⚠️ **Crise de Asma / Obstrução Grave.** As vias aéreas estão muito fechadas (como o canudo fino da nossa experiência).")
                elif risco_infeccao >= 50:
                    st.session_state.diag_gripe += 1
                    st.warning("🟠 **Gripe ou Resfriado.** O problema principal parece ser uma infecção viral, e não asma.")
                else:
                    st.session_state.diag_saudavel += 1
                    st.success("✅ **Vias Limpas.** O pulmão parece funcionar perfeitamente (como o canudo largo).")

# --- ESTAÇÃO 5: Quiz Interativo (MÚLTIPLAS PERGUNTAS) ---
elif pagina == "5. Quiz Interativo 🎮":
    st.markdown("<div class='texto-respirando'>🏆 Desafio do Ar!</div>", unsafe_allow_html=True)
    st.write("Responda as 3 perguntas corretamente para liberar seu certificado!")
    
    # Formulário agrupa as respostas para não recarregar a página toda hora
    with st.form("quiz_form"):
        p1 = st.radio("1. Qual músculo fica embaixo dos pulmões e ajuda na respiração?", ["Escolha...", "Coração", "Diafragma", "Estômago"])
        p2 = st.radio("2. Na nossa experiência, o que o CANUDO FINO representava?", ["Escolha...", "Pulmão super forte", "Respiração normal", "Pessoa com Asma (obstrução)"])
        p3 = st.radio("3. Qual gás nosso corpo joga FORA quando respiramos?", ["Escolha...", "Gás Carbônico", "Oxigênio", "Gás Hélio"])
        
        enviou = st.form_submit_button("Corrigir Prova 📝")
        
    if enviou:
        st.session_state.quiz_tentativas += 1
        acertos = 0
        if p1 == "Diafragma": acertos += 1
        if p2 == "Pessoa com Asma (obstrução)": acertos += 1
        if p3 == "Gás Carbônico": acertos += 1
        
        if acertos == 3:
            st.session_state.quiz_acertos_totais += 1
            st.toast('Nota Máxima!', icon='💯')
            st.success("🎉 Sensacional! Você gabaritou o nosso teste!")
            st.balloons()
            st.session_state['aprovado'] = True
        else:
            st.error(f"Você acertou {acertos} de 3. Tente de novo! Dica: Lembre do nosso painel e do pulmão de garrafa PET.")
            st.session_state['aprovado'] = False

    if st.session_state.get('aprovado', False):
        st.write("---")
        nome_visitante = st.text_input("Gere seu Certificado! Digite seu nome:")
        if nome_visitante:
            st.markdown(f"""
            <div class='certificado'>
                <h2 style='color: #2e3b4e;'>🔬 Certificado de Cientista Honorário 🔬</h2>
                <p style='color: #666;'>Certificamos com orgulho que</p>
                <h1 style='color: #1CAAD9; margin: 15px 0;'><b>{nome_visitante.upper()}</b></h1>
                <p style='color: #555; font-size: 18px;'>Gabaritou a prova e concluiu o estudo sobre o Sistema Respiratório!</p>
                <br><p style='color: #888; font-style: italic;'>Equipe Respiração do Futuro</p>
            </div>
            """, unsafe_allow_html=True)

# --- DASHBOARD DA FEIRA (ÁREA RESTRITA) ---
elif pagina == "📊 Dashboard da Feira":
    st.markdown("<div class='texto-respirando'>🔒 Painel do Pesquisador</div>", unsafe_allow_html=True)
    st.write("Painel de telemetria restrito aos cientistas da equipe.")
    
    # Campo de senha mascarado
    senha = st.text_input("Insira a credencial de acesso:", type="password")
    
    if senha == "ciencia2026": # Você pode mudar essa senha se quiser
        st.success("✅ Acesso Liberado! Bem-vinda, equipe.")
        st.write("---")
        
        st.title("📈 Central de Pesquisa Ao Vivo")
        
        total_diag = st.session_state.diag_saudavel + st.session_state.diag_asma + st.session_state.diag_gripe
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Diagnósticos Totais", total_diag)
        col2.metric("Certificados Emitidos", st.session_state.quiz_acertos_totais)
        col3.metric("Tentativas no Quiz", st.session_state.quiz_tentativas)
        
        st.write("---")
        
        if total_diag > 0:
            st.subheader("Distribuição de Saúde dos Visitantes")
            
            dados_pizza = pd.DataFrame({
                "Condição": ["Saudáveis", "Asma/Obstrução", "Gripe/Infecção"],
                "Quantidade": [st.session_state.diag_saudavel, st.session_state.diag_asma, st.session_state.diag_gripe]
            })
            
            fig_pie = px.pie(
                dados_pizza, 
                values='Quantidade', 
                names='Condição', 
                hole=0.4, 
                color='Condição',
                color_discrete_map={
                    "Saudáveis": "#2ecc71", 
                    "Asma/Obstrução": "#e74c3c", 
                    "Gripe/Infecção": "#f1c40f"
                }
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20))
            
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("O gráfico interativo aparecerá aqui assim que o primeiro diagnóstico for realizado na aba 4!")
            
    elif senha != "":
        st.error("❌ Acesso Negado! Credencial incorreta.")
