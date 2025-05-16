from typing import Dict, Optional, Any, List
import streamlit as st
from google import genai
from google.genai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv


load_dotenv()


def load_css(file_name: str) -> None:
    """
    Carrega um arquivo CSS externo para estilizar o aplicativo Streamlit.

    Args:
        file_name (str): O nome do arquivo CSS (e.g., "style.css").
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo CSS '{file_name}' não encontrado. Verifique o caminho.")
    except Exception as e:
        st.error(f"Erro ao carregar CSS '{file_name}': {e}")


def load_prompt_template(file_path: str = "prompt.md") -> Optional[str]:
    """
    Carrega o template do prompt de um arquivo de texto.

    Args:
        file_path (str): O caminho para o arquivo do prompt.

    Returns:
        Optional[str]: O conteúdo do prompt como string, ou None se o arquivo não for encontrado.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(
            f"Arquivo de prompt '{file_path}' não encontrado. Verifique o caminho."
        )
        return None
    except Exception as e:
        st.error(f"Erro ao carregar prompt de '{file_path}': {e}")
        return None


def generate_mentorship_plan_with_gemini(
    user_inputs: Dict[str, Any]
) -> Optional[str]:
    """
    Gera um plano de mentoria usando o modelo Gemini do Google AI.

    Args:
        user_inputs (Dict[str, Any]): Um dicionário contendo os inputs do usuário.

    Returns:
        Optional[str]: O plano de mentoria gerado como texto, ou None em caso de erro.
    """

    system_instruction = load_prompt_template()

    if not system_instruction:
        st.error(
            "Template do prompt não pôde ser carregado. Verifique o arquivo 'prompt.md'."
        )
        return None

    try:
        client = genai.Client()

        safety_settings_config: List[Dict[str, Any]] = [
            {
                "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        ]

        # Constrói a string de dados do usuário para inclusão no prompt
        user_data_string_parts = [
            f"1.  **Nome:** {user_inputs.get('nome', 'N/A')}",
            f"2.  **Nível de Experiência Atual:** {user_inputs.get('experiencia', 'N/A')}",
            f"3.  **Área de Interesse Principal em Tech:** {user_inputs.get('area_interesse', 'N/A')}",
            f"4.  **Cargo/Vaga Desejada Específica:** {user_inputs.get('cargo_desejado', 'N/A')}",
            f"5.  **Skills Técnicas Atuais (Hard Skills):** {user_inputs.get('skills_tecnicas', 'N/A')}",
            f"6.  **Tempo Disponível para Estudos (semanal):** {user_inputs.get('tempo_estudo', 'N/A')} horas",
            f"7.  **Localização de Preferência (ou remoto):** {user_inputs.get('localizacao', 'N/A')}",
        ]
        user_data_string = (
            "Aqui estão os dados do usuário para quem você, Laura, irá gerar o plano de mentoria:\n\n"
            + "\n".join(user_data_string_parts)
            + "\n---\n"
        )

        content = [{"role": "user", "parts": [{"text": user_data_string}]}]

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=content,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=1,
                safety_settings=safety_settings_config,
                top_p=0.9,
                seed=42,
                max_output_tokens=7000
            ),
        )

        return response.text
    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o plano com o Gemini: {e}")
        return None
