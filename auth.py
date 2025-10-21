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


def check_authentication():
    """
    Verifica se o usuário está autenticado.
    Retorna True se autenticado, False caso contrário.
    """
    authenticator = get_authenticator()
    
    # Primeiro verifica se já está autenticado
    if st.session_state.get('authentication_status') == True:
        return True
    
    # Se não está autenticado, mostra tela de login customizada
    # CSS customizado para a tela de login
    login_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');
            
            /* Remove scroll da página inteira */
            html, body {
                overflow: hidden !important;
                height: 100vh !important;
                max-height: 100vh !important;
            }
            
            [data-testid="stAppViewContainer"], .main {
                overflow: hidden !important;
                height: 100vh !important;
                max-height: 100vh !important;
            }
            
            /* Esconde TUDO do Streamlit na tela de login */
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            [data-testid="stSidebar"] {display: none !important;}
            [data-testid="stToolbar"] {display: none !important;}
            [data-testid="stDecoration"] {display: none !important;}
            button[title="View fullscreen"] {display: none !important;}
            .stDeployButton {display: none !important;}
            
            /* Título dentro do formulário */
            [data-testid="stForm"]::before {
                content: "🔐 LOGIN";
                display: block;
                font-family: 'Anton', sans-serif;
                font-size: 2rem;
                text-align: center;
                text-transform: uppercase;
                color: #202020;
                margin-bottom: 0 !important;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #FABB48;
            }
            
            /* Esconde o título "Login" padrão do streamlit-authenticator */
            [data-testid="stForm"] h3,
            [data-testid="stForm"] h2,
            [data-testid="stForm"] h1,
            [data-testid="stForm"] [data-testid="stMarkdownContainer"] h3,
            [data-testid="stForm"] [data-testid="stMarkdownContainer"] h2,
            [data-testid="stForm"] [data-testid="stMarkdownContainer"] h1 {
                display: none !important;
            }
            
            /* Reduz espaço entre a barra divisória e o primeiro input */
            [data-testid="stForm"] > div:first-child,
            [data-testid="stForm"] > div:first-of-type {
                margin-top: 0.5rem !important;
                padding-top: 0 !important;
            }
            
            /* FORÇA todos os containers a terem mesma largura - abordagem super agressiva */
            [data-testid="stForm"] > div,
            [data-testid="stForm"] > div > div,
            [data-testid="stForm"] [data-testid="stTextInput"],
            [data-testid="stForm"] [data-testid="stTextInput"] > div,
            [data-testid="stForm"] [data-testid="stTextInput"] > div > div,
            [data-testid="stForm"] div[data-baseweb="form-control-container"],
            [data-testid="stForm"] div[data-baseweb="form-control-container"] > div,
            [data-testid="stForm"] div[data-baseweb="input"],
            [data-testid="stForm"] div[data-baseweb="base-input"],
            [data-testid="stForm"] label + div {
                width: 100% !important;
                max-width: 100% !important;
                min-width: 100% !important;
                flex: 1 1 100% !important;
            }
            
            /* Remove margens e paddings dos containers de input */
            [data-testid="stForm"] [data-testid="stTextInput"],
            [data-testid="stForm"] [data-testid="stTextInput"] > div,
            [data-testid="stForm"] div[data-baseweb="form-control-container"],
            [data-testid="stForm"] div[data-baseweb="form-control-container"] > div,
            [data-testid="stForm"] div[data-baseweb="input"],
            [data-testid="stForm"] div[data-baseweb="input"] > div,
            [data-testid="stForm"] div[data-baseweb="base-input"],
            [data-testid="stForm"] div[data-baseweb="base-input"] > div {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* Estiliza os inputs - MUITO ESPECÍFICO */
            [data-testid="stForm"] input[type="text"] {
                color: #000000 !important;
                -webkit-text-fill-color: #000000 !important;
                background-color: #ffffff !important;
                border: 2px solid #e0e0e0 !important;
                border-radius: 8px !important;
                padding: 0.75rem !important;
                font-size: 16px !important;
                width: 100% !important;
                min-width: 100% !important;
                max-width: 100% !important;
                box-sizing: border-box !important;
                margin: 0 !important;
            }
            
            /* Input de senha com espaço para o ícone - MESMA largura que username */
            [data-testid="stForm"] input[type="password"] {
                color: #000000 !important;
                -webkit-text-fill-color: #000000 !important;
                background-color: #ffffff !important;
                border: 2px solid #e0e0e0 !important;
                border-radius: 8px !important;
                padding: 0.75rem !important;
                padding-right: 3rem !important; /* Espaço para o olhinho */
                font-size: 16px !important;
                width: 100% !important;
                min-width: 100% !important;
                max-width: 100% !important;
                box-sizing: border-box !important;
                margin: 0 !important;
            }
            
            [data-testid="stForm"] input::placeholder {
                color: #666666 !important;
                -webkit-text-fill-color: #666666 !important;
                opacity: 1 !important;
            }
            
            [data-testid="stForm"] input:focus {
                border-color: #FABB48 !important;
                outline: none !important;
                box-shadow: 0 0 0 2px rgba(250, 187, 72, 0.2) !important;
            }
            
            /* ÍCONE DO OLHINHO - Seletores múltiplos para garantir */
            [data-testid="stForm"] button[kind="icon"],
            [data-testid="stForm"] button[kind="iconButton"],
            [data-testid="stForm"] button[data-baseweb="button"][kind="icon"],
            [data-testid="stForm"] div[data-baseweb="base-input"] button {
                position: absolute !important;
                right: 0.5rem !important;
                top: 50% !important;
                transform: translateY(-50%) !important;
                background-color: transparent !important;
                border: none !important;
                padding: 0.25rem !important;
                width: 2rem !important;
                height: 2rem !important;
                min-width: 2rem !important;
                min-height: 2rem !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                cursor: pointer !important;
                z-index: 100 !important;
                opacity: 1 !important;
                visibility: visible !important;
            }
            
            /* SVG do olhinho - forçar visibilidade */
            [data-testid="stForm"] button[kind="icon"] svg,
            [data-testid="stForm"] button[kind="iconButton"] svg,
            [data-testid="stForm"] div[data-baseweb="base-input"] button svg {
                width: 1.25rem !important;
                height: 1.25rem !important;
                color: #666666 !important;
                opacity: 1 !important;
                visibility: visible !important;
                display: block !important;
            }
            
            /* Paths do SVG - CRUCIAL para visibilidade */
            [data-testid="stForm"] button[kind="icon"] svg path,
            [data-testid="stForm"] button[kind="iconButton"] svg path,
            [data-testid="stForm"] div[data-baseweb="base-input"] button svg path {
                stroke: #666666 !important;
                fill: none !important;
                stroke-width: 2 !important;
                opacity: 1 !important;
                visibility: visible !important;
            }
            
            /* Hover do ícone */
            [data-testid="stForm"] button[kind="icon"]:hover,
            [data-testid="stForm"] button[kind="iconButton"]:hover,
            [data-testid="stForm"] div[data-baseweb="base-input"] button:hover {
                background-color: #f0f0f0 !important;
                border-radius: 4px !important;
            }
            
            [data-testid="stForm"] button[kind="icon"]:hover svg path,
            [data-testid="stForm"] button[kind="iconButton"]:hover svg path,
            [data-testid="stForm"] div[data-baseweb="base-input"] button:hover svg path {
                stroke: #202020 !important;
            }
            
            /* Container do input de senha - RELATIVO */
            [data-testid="stForm"] div[data-baseweb="base-input"],
            [data-testid="stForm"] div[data-baseweb="input"] {
                position: relative !important;
            }
            
            /* Estiliza os labels */
            [data-testid="stForm"] label {
                color: #202020 !important;
                font-weight: 600 !important;
                margin-bottom: 0.5rem !important;
                font-size: 14px !important;
            }
            
            /* Estiliza o botão de login */
            [data-testid="stForm"] button[kind="secondaryFormSubmit"],
            [data-testid="stForm"] button[type="submit"] {
                background-color: #FABB48 !important;
                color: #202020 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.75rem 2rem !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                width: 100% !important;
                margin-top: 1rem !important;
                margin-bottom: 2.5rem !important;
                transition: all 0.2s ease-in-out !important;
            }
            
            [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover,
            [data-testid="stForm"] button[type="submit"]:hover {
                background-color: #e6a940 !important;
                transform: scale(1.02) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
            }
            
            /* Reduz espaçamento vertical */
            [data-testid="stForm"] [data-testid="stVerticalBlock"] > div {
                gap: 0.5rem !important;
            }
            
            /* Reduz espaço específico do primeiro elemento após o título */
            [data-testid="stForm"] > div:first-of-type {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* Container principal mais compacto e sem scroll */
            .block-container {
                padding: 1rem !important;
                max-width: 500px !important;
                margin: 0 auto !important;
                height: 100vh !important;
                max-height: 100vh !important;
                overflow: hidden !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
                box-sizing: border-box !important;
            }
            
            /* Garante que o formulário não fique cortado */
            [data-testid="stForm"] {
                max-width: 400px;
                margin: 1rem auto;
                padding: 2rem 2rem 2.5rem 2rem !important;
                background: white;
                border-radius: 15px;
                box-shadow: 6px 6px 0px 0px #FABB48;
                border: 2px solid #FABB48;
                position: relative;
                box-sizing: border-box !important;
                max-height: 90vh;
                overflow: visible;
            }
            
            /* Reduz espaçamento da mensagem de info */
            [data-testid="stInfo"] {
                margin-bottom: 0.5rem !important;
            }
            </style>
            
            <script>
            // Flag para evitar múltiplas execuções
            let passwordIconFixed = false;
            
            // Força a visibilidade do ícone do olhinho após carregamento
            function forcePasswordIconVisibility() {
                if (passwordIconFixed) return; // Evita múltiplas execuções
                
                const form = document.querySelector('[data-testid="stForm"]');
                if (!form) {
                    // Se o formulário ainda não existe, tenta novamente depois
                    setTimeout(forcePasswordIconVisibility, 200);
                    return;
                }
                
                // Procura por todos os botões que podem ser o ícone (apenas dentro do form)
                const buttons = form.querySelectorAll('button[kind="icon"], button[kind="iconButton"]');
                
                if (buttons.length === 0) {
                    // Se não encontrou botões, tenta novamente depois
                    setTimeout(forcePasswordIconVisibility, 200);
                    return;
                }
                
                buttons.forEach(function(button) {
                    // Verifica se não é o botão de submit (ignora secondaryFormSubmit e submit)
                    const kind = button.getAttribute('kind');
                    const type = button.type;
                    if (kind !== 'secondaryFormSubmit' && type !== 'submit') {
                        // Aplica estilos diretamente via JavaScript (ícone do olhinho)
                        button.style.opacity = '1';
                        button.style.visibility = 'visible';
                        button.style.display = 'flex';
                        button.style.position = 'absolute';
                        button.style.right = '0.5rem';
                        button.style.zIndex = '100';
                        
                        // Força visibilidade do SVG e seus elementos
                        const svg = button.querySelector('svg');
                        if (svg) {
                            svg.style.opacity = '1';
                            svg.style.visibility = 'visible';
                            svg.style.display = 'block';
                            svg.style.color = '#666666';
                            
                            const paths = svg.querySelectorAll('path');
                            paths.forEach(function(path) {
                                path.style.opacity = '1';
                                path.style.visibility = 'visible';
                                path.style.stroke = '#666666';
                                path.style.strokeWidth = '2';
                                path.style.fill = 'none';
                            });
                        }
                    }
                });
                
                // Garante que o container do input de senha seja relativo e tenha 100% de largura
                const passwordInputs = form.querySelectorAll('input[type="password"]');
                passwordInputs.forEach(function(input) {
                    // Força largura no input
                    input.style.width = '100%';
                    input.style.minWidth = '100%';
                    input.style.maxWidth = '100%';
                    input.style.boxSizing = 'border-box';
                    input.style.margin = '0';
                    
                    // Força largura e remove padding em TODOS os containers parent
                    let parent = input.parentElement;
                    let levels = 0;
                    while (parent && levels < 5) { // Sobe até 5 níveis
                        parent.style.width = '100%';
                        parent.style.minWidth = '100%';
                        parent.style.maxWidth = '100%';
                        parent.style.margin = '0';
                        parent.style.padding = '0';
                        parent.style.boxSizing = 'border-box';
                        if (parent.hasAttribute('data-baseweb')) {
                            parent.style.position = 'relative';
                        }
                        parent = parent.parentElement;
                        levels++;
                        if (parent === form) break; // Para quando chegar no form
                    }
                });
                
                // Força largura igual no input de username também
                const usernameInputs = form.querySelectorAll('input[type="text"]');
                usernameInputs.forEach(function(input) {
                    // Força largura no input
                    input.style.width = '100%';
                    input.style.minWidth = '100%';
                    input.style.maxWidth = '100%';
                    input.style.boxSizing = 'border-box';
                    input.style.margin = '0';
                    
                    // Força largura e remove padding em TODOS os containers parent
                    let parent = input.parentElement;
                    let levels = 0;
                    while (parent && levels < 5) { // Sobe até 5 níveis
                        parent.style.width = '100%';
                        parent.style.minWidth = '100%';
                        parent.style.maxWidth = '100%';
                        parent.style.margin = '0';
                        parent.style.padding = '0';
                        parent.style.boxSizing = 'border-box';
                        parent = parent.parentElement;
                        levels++;
                        if (parent === form) break; // Para quando chegar no form
                    }
                });
                
                // Força estilos do botão de login
                const loginButton = form.querySelector('button[kind="primary"]');
                if (loginButton) {
                    loginButton.style.marginTop = '1rem';
                    loginButton.style.backgroundColor = '#FABB48';
                    
                    // Adiciona listener para o hover
                    loginButton.addEventListener('mouseenter', function() {
                        this.style.backgroundColor = '#e6a940';
                    });
                    loginButton.addEventListener('mouseleave', function() {
                        this.style.backgroundColor = '#FABB48';
                    });
                }
                
                // Marca como concluído
                passwordIconFixed = true;
            }
            
            // Executa quando o DOM estiver pronto
            setTimeout(forcePasswordIconVisibility, 100);
            setTimeout(forcePasswordIconVisibility, 500);
            setTimeout(forcePasswordIconVisibility, 1000);
            </script>
        """
    st.markdown(login_style, unsafe_allow_html=True)
    
    # Mensagem de boas-vindas ACIMA da caixa
    st.info('👋 Por favor, faça login para acessar o sistema')
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Renderiza o widget de login (título agora está dentro via CSS ::before)
    authenticator.login(location='main')
    
    # JavaScript que roda DEPOIS do formulário ser criado usando components.html
    components.html("""
            <script>
            (function() {
                // Função que aplica os estilos após o formulário existir
                function applyLoginStyles() {
                    const form = window.parent.document.querySelector('[data-testid="stForm"]');
                    if (!form) {
                        console.log('[AUTH] Form não encontrado, tentando novamente...');
                        setTimeout(applyLoginStyles, 100);
                        return;
                    }
                    
                    // DEBUG: Lista todos os botões no formulário
                    const allButtons = form.querySelectorAll('button');
                    console.log('[AUTH] 🔍 Total de botões encontrados:', allButtons.length);
                    allButtons.forEach((btn, index) => {
                        console.log(`[AUTH] Botão ${index}:`, {
                            tag: btn.tagName,
                            kind: btn.getAttribute('kind'),
                            type: btn.type,
                            class: btn.className,
                            text: btn.innerText,
                            html: btn.outerHTML.substring(0, 200)
                        });
                    });
                    
                    // Tenta diferentes seletores - o botão tem kind="secondaryFormSubmit"!
                    let loginButton = form.querySelector('button[kind="secondaryFormSubmit"]') ||
                                     form.querySelector('button[type="submit"]');
                    
                    if (loginButton) {
                        console.log('[AUTH] ✅ Botão de login encontrado! Aplicando estilos...');
                        loginButton.style.marginTop = '1rem';
                        loginButton.style.backgroundColor = '#FABB48';
                        
                        // Adiciona listeners SEM remover os existentes
                        loginButton.addEventListener('mouseenter', function() {
                            console.log('[AUTH] 🖱️ Mouse enter - mudando cor para #e6a940');
                            this.style.backgroundColor = '#e6a940';
                        });
                        loginButton.addEventListener('mouseleave', function() {
                            console.log('[AUTH] 🖱️ Mouse leave - voltando cor para #FABB48');
                            this.style.backgroundColor = '#FABB48';
                        });
                        
                        console.log('[AUTH] ✅ Estilos aplicados com sucesso!');
                    } else {
                        console.log('[AUTH] ❌ Botão não encontrado com nenhum seletor, tentando novamente...');
                        setTimeout(applyLoginStyles, 100);
                    }
                }
                
                // Executa imediatamente e tenta múltiplas vezes
                console.log('[AUTH] 🚀 Iniciando aplicação de estilos...');
                applyLoginStyles();
                setTimeout(applyLoginStyles, 200);
                setTimeout(applyLoginStyles, 500);
                setTimeout(applyLoginStyles, 1000);
                setTimeout(applyLoginStyles, 2000);
            })();
            </script>
        """, height=0)
    
    # Verifica novamente após tentar login
    authentication_status = st.session_state.get('authentication_status')
    
    if authentication_status == False:
        st.error('❌ Usuário ou senha incorretos')
        return False
    elif authentication_status == None:
        return False
    
    # Se autenticou com sucesso, retorna True
    return True

