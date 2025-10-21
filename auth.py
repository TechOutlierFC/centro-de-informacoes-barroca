import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as components
import yaml
from yaml.loader import SafeLoader

def get_authenticator():
    """
    Retorna o objeto authenticator configurado.
    Usa cache no session_state para manter a instância entre páginas.
    """
    
    # Verifica se já existe um authenticator no session_state
    if 'authenticator' in st.session_state:
        return st.session_state['authenticator']
    
    # Tenta carregar do Streamlit Secrets (recomendado para produção)
    if "credentials" in st.secrets:
        # Converte Secrets para dicionário mutável recursivamente
        config = {
            'credentials': {
                'usernames': {
                    username: dict(user_data)
                    for username, user_data in st.secrets["credentials"]["credentials"]["usernames"].items()
                }
            },
            'cookie': dict(st.secrets["credentials"]["cookie"])
        }
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    # Armazena no session_state para reutilizar
    st.session_state['authenticator'] = authenticator
    
    return authenticator