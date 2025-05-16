from typing import Dict, Any, Optional
import streamlit as st
from utils import load_css, generate_mentorship_plan_with_gemini


# --- Configurações da Página ---
st.set_page_config(
    page_title="Laura - Sua Mentora de Carreira Tech",
    page_icon="👩‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Carregar Estilos CSS ---
# Crie um arquivo style.css vazio ou com seus estilos se necessário
try:
    load_css("style.css")  # Supondo que você tenha um style.css
except Exception:
    pass

# --- Conteúdo da Barra Lateral ---
with st.sidebar:
    try:
        st.image(
            "icon/icon2.png",  # Certifique-se que este arquivo está no local correto
            width=300,
        )
    except Exception:  # Caso o icon.png não exista
        st.warning("icon.png não encontrado.")

    st.subheader("Mentoria por IA")
    st.markdown(
        "Este é um conteúdo gerado por IA e serve como um guia inicial. "
        "Adapte-o à sua realidade e busque sempre aprofundar seus conhecimentos e networking!"
    )
    st.markdown("---")
    st.markdown("Desenvolvido com ❤️ usando Streamlit e Gemini.")

# --- Título e Introdução Principal ---
st.title("👩‍💻 Laura: Sua Mentora de Carreira Tech")
st.markdown(
    "Olá! Sou Laura, sua mentora virtual. Preencha os campos abaixo para que eu possa te ajudar a "
    "traçar um plano de carreira personalizado e alcançar seus objetivos no mundo da tecnologia."
)
st.markdown("---")

# --- Formulário de Coleta de Informações do Usuário ---
st.header("📝 Conte-me sobre você:")

with st.container(border=True):
    with st.form(key="mentorship_form"):
        col1, col2 = st.columns(2)

        with col1:
            nome: str = st.text_input("Seu Nome:", placeholder="Ex: Ana Silva")

            inner_col1_exp, inner_col1_area = st.columns(2)
            with inner_col1_exp:
                experiencia_opts: list[str] = [
                    "Iniciante",
                    "Júnior",
                    "Pleno",
                    "Sênior",
                    "Especialista",
                    "Transição de Carreira",
                ]
                experiencia: str = st.selectbox(
                    "Nível de Experiência:",
                    experiencia_opts,
                    help="Seu nível de experiência atual.",
                )

            with inner_col1_area:
                area_interesse: str = st.text_input(
                    "Área de Interesse:",
                    placeholder="Ex: Engenharia de Software",
                    help="Sua área de interesse principal em Tech.",
                )

            cargo_desejado: str = st.text_input(
                "Cargo/Vaga Desejada:",
                placeholder="Ex: Desenvolvedora Python Pleno",
                help="Qual cargo ou vaga específica você almeja?",
            )

        with col2:
            skills_tecnicas: str = st.text_area(
                "Principais Habilidades Técnicas Atuais (Hard Skills):",
                height=120,
                placeholder="Ex: Python, SQL, Git, React, Scrum, AWS S3, Docker",
            )

            # Criar colunas internas para tempo de estudo e localização
            inner_col2_tempo, inner_col2_local = st.columns(2)

            with inner_col2_tempo:
                tempo_estudo: int = st.number_input(
                    "Estudo (horas/semana):",
                    min_value=1,
                    max_value=60,
                    value=10,
                    step=1,
                    help="Tempo Disponível para Estudos (horas por semana).",
                )

            with inner_col2_local:
                localizacao: str = st.text_input(
                    "Preferência de vagas:",
                    placeholder="Ex: São Paulo, Remoto",
                    help="Localização de Preferência (ou 'Remoto').",
                )

        submit_button: bool = st.form_submit_button(
            label="✨ Gerar Plano de Mentoria Personalizado!"
        )

# --- Processamento e Exibição do Resultado ---
if submit_button:

    # Validação
    campos_faltando = []
    if not nome:
        campos_faltando.append("Nome")
    if not experiencia:
        campos_faltando.append("Nível de Experiência")
    if not area_interesse:
        campos_faltando.append(
            "Área de Interesse"
        )
    if not cargo_desejado:
        campos_faltando.append("Cargo/Vaga Desejada")
    if not skills_tecnicas:
        campos_faltando.append("Habilidades Técnicas")
    # tempo_estudo tem valor default
    if not localizacao:
        campos_faltando.append("Local Preferencial")

    if not area_interesse:
        st.warning("✏️ Por favor, especifique a 'Outra' área de interesse.")
    elif campos_faltando:
        st.warning(
            f"✏️ Por favor, preencha os seguintes campos obrigatórios: {', '.join(campos_faltando)}."
        )
    else:
        user_inputs: Dict[str, Any] = {
            "nome": nome,
            "experiencia": experiencia,
            "area_interesse": area_interesse,
            "cargo_desejado": cargo_desejado,
            "skills_tecnicas": skills_tecnicas,
            "tempo_estudo": tempo_estudo,
            "localizacao": localizacao,
        }

        with st.spinner(
            "Laura está preparando seu plano personalizado... Aguarde um momento! 🚀"
        ):
            mentorship_result: Optional[str] = generate_mentorship_plan_with_gemini(
                user_inputs
            )

        if mentorship_result:
            st.success("🎉 Seu plano de mentoria personalizado está pronto!")
            st.balloons()

            st.markdown("---")
            st.header(f"🎯 Seu Plano de Carreira Detalhado, {nome}!")
            st.markdown(mentorship_result, unsafe_allow_html=True)
        else:
            st.error(
                "😕 Desculpe, não foi possível gerar o plano de mentoria no momento. Verifique os dados ou tente novamente mais tarde."
            )
