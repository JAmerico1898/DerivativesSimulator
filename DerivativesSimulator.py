"""
Laboratório de Derivativos - Main Hub
Ferramenta de Ensino de Derivativos - COPPEAD/UFRJ

Hub principal que coordena todos os módulos do aplicativo.
"""

import streamlit as st

# Import all modules
import modulo_1_introducao
import modulo_2_termos
import modulo_3_futuros
import modulo_4_swaps
import modulo_5_opcoes
import modulo_6_derivativos_embutidos


# Page configuration
st.set_page_config(
    page_title="Laboratório de Derivativos | COPPEAD",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for the entire application
MAIN_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.3; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        font-weight: 400;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .main-header .institution {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        font-weight: 300;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Module cards grid */
    .modules-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        padding: 1rem 0;
    }
    
    @media (max-width: 1200px) {
        .modules-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 768px) {
        .modules-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Module card styling */
    .module-card {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0,0,0,0.05);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .module-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--card-color-start), var(--card-color-end));
    }
    
    .module-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .module-card .icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .module-card .title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    
    .module-card .description {
        font-size: 0.9rem;
        color: #666;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .module-card .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        background: linear-gradient(90deg, var(--card-color-start), var(--card-color-end));
        color: white;
    }
    
    /* Card color variations */
    .card-intro { --card-color-start: #667eea; --card-color-end: #764ba2; }
    .card-termos { --card-color-start: #f093fb; --card-color-end: #f5576c; }
    .card-futuros { --card-color-start: #4facfe; --card-color-end: #00f2fe; }
    .card-swaps { --card-color-start: #43e97b; --card-color-end: #38f9d7; }
    .card-opcoes { --card-color-start: #fa709a; --card-color-end: #fee140; }
    .card-embutidos { --card-color-start: #a18cd1; --card-color-end: #fbc2eb; }
    
    /* Sidebar button styling */
    .sidebar-btn {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.875rem 1rem;
        margin: 0.25rem 0;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        color: white;
        font-size: 0.95rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }
    
    .sidebar-btn:hover {
        background: rgba(255,255,255,0.15);
        border-color: rgba(255,255,255,0.2);
        transform: translateX(4px);
    }
    
    .sidebar-btn.active {
        background: linear-gradient(90deg, rgba(102,126,234,0.4), rgba(118,75,162,0.4));
        border-color: rgba(102,126,234,0.5);
    }
    
    .sidebar-btn .icon {
        font-size: 1.25rem;
    }
    
    /* Home button special styling */
    .home-btn {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border: none;
        font-weight: 600;
    }
    
    .home-btn:hover {
        background: linear-gradient(90deg, #764ba2, #667eea);
        transform: translateX(4px);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(0,0,0,0.1);
        color: #666;
        font-size: 0.85rem;
    }
    
    .footer a {
        color: #667eea;
        text-decoration: none;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Streamlit button overrides for sidebar */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.15);
        border-color: rgba(255,255,255,0.2);
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Welcome text styling */
    .welcome-text {
        text-align: center;
        max-width: 800px;
        margin: 0 auto 2rem auto;
        color: #444;
        font-size: 1.05rem;
        line-height: 1.7;
    }
</style>
"""

# Module information for cards and navigation
MODULES = {
    "home": {
        "icon": "🏠",
        "title": "Início",
        "description": "Página inicial do laboratório",
        "card_class": ""
    },
    "introducao": {
        "icon": "📚",
        "title": "Introdução",
        "description": "Quiz interativo sobre conceitos fundamentais de derivativos financeiros",
        "card_class": "card-intro",
        "tag": "Quiz"
    },
    "termos": {
        "icon": "💱",
        "title": "Contratos a Termo",
        "description": "Simulador de NDF (Non-Deliverable Forward) para operações de câmbio USD/BRL",
        "card_class": "card-termos",
        "tag": "Simulador"
    },
    "futuros": {
        "icon": "📈",
        "title": "Contratos Futuros",
        "description": "Simulador de contratos DI Futuro com cálculo de PU e análise de resultados",
        "card_class": "card-futuros",
        "tag": "Simulador"
    },
    "swaps": {
        "icon": "🔄",
        "title": "Swaps",
        "description": "Calculadora completa de operações de swap no mercado brasileiro",
        "card_class": "card-swaps",
        "tag": "Calculadora"
    },
    "opcoes": {
        "icon": "⚡",
        "title": "Opções",
        "description": "Ferramenta completa com simulador, estratégias e recursos educacionais",
        "card_class": "card-opcoes",
        "tag": "Completo"
    },
    "embutidos": {
        "icon": "🔗",
        "title": "Derivativos Embutidos",
        "description": "Visualização e análise de derivativos embutidos em produtos estruturados",
        "card_class": "card-embutidos",
        "tag": "Animações"
    }
}


def init_session_state():
    """Initialize session state variables."""
    if "current_module" not in st.session_state:
        st.session_state.current_module = "home"


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <div style="color: white; font-size: 1.1rem; font-weight: 600;">Laboratório de</div>
            <div style="color: white; font-size: 1.3rem; font-weight: 700;">Derivativos</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.25rem;">COPPEAD/UFRJ</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Home button
        if st.button("🏠  Início", key="nav_home", use_container_width=True):
            st.session_state.current_module = "home"
            st.rerun()
        
        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;'>Módulos</p>", unsafe_allow_html=True)
        
        # Module navigation buttons
        modules_nav = ["introducao", "termos", "futuros", "swaps", "opcoes", "embutidos"]
        
        for module_key in modules_nav:
            module = MODULES[module_key]
            button_label = f"{module['icon']}  {module['title']}"
            
            if st.button(button_label, key=f"nav_{module_key}", use_container_width=True):
                st.session_state.current_module = module_key
                st.rerun()
        
        # Footer info
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: rgba(255,255,255,0.5); font-size: 0.75rem; margin: 0;">
                Prof. José Américo
            </p>
            <p style="color: rgba(255,255,255,0.4); font-size: 0.7rem; margin: 0.25rem 0 0 0;">
                © 2025
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_home():
    """Render the home page with module cards."""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Laboratório de Derivativos</h1>
        <p class="subtitle">Ferramenta Interativa de Ensino de Derivativos Financeiros</p>
        <p class="institution">COPPEAD/UFRJ • Prof. José Américo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome text
    st.markdown("""
    <p class="welcome-text">
        Bem-vindo ao Laboratório de Derivativos! Esta plataforma oferece simuladores interativos, 
        calculadoras e recursos educacionais para o estudo de derivativos financeiros. 
        Selecione um módulo abaixo para começar sua jornada de aprendizado.
    </p>
    """, unsafe_allow_html=True)
    
    # Section title
    st.markdown('<p class="section-title">📦 Módulos Disponíveis</p>', unsafe_allow_html=True)
    
    # Create module cards using columns
    modules_list = ["introducao", "termos", "futuros", "swaps", "opcoes", "embutidos"]
    
    # First row - 3 cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_module_card("introducao")
    
    with col2:
        render_module_card("termos")
    
    with col3:
        render_module_card("futuros")
    
    # Second row - 3 cards
    col4, col5, col6 = st.columns(3)
    
    with col4:
        render_module_card("swaps")
    
    with col5:
        render_module_card("opcoes")
    
    with col6:
        render_module_card("embutidos")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Laboratório de Derivativos | COPPEAD/UFRJ</p>
        <p>Desenvolvido para fins educacionais. Operações reais envolvem complexidades adicionais.</p>
    </div>
    """, unsafe_allow_html=True)


def render_module_card(module_key):
    """Render a single module card."""
    module = MODULES[module_key]
    
    st.markdown(f"""
    <div class="module-card {module['card_class']}" onclick="document.getElementById('btn_{module_key}').click()">
        <div class="icon">{module['icon']}</div>
        <div class="title">{module['title']}</div>
        <div class="description">{module['description']}</div>
        <span class="tag">{module.get('tag', 'Módulo')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button that will be triggered by card click
    if st.button(f"Acessar {module['title']}", key=f"btn_{module_key}", use_container_width=True):
        st.session_state.current_module = module_key
        st.rerun()


def render_module_header(module_key):
    """Render a header for the current module."""
    module = MODULES[module_key]
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid #f0f0f0;">
        <span style="font-size: 2.5rem;">{module['icon']}</span>
        <div>
            <h1 style="margin: 0; font-size: 1.8rem; color: #1a1a2e;">{module['title']}</h1>
            <p style="margin: 0; color: #666; font-size: 0.95rem;">{module['description']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""
    # Apply custom CSS
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate module
    current = st.session_state.current_module
    
    if current == "home":
        render_home()
    
    elif current == "introducao":
        render_module_header("introducao")
        modulo_1_introducao.render()
    
    elif current == "termos":
        render_module_header("termos")
        modulo_2_termos.render()
    
    elif current == "futuros":
        render_module_header("futuros")
        modulo_3_futuros.render()
    
    elif current == "swaps":
        render_module_header("swaps")
        modulo_4_swaps.render()
    
    elif current == "opcoes":
        render_module_header("opcoes")
        modulo_5_opcoes.render()
    
    elif current == "embutidos":
        render_module_header("embutidos")
        modulo_6_derivativos_embutidos.render()


if __name__ == "__main__":
    main()