"""
Módulo 5: Opções
Ferramenta interativa de ensino de opções com simulador e estratégias.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import norm


# Custom CSS for better styling
CUSTOM_CSS = """
<style>
.main {
    padding: 2rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    border-radius: 4px 4px 0px 0px;
    padding: 10px 16px;
    font-weight: 600;
}
h1, h2, h3 {
    padding-top: 1rem;
}
.highlight {
    background-color: #f0f2f6;
    padding: 1.5rem;
    border-radius: 0.5rem;
}
.small-text {
    font-size: 0.8rem;
}
</style>
"""


def black_scholes(S, K, T, r, sigma, option_type):
    """
    Calculate option price using Black-Scholes model.
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free interest rate (annual)
    sigma: Volatility
    option_type: 'call' or 'put'
    
    Returns:
    option_price: Price of the option
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return option_price


def option_payoff(S_T, K, option_type, position):
    """
    Calculate option payoff at expiration.
    
    Parameters:
    S_T: Stock price at expiration
    K: Strike price
    option_type: 'call' or 'put'
    position: 'buy' or 'sell'
    
    Returns:
    payoff: Payoff at expiration
    """
    if option_type == 'call':
        payoff = max(0, S_T - K)
    else:  # put
        payoff = max(0, K - S_T)
    
    if position == 'sell':
        payoff = -payoff
    
    return payoff


def option_profit(S_T, K, premium, option_type, position):
    """
    Calculate option profit at expiration.
    
    Parameters:
    S_T: Stock price at expiration
    K: Strike price
    premium: Option premium
    option_type: 'call' or 'put'
    position: 'buy' or 'sell'
    
    Returns:
    profit: Profit at expiration
    """
    payoff = option_payoff(S_T, K, option_type, position)
    
    if position == 'buy':
        profit = payoff - premium
    else:  # sell
        profit = premium + payoff
    
    return profit


def break_even_point(K, premium, option_type, position):
    """
    Calculate break-even point.
    
    Parameters:
    K: Strike price
    premium: Option premium
    option_type: 'call' or 'put'
    position: 'buy' or 'sell'
    
    Returns:
    break_even: Break-even point
    """
    if position == 'buy':
        if option_type == 'call':
            return K + premium
        else:  # put
            return K - premium
    else:  # sell
        if option_type == 'call':
            return K + premium
        else:  # put
            return K - premium


def render_introduction_tab():
    """Render the introduction tab content."""
    st.title("Ferramenta de Ensino de Opções")
    st.markdown("### Bem-vindo à Ferramenta Interativa de Ensino de Opções!")
    
    st.markdown("""
    Esta ferramenta foi desenvolvida para ajudá-lo a entender e visualizar estratégias com opções, incluindo:
    
    - **Opções Americanas vs Europeias**: Entenda as diferenças entre esses dois estilos de opções
    - **Calls vs Puts**: Aprenda como esses tipos de opções funcionam
    - **Compra vs Venda**: Visualize o payoff e o lucro para diferentes posições
    
    Use a aba do simulador para interagir com diferentes parâmetros de opções e ver como eles afetam a precificação e a lucratividade.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Opções Europeias vs Americanas")
        st.markdown("""
        - **Opções Europeias**: Só podem ser exercidas no vencimento
        - **Opções Americanas**: Podem ser exercidas a qualquer momento antes do vencimento
        
        Este simulador foca principalmente em opções europeias para simplificar o ensino dos conceitos fundamentais.
        """)
    
    with col2:
        st.markdown("### Calls vs Puts")
        st.markdown("""
        - **Opção de Compra (Call)**: Dá ao comprador o direito (mas não a obrigação) de comprar o ativo subjacente pelo preço de exercício
        - **Opção de Venda (Put)**: Dá ao comprador o direito (mas não a obrigação) de vender o ativo subjacente pelo preço de exercício
        """)
    
    st.markdown("### Compra vs Venda")
    st.markdown("""
    - **Compra de Opções (Posição Comprada/Long)**: 
    - Risco limitado (prêmio pago)
    - Lucro potencial ilimitado (para calls)
    - Lucro potencial limitado (para puts)
    
    - **Venda de Opções (Posição Vendida/Short)**:
    - Lucro potencial limitado (prêmio recebido)
    - Perda potencial ilimitada (para calls)
    - Perda potencial limitada (para puts)
    """)
    
    st.markdown("### Como Usar Esta Ferramenta")
    st.markdown("""
    1. Vá para a aba Simulador de Opções
    2. Selecione os parâmetros da sua opção
    3. Visualize os diagramas de payoff e lucro
    4. Ajuste os parâmetros para ver como eles afetam a avaliação da opção
    
    A ferramenta também fornecerá explicações educacionais baseadas nas suas seleções.
    """)


def render_simulator_tab():
    """Render the option simulator tab content."""
    st.title("Simulador de Opções")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parâmetros da Opção")
        
        # Option Type Selection
        option_style = st.radio(
            "Estilo da Opção", 
            ["Europeia", "Americana"], 
            index=0, 
            help="Opções europeias só podem ser exercidas no vencimento. Opções americanas podem ser exercidas a qualquer momento antes do vencimento.",
            key="opcoes_option_style"
        )
        
        position = st.radio(
            "Posição", 
            ["Compra", "Venda"], 
            index=0, 
            help="Comprar (long) ou Vender (short) a opção",
            key="opcoes_position"
        )
        
        option_type = st.radio(
            "Tipo de Opção", 
            ["Call", "Put"], 
            index=0, 
            help="Call dá direito de comprar. Put dá direito de vender.",
            key="opcoes_option_type"
        )
        
        # Market and Contract Parameters
        st.markdown("### Parâmetros de Mercado")
        
        S = st.slider(
            "Preço Atual do Ativo Subjacente (S)", 
            min_value=10.0, 
            max_value=200.0, 
            value=100.0, 
            step=1.0, 
            help="Preço de mercado atual do ativo subjacente",
            key="opcoes_S"
        )
        
        K = st.slider(
            "Preço de Exercício (K)", 
            min_value=10.0, 
            max_value=200.0, 
            value=100.0, 
            step=1.0, 
            help="O preço pelo qual a opção pode ser exercida",
            key="opcoes_K"
        )
        
        T = st.slider(
            "Tempo até o Vencimento (anos)", 
            min_value=0.1, 
            max_value=2.0, 
            value=1.0, 
            step=0.1, 
            help="Tempo até a opção expirar (em anos)",
            key="opcoes_T"
        )
        
        sigma = st.slider(
            "Volatilidade (σ, %)", 
            min_value=5.0, 
            max_value=100.0, 
            value=20.0, 
            step=5.0, 
            help="Volatilidade anualizada do ativo subjacente",
            key="opcoes_sigma"
        ) / 100
        
        r = st.slider(
            "Taxa de Juros Livre de Risco (r, %)", 
            min_value=0.0, 
            max_value=20.0, 
            value=10.0, 
            step=0.5, 
            help="Taxa de juros anual livre de risco",
            key="opcoes_r"
        ) / 100
        
        # Map Portuguese selections to English for calculations
        position_eng = "buy" if position == "Compra" else "sell"
        option_type_eng = option_type.lower()
        
        # Calculate option premium
        premium = black_scholes(S, K, T, r, sigma, option_type_eng)
        
        st.markdown("### Prêmio da Opção")
        st.markdown(f"#### R$ {premium:.2f}")
        
        if option_style == "Americana" and option_type == "Put" and K > S:
            st.warning("Nota: Para opções de venda americanas quando o preço de exercício > preço atual, o exercício antecipado pode ser ótimo. O modelo Black-Scholes pode subestimar o prêmio.")
    
    with col2:
        st.markdown("### Diagramas de Payoff e Lucro")
        
        # Generate price range for x-axis
        range_percent = 0.5
        price_min = max(1, K * (1 - range_percent))
        price_max = K * (1 + range_percent)
        
        # Create price array
        prices = np.linspace(price_min, price_max, 100)
        
        # Calculate payoffs and profits
        payoffs = [option_payoff(price, K, option_type_eng, position_eng) for price in prices]
        profits = [option_profit(price, K, premium, option_type_eng, position_eng) for price in prices]
        
        # Calculate break-even point
        be_point = break_even_point(K, premium, option_type_eng, position_eng)
        
        # Create DataFrame for displaying data
        df = pd.DataFrame({
            'Preço do Subjacente': prices,
            'Payoff': payoffs,
            'Lucro': profits
        })
        
        # Create payoff diagram using Plotly
        fig1 = go.Figure()
        
        fig1.add_trace(go.Scatter(
            x=prices,
            y=payoffs,
            mode='lines',
            name='Payoff',
            line=dict(color='blue', width=2)
        ))
        
        fig1.add_trace(go.Scatter(
            x=[K],
            y=[0],
            mode='markers',
            name='Preço de Exercício',
            marker=dict(color='red', size=10)
        ))
        
        fig1.update_layout(
            title=f"Diagrama de Payoff: {position} de {option_type}",
            xaxis_title="Preço do Subjacente no Vencimento",
            yaxis_title="Payoff",
            height=400,
            hovermode="x unified"
        )
        
        fig1.add_shape(
            type="line",
            x0=price_min,
            y0=0,
            x1=price_max,
            y1=0,
            line=dict(color="black", width=1, dash="dash")
        )
        
        # Create profit diagram using Plotly
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=prices,
            y=profits,
            mode='lines',
            name='Lucro',
            line=dict(color='green', width=2)
        ))
        
        fig2.add_trace(go.Scatter(
            x=[K],
            y=[option_profit(K, K, premium, option_type_eng, position_eng)],
            mode='markers',
            name='Preço de Exercício',
            marker=dict(color='red', size=10)
        ))
        
        fig2.add_trace(go.Scatter(
            x=[be_point],
            y=[0],
            mode='markers',
            name='Ponto de Equilíbrio',
            marker=dict(color='purple', size=10)
        ))
        
        fig2.update_layout(
            title=f"Diagrama de Lucro: {position} de {option_type}",
            xaxis_title="Preço do Subjacente no Vencimento",
            yaxis_title="Lucro",
            height=400,
            hovermode="x unified"
        )
        
        fig2.add_shape(
            type="line",
            x0=price_min,
            y0=0,
            x1=price_max,
            y1=0,
            line=dict(color="black", width=1, dash="dash")
        )
        
        # Display charts
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        
    # Display explanation
    st.markdown("### Explicação")
    
    st.markdown(f"""
    #### Explicação da {position} de {option_type}
    
    - **Prêmio**: R$ {premium:.2f}
    - **Ponto de Equilíbrio (Break-Even)**: R$ {be_point:.2f}
    """)
    
    if option_type == "Call":
        if position == "Compra":
            st.markdown("""
            **Explicação da Estratégia:**
            - Você está pagando um prêmio pelo direito de comprar o ativo subjacente pelo preço de exercício
            - Lucro quando o preço do subjacente sobe acima do preço de exercício mais o prêmio
            - Risco máximo é limitado ao prêmio pago
            - Lucro máximo é teoricamente ilimitado (pois o preço da ação pode subir indefinidamente)
            """)
        else:  # Venda
            st.markdown("""
            **Explicação da Estratégia:**
            - Você está recebendo um prêmio pela obrigação de vender o ativo subjacente pelo preço de exercício
            - Lucro quando o preço do subjacente fica abaixo do preço de exercício mais o prêmio
            - Lucro máximo é limitado ao prêmio recebido
            - Risco máximo é teoricamente ilimitado (pois o preço da ação pode subir indefinidamente)
            """)
    else:  # Put
        if position == "Compra":
            st.markdown("""
            **Explicação da Estratégia:**
            - Você está pagando um prêmio pelo direito de vender o ativo subjacente pelo preço de exercício
            - Lucro quando o preço do subjacente cai abaixo do preço de exercício menos o prêmio
            - Risco máximo é limitado ao prêmio pago
            - Lucro máximo é limitado (pois o preço da ação só pode cair até zero)
            """)
        else:  # Venda
            st.markdown("""
            **Explicação da Estratégia:**
            - Você está recebendo um prêmio pela obrigação de comprar o ativo subjacente pelo preço de exercício
            - Lucro quando o preço do subjacente fica acima do preço de exercício menos o prêmio
            - Lucro máximo é limitado ao prêmio recebido
            - Risco máximo é limitado (pois o preço da ação só pode cair até zero)
            """)
    
    # Option Greeks Calculation
    st.markdown("### Gregas das Opções")
    
    # Calculate d1 and d2 for Greeks
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Calculate Delta
    if option_type == "Call":
        delta = norm.cdf(d1)
    else:  # Put
        delta = norm.cdf(d1) - 1
    
    # Calculate Gamma
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Calculate Theta (time decay)
    if option_type == "Call":
        theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:  # Put
        theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    theta = theta / 365  # convert to daily
    
    # Calculate Vega
    vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # for 1% change in volatility
    
    if position == "Venda":
        delta = -delta
        gamma = -gamma
        theta = -theta
        vega = -vega
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Delta", f"{delta:.4f}")
        st.caption("Variação no preço da opção para R$1 de variação no subjacente")
    
    with col2:
        st.metric("Gamma", f"{gamma:.4f}")
        st.caption("Taxa de variação do Delta para R$1 de variação no subjacente")
    
    with col3:
        st.metric("Theta", f"{theta:.4f}")
        st.caption("Decaimento temporal diário (variação no preço da opção com a passagem do tempo)")
    
    with col4:
        st.metric("Vega", f"{vega:.4f}")
        st.caption("Variação no preço da opção para 1% de variação na volatilidade")


def render_strategies_tab():
    """Render the option strategies tab content."""
    st.title("Estratégias com Opções")
    
    st.markdown("""
    ### Explore Estratégias de Opções Baseadas na Perspectiva de Mercado
    
    Estratégias com opções podem ser adaptadas para diferentes expectativas de mercado. Selecione sua 
    perspectiva de mercado e explore estratégias adequadas para esse cenário.
    """)
    
    # Market outlook selection
    market_outlook = st.selectbox(
        "Selecione Sua Perspectiva de Mercado",
        [
            "Altista (Esperando que os preços subam significativamente)",
            "Levemente Altista (Esperando movimento moderado de alta)",
            "Baixista (Esperando que os preços caiam significativamente)",
            "Levemente Baixista (Esperando movimento moderado de baixa)",
            "Neutro (Esperando que os preços fiquem em uma faixa)",
            "Volátil (Esperando grandes movimentos de preço em qualquer direção)",
            "Baixa Volatilidade (Esperando movimento mínimo de preço)"
        ],
        key="opcoes_market_outlook"
    )
    
    # Dictionary mapping market outlooks to suitable strategies
    strategy_map = {
        "Altista (Esperando que os preços subam significativamente)": [
            "Compra de Call (Long Call)", 
            "Trava de Alta com Calls (Bull Call Spread)",
            "Reversão de Risco (Compra Call, Vende Put)"
        ],
        "Levemente Altista (Esperando movimento moderado de alta)": [
            "Venda Coberta de Call (Covered Call)", 
            "Trava de Alta com Puts (Bull Put Spread)",
            "Spread Vertical de Call Comprado"
        ],
        "Baixista (Esperando que os preços caiam significativamente)": [
            "Compra de Put (Long Put)", 
            "Trava de Baixa com Puts (Bear Put Spread)",
            "Reversão de Risco (Compra Put, Vende Call)"
        ],
        "Levemente Baixista (Esperando movimento moderado de baixa)": [
            "Trava de Baixa com Calls (Bear Call Spread)", 
            "Venda Coberta de Put (Covered Put)",
            "Venda de Call (Short Call)"
        ],
        "Neutro (Esperando que os preços fiquem em uma faixa)": [
            "Condor de Ferro (Iron Condor)", 
            "Venda de Straddle (Short Straddle)",
            "Venda de Strangle (Short Strangle)",
            "Borboleta (Butterfly Spread)"
        ],
        "Volátil (Esperando grandes movimentos de preço em qualquer direção)": [
            "Compra de Straddle (Long Straddle)", 
            "Compra de Strangle (Long Strangle)",
            "Long Guts"
        ],
        "Baixa Volatilidade (Esperando movimento mínimo de preço)": [
            "Borboleta de Ferro (Iron Butterfly)", 
            "Venda de Straddle (Short Straddle)",
            "Spread de Calendário (Calendar Spread)"
        ]
    }
    
    # Strategy selection based on market outlook
    strategy_options = strategy_map[market_outlook]
    selected_strategy = st.selectbox("Selecione uma Estratégia", strategy_options, key="opcoes_selected_strategy")
    
    # Parameters for all strategies
    st.markdown("### Parâmetros da Estratégia")
    col1, col2 = st.columns(2)
    
    with col1:
        S = st.slider("Preço Atual do Ativo Subjacente (S)", min_value=10.0, max_value=200.0, value=100.0, step=1.0, key="opcoes_strat_S")
        sigma = st.slider("Volatilidade (σ, %)", min_value=5.0, max_value=100.0, value=20.0, step=5.0, key="opcoes_strat_sigma") / 100
    
    with col2:
        T = st.slider("Tempo até o Vencimento (anos)", min_value=0.1, max_value=2.0, value=1.0, step=0.1, key="opcoes_strat_T")
        r = st.slider("Taxa de Juros Livre de Risco (r, %)", min_value=0.0, max_value=20.0, value=10.0, step=0.5, key="opcoes_strat_r") / 100
    
    # Initialize variables for strategy calculations
    prices = np.array([])
    profits = []
    df = pd.DataFrame()
    
    # Strategy-specific parameters and functions
    if "Compra de Call" in selected_strategy or "Long Call" in selected_strategy:
        K_call = st.slider("Preço de Exercício da Call", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="opcoes_K_call_long")
        call_premium = black_scholes(S, K_call, T, r, sigma, "call")
        
        st.markdown(f"""
        ### Estratégia de Compra de Call (Long Call)
        
        **Descrição:** Compra de uma opção de compra, dando a você o direito de comprar o ativo subjacente pelo preço de exercício.
        
        **Parâmetros:**
        - Preço de Exercício da Call: R$ {K_call:.2f}
        - Prêmio da Call: R$ {call_premium:.2f}
        
        **Risco Máximo:** Limitado ao prêmio pago (R$ {call_premium:.2f})
        
        **Ganho Máximo:** Ilimitado (conforme o preço do subjacente sobe)
        
        **Ponto de Equilíbrio:** Preço de Exercício + Prêmio = R$ {K_call + call_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K_call * 0.5), K_call * 1.5, 100)
        payoffs = [max(0, price - K_call) for price in prices]
        profits = [max(0, price - K_call) - call_premium for price in prices]
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Payoff': payoffs, 'Lucro': profits})
        
    elif "Compra de Put" in selected_strategy or "Long Put" in selected_strategy:
        K_put = st.slider("Preço de Exercício da Put", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="opcoes_K_put_long")
        put_premium = black_scholes(S, K_put, T, r, sigma, "put")
        
        st.markdown(f"""
        ### Estratégia de Compra de Put (Long Put)
        
        **Descrição:** Compra de uma opção de venda, dando a você o direito de vender o ativo subjacente pelo preço de exercício.
        
        **Parâmetros:**
        - Preço de Exercício da Put: R$ {K_put:.2f}
        - Prêmio da Put: R$ {put_premium:.2f}
        
        **Risco Máximo:** Limitado ao prêmio pago (R$ {put_premium:.2f})
        
        **Ganho Máximo:** Limitado mas substancial (Preço de Exercício - Prêmio = R$ {K_put - put_premium:.2f})
        
        **Ponto de Equilíbrio:** Preço de Exercício - Prêmio = R$ {K_put - put_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K_put * 0.5), K_put * 1.5, 100)
        payoffs = [max(0, K_put - price) for price in prices]
        profits = [max(0, K_put - price) - put_premium for price in prices]
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Payoff': payoffs, 'Lucro': profits})
        
    elif "Venda de Call" in selected_strategy or "Short Call" in selected_strategy:
        K_call = st.slider("Preço de Exercício da Call", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="opcoes_K_call_short")
        call_premium = black_scholes(S, K_call, T, r, sigma, "call")
        
        st.markdown(f"""
        ### Estratégia de Venda de Call (Short Call)
        
        **Descrição:** Venda de uma opção de compra, obrigando você a vender o ativo subjacente pelo preço de exercício se a opção for exercida.
        
        **Parâmetros:**
        - Preço de Exercício da Call: R$ {K_call:.2f}
        - Prêmio Recebido da Call: R$ {call_premium:.2f}
        
        **Risco Máximo:** Ilimitado (conforme o preço do subjacente sobe)
        
        **Ganho Máximo:** Limitado ao prêmio recebido (R$ {call_premium:.2f})
        
        **Ponto de Equilíbrio:** Preço de Exercício + Prêmio = R$ {K_call + call_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K_call * 0.5), K_call * 1.5, 100)
        payoffs = [-max(0, price - K_call) for price in prices]
        profits = [call_premium - max(0, price - K_call) for price in prices]
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Payoff': payoffs, 'Lucro': profits})
        
    elif "Venda Coberta de Call" in selected_strategy or "Covered Call" in selected_strategy:
        K_call = st.slider("Preço de Exercício da Call", min_value=50.0, max_value=150.0, value=110.0, step=5.0, key="opcoes_K_call_covered")
        call_premium = black_scholes(S, K_call, T, r, sigma, "call")
        
        st.markdown(f"""
        ### Estratégia de Venda Coberta de Call (Covered Call)
        
        **Descrição:** Possuir o ativo subjacente e vender uma opção de compra sobre ele.
        
        **Parâmetros:**
        - Preço Atual da Ação: R$ {S:.2f}
        - Preço de Exercício da Call: R$ {K_call:.2f}
        - Prêmio Recebido da Call: R$ {call_premium:.2f}
        
        **Risco Máximo:** Substancial (Preço da Ação - Prêmio = R$ {S - call_premium:.2f}) se o preço da ação cair a zero
        
        **Ganho Máximo:** Limitado (Prêmio da Call + (Strike - Preço da Ação) = R$ {call_premium + (K_call - S):.2f})
        
        **Ponto de Equilíbrio:** Preço da Ação - Prêmio = R$ {S - call_premium:.2f}
        """)
        
        prices = np.linspace(max(1, S * 0.5), S * 1.5, 100)
        profits = []
        for price in prices:
            stock_profit = price - S
            call_profit = call_premium - max(0, price - K_call)
            total_profit = stock_profit + call_profit
            profits.append(total_profit)
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Lucro': profits})
        
    elif "Trava de Alta com Calls" in selected_strategy or "Bull Call Spread" in selected_strategy:
        K_long = st.slider("Preço de Exercício da Call Comprada", min_value=50.0, max_value=150.0, value=95.0, step=5.0, key="opcoes_K_long_bull")
        K_short = st.slider("Preço de Exercício da Call Vendida", min_value=K_long, max_value=150.0, value=110.0, step=5.0, key="opcoes_K_short_bull")
        
        long_premium = black_scholes(S, K_long, T, r, sigma, "call")
        short_premium = black_scholes(S, K_short, T, r, sigma, "call")
        net_premium = long_premium - short_premium
        
        st.markdown(f"""
        ### Estratégia de Trava de Alta com Calls (Bull Call Spread)
        
        **Descrição:** Comprar uma opção de compra com strike menor e vender uma opção de compra com strike maior.
        
        **Parâmetros:**
        - Preço de Exercício da Call Comprada: R$ {K_long:.2f} (Prêmio: R$ {long_premium:.2f})
        - Preço de Exercício da Call Vendida: R$ {K_short:.2f} (Prêmio: R$ {short_premium:.2f})
        - Prêmio Líquido Pago: R$ {net_premium:.2f}
        
        **Risco Máximo:** Limitado ao prêmio líquido pago (R$ {net_premium:.2f})
        
        **Ganho Máximo:** Limitado à diferença entre os strikes menos o prêmio líquido (R$ {K_short - K_long - net_premium:.2f})
        
        **Ponto de Equilíbrio:** Strike Menor + Prêmio Líquido = R$ {K_long + net_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K_long * 0.8), K_short * 1.2, 100)
        profits = []
        for price in prices:
            long_profit = max(0, price - K_long) - long_premium
            short_profit = short_premium - max(0, price - K_short)
            total_profit = long_profit + short_profit
            profits.append(total_profit)
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Lucro': profits})
        
    elif "Trava de Baixa com Puts" in selected_strategy or "Bear Put Spread" in selected_strategy:
        K_long = st.slider("Preço de Exercício da Put Comprada", min_value=50.0, max_value=150.0, value=110.0, step=5.0, key="opcoes_K_long_bear")
        K_short = st.slider("Preço de Exercício da Put Vendida", min_value=50.0, max_value=K_long, value=95.0, step=5.0, key="opcoes_K_short_bear")
        
        long_premium = black_scholes(S, K_long, T, r, sigma, "put")
        short_premium = black_scholes(S, K_short, T, r, sigma, "put")
        net_premium = long_premium - short_premium
        
        st.markdown(f"""
        ### Estratégia de Trava de Baixa com Puts (Bear Put Spread)
        
        **Descrição:** Comprar uma opção de venda com strike maior e vender uma opção de venda com strike menor.
        
        **Parâmetros:**
        - Preço de Exercício da Put Comprada: R$ {K_long:.2f} (Prêmio: R$ {long_premium:.2f})
        - Preço de Exercício da Put Vendida: R$ {K_short:.2f} (Prêmio: R$ {short_premium:.2f})
        - Prêmio Líquido Pago: R$ {net_premium:.2f}
        
        **Risco Máximo:** Limitado ao prêmio líquido pago (R$ {net_premium:.2f})
        
        **Ganho Máximo:** Limitado à diferença entre os strikes menos o prêmio líquido (R$ {K_long - K_short - net_premium:.2f})
        
        **Ponto de Equilíbrio:** Strike Maior - Prêmio Líquido = R$ {K_long - net_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K_short * 0.8), K_long * 1.2, 100)
        profits = []
        for price in prices:
            long_profit = max(0, K_long - price) - long_premium
            short_profit = short_premium - max(0, K_short - price)
            total_profit = long_profit + short_profit
            profits.append(total_profit)
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Lucro': profits})
        
    elif "Compra de Straddle" in selected_strategy or "Long Straddle" in selected_strategy:
        K = st.slider("Preço de Exercício", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="opcoes_K_straddle")
        
        call_premium = black_scholes(S, K, T, r, sigma, "call")
        put_premium = black_scholes(S, K, T, r, sigma, "put")
        total_premium = call_premium + put_premium
        
        st.markdown(f"""
        ### Estratégia de Compra de Straddle (Long Straddle)
        
        **Descrição:** Comprar tanto uma call quanto uma put no mesmo preço de exercício, lucrando com grandes movimentos de preço em qualquer direção.
        
        **Parâmetros:**
        - Preço de Exercício: R$ {K:.2f}
        - Prêmio da Call: R$ {call_premium:.2f}
        - Prêmio da Put: R$ {put_premium:.2f}
        - Prêmio Total: R$ {total_premium:.2f}
        
        **Risco Máximo:** Limitado ao prêmio total pago (R$ {total_premium:.2f})
        
        **Ganho Máximo:** Ilimitado (conforme o preço se afasta do strike em qualquer direção)
        
        **Pontos de Equilíbrio:** 
        - Para cima: Strike + Prêmio Total = R$ {K + total_premium:.2f}
        - Para baixo: Strike - Prêmio Total = R$ {K - total_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K * 0.5), K * 1.5, 100)
        profits = []
        for price in prices:
            call_profit = max(0, price - K) - call_premium
            put_profit = max(0, K - price) - put_premium
            total_profit = call_profit + put_profit
            profits.append(total_profit)
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Lucro': profits})
        
    elif "Condor de Ferro" in selected_strategy or "Iron Condor" in selected_strategy:
        col1, col2 = st.columns(2)
        
        with col1:
            K_put_long = st.slider("Strike da Put Comprada", min_value=50.0, max_value=90.0, value=80.0, step=5.0, key="opcoes_K_put_long_ic")
            K_put_short = st.slider("Strike da Put Vendida", min_value=K_put_long, max_value=100.0, value=90.0, step=5.0, key="opcoes_K_put_short_ic")
        
        with col2:
            K_call_short = st.slider("Strike da Call Vendida", min_value=K_put_short, max_value=150.0, value=110.0, step=5.0, key="opcoes_K_call_short_ic")
            K_call_long = st.slider("Strike da Call Comprada", min_value=K_call_short, max_value=150.0, value=120.0, step=5.0, key="opcoes_K_call_long_ic")
        
        put_long_premium = black_scholes(S, K_put_long, T, r, sigma, "put")
        put_short_premium = black_scholes(S, K_put_short, T, r, sigma, "put")
        call_short_premium = black_scholes(S, K_call_short, T, r, sigma, "call")
        call_long_premium = black_scholes(S, K_call_long, T, r, sigma, "call")
        
        net_premium = put_short_premium + call_short_premium - put_long_premium - call_long_premium
        max_profit = net_premium
        max_risk = (K_put_short - K_put_long) - net_premium
        
        st.markdown(f"""
        ### Estratégia Condor de Ferro (Iron Condor)
        
        **Descrição:** Uma estratégia neutra de mercado que lucra quando o preço do subjacente permanece dentro de uma faixa.
        
        **Parâmetros:**
        - Strike da Put Comprada: R$ {K_put_long:.2f} (Prêmio: R$ {put_long_premium:.2f})
        - Strike da Put Vendida: R$ {K_put_short:.2f} (Prêmio: R$ {put_short_premium:.2f})
        - Strike da Call Vendida: R$ {K_call_short:.2f} (Prêmio: R$ {call_short_premium:.2f})
        - Strike da Call Comprada: R$ {K_call_long:.2f} (Prêmio: R$ {call_long_premium:.2f})
        - Prêmio Líquido Recebido: R$ {net_premium:.2f}
        
        **Risco Máximo:** Limitado à largura de qualquer spread menos o prêmio líquido (R$ {max_risk:.2f})
        
        **Ganho Máximo:** Limitado ao prêmio líquido recebido (R$ {max_profit:.2f})
        
        **Pontos de Equilíbrio:** 
        - Inferior: Strike da Put Vendida - Prêmio Líquido = R$ {K_put_short - net_premium:.2f}
        - Superior: Strike da Call Vendida + Prêmio Líquido = R$ {K_call_short + net_premium:.2f}
        """)
        
        prices = np.linspace(max(1, K_put_long * 0.8), K_call_long * 1.2, 100)
        profits = []
        for price in prices:
            put_long_profit = max(0, K_put_long - price) - put_long_premium
            put_short_profit = put_short_premium - max(0, K_put_short - price)
            call_short_profit = call_short_premium - max(0, price - K_call_short)
            call_long_profit = max(0, price - K_call_long) - call_long_premium
            total_profit = put_long_profit + put_short_profit + call_short_profit + call_long_profit
            profits.append(total_profit)
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Lucro': profits})
    
    else:
        # Default case for strategies not yet implemented
        st.info("Esta estratégia será implementada em breve. Por favor, selecione outra estratégia.")
        prices = np.linspace(50, 150, 100)
        profits = [0] * 100
        df = pd.DataFrame({'Preço do Subjacente': prices, 'Lucro': profits})
    
    # Display chart for all strategies
    if len(profits) > 0:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Preço do Subjacente'] if 'Preço do Subjacente' in df.columns else df.iloc[:, 0],
            y=df['Lucro'],
            mode='lines',
            name='Lucro',
            line=dict(color='green', width=2)
        ))
        
        # Add zero line
        fig.add_shape(
            type="line",
            x0=min(prices),
            y0=0,
            x1=max(prices),
            y1=0,
            line=dict(color="black", width=1, dash="dash")
        )
        
        # Add current price marker
        fig.add_trace(go.Scatter(
            x=[S],
            y=[0],
            mode='markers',
            name='Preço Atual',
            marker=dict(color='blue', size=10)
        ))
        
        fig.update_layout(
            title=f"{selected_strategy} - Diagrama de Lucro/Prejuízo",
            xaxis_title="Preço do Subjacente no Vencimento",
            yaxis_title="Lucro/Prejuízo",
            height=500,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Strategy advantages and disadvantages
    render_strategy_analysis(selected_strategy)


def render_strategy_analysis(selected_strategy):
    """Render advantages, disadvantages, and guidance for the selected strategy."""
    st.markdown("### Vantagens e Desvantagens da Estratégia")
    
    advantages = {
        "Compra de Call (Long Call)": [
            "Potencial de lucro ilimitado conforme o preço sobe",
            "Risco limitado (prêmio pago)",
            "Alavancagem (controlar posição maior com menos capital)",
            "Sem risco de queda além do prêmio"
        ],
        "Compra de Put (Long Put)": [
            "Lucra com movimento de queda do preço",
            "Risco limitado (prêmio pago)",
            "Pode ser usado como seguro de carteira",
            "Alavancagem (controlar posição maior com menos capital)"
        ],
        "Venda de Call (Short Call)": [
            "Lucra com preços em queda, estáveis ou levemente em alta",
            "Prêmio recebido antecipadamente",
            "Pode ser usado para gerar renda em posições existentes",
            "Decaimento temporal trabalha a seu favor"
        ],
        "Venda Coberta de Call (Covered Call)": [
            "Gerar renda de posições de ações existentes",
            "Fornece alguma proteção contra queda (prêmio reduz custo base)",
            "Pode aumentar o rendimento geral da carteira",
            "Beneficia-se do decaimento temporal"
        ],
        "Trava de Alta com Calls (Bull Call Spread)": [
            "Custo menor do que comprar uma call diretamente",
            "Risco e recompensa definidos",
            "Ponto de equilíbrio menor que uma long call",
            "Lucrativo em mercados moderadamente altistas"
        ],
        "Trava de Baixa com Puts (Bear Put Spread)": [
            "Custo menor do que comprar uma put diretamente",
            "Risco e recompensa definidos",
            "Lucrativo em mercados moderadamente baixistas",
            "Put vendida ajuda a compensar custo da put comprada"
        ],
        "Compra de Straddle (Long Straddle)": [
            "Lucra com grandes movimentos em qualquer direção",
            "Risco limitado (prêmio total pago)",
            "Potencial de lucro ilimitado",
            "Bom para condições de mercado incertas ou antes de eventos importantes"
        ],
        "Condor de Ferro (Iron Condor)": [
            "Lucra em mercados laterais",
            "Prêmio recebido antecipadamente",
            "Risco e recompensa definidos",
            "Beneficia-se do decaimento temporal"
        ]
    }
    
    disadvantages = {
        "Compra de Call (Long Call)": [
            "Perde valor com o passar do tempo (decaimento temporal)",
            "Requer movimento significativo de preço para ser lucrativa",
            "Diminuição de volatilidade prejudica o valor da posição",
            "Pode expirar sem valor (100% de perda do prêmio)"
        ],
        "Compra de Put (Long Put)": [
            "Perde valor com o passar do tempo (decaimento temporal)",
            "Requer movimento significativo de preço para ser lucrativa",
            "Diminuição de volatilidade prejudica o valor da posição",
            "Pode expirar sem valor (100% de perda do prêmio)"
        ],
        "Venda de Call (Short Call)": [
            "Risco ilimitado se o preço subir acentuadamente",
            "Requer margem (garantia)",
            "Risco de exercício antecipado (para opções americanas)",
            "Aumento de volatilidade prejudica a posição"
        ],
        "Venda Coberta de Call (Covered Call)": [
            "Limita potencial de alta",
            "Proteção limitada contra queda",
            "Custo de oportunidade se a ação subir significativamente",
            "Ação ainda pode cair substancialmente"
        ],
        "Trava de Alta com Calls (Bull Call Spread)": [
            "Potencial de lucro limitado",
            "Requer aumento moderado de preço para ser lucrativa",
            "Decaimento temporal trabalha contra a posição",
            "Ambas as opções podem expirar sem valor"
        ],
        "Trava de Baixa com Puts (Bear Put Spread)": [
            "Potencial de lucro limitado",
            "Requer queda moderada de preço para ser lucrativa",
            "Decaimento temporal trabalha contra a posição",
            "Ambas as opções podem expirar sem valor"
        ],
        "Compra de Straddle (Long Straddle)": [
            "Estratégia cara (dois prêmios)",
            "Requer movimento significativo de preço em qualquer direção",
            "Sofre com decaimento temporal",
            "Diminuição de volatilidade prejudica o valor da posição"
        ],
        "Condor de Ferro (Iron Condor)": [
            "Potencial de lucro limitado",
            "Risco de perda significativa se o preço ultrapassar qualquer strike vendido",
            "Múltiplas pernas aumentam custos de transação",
            "Complexo de gerenciar"
        ]
    }
    
    # Map selected strategy to dictionary key
    strategy_key_map = {
        "Compra de Call (Long Call)": "Compra de Call (Long Call)",
        "Trava de Alta com Calls (Bull Call Spread)": "Trava de Alta com Calls (Bull Call Spread)",
        "Reversão de Risco (Compra Call, Vende Put)": "Compra de Call (Long Call)",
        "Venda Coberta de Call (Covered Call)": "Venda Coberta de Call (Covered Call)",
        "Trava de Alta com Puts (Bull Put Spread)": "Trava de Alta com Calls (Bull Call Spread)",
        "Spread Vertical de Call Comprado": "Trava de Alta com Calls (Bull Call Spread)",
        "Compra de Put (Long Put)": "Compra de Put (Long Put)",
        "Trava de Baixa com Puts (Bear Put Spread)": "Trava de Baixa com Puts (Bear Put Spread)",
        "Reversão de Risco (Compra Put, Vende Call)": "Compra de Put (Long Put)",
        "Trava de Baixa com Calls (Bear Call Spread)": "Trava de Baixa com Puts (Bear Put Spread)",
        "Venda Coberta de Put (Covered Put)": "Venda de Call (Short Call)",
        "Venda de Call (Short Call)": "Venda de Call (Short Call)",
        "Condor de Ferro (Iron Condor)": "Condor de Ferro (Iron Condor)",
        "Venda de Straddle (Short Straddle)": "Condor de Ferro (Iron Condor)",
        "Venda de Strangle (Short Strangle)": "Condor de Ferro (Iron Condor)",
        "Borboleta (Butterfly Spread)": "Condor de Ferro (Iron Condor)",
        "Compra de Straddle (Long Straddle)": "Compra de Straddle (Long Straddle)",
        "Compra de Strangle (Long Strangle)": "Compra de Straddle (Long Straddle)",
        "Long Guts": "Compra de Straddle (Long Straddle)",
        "Borboleta de Ferro (Iron Butterfly)": "Condor de Ferro (Iron Condor)",
        "Spread de Calendário (Calendar Spread)": "Condor de Ferro (Iron Condor)"
    }
    
    strategy_key = strategy_key_map.get(selected_strategy, selected_strategy)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Vantagens")
        for adv in advantages.get(strategy_key, ["Nenhuma vantagem específica listada"]):
            st.markdown(f"- {adv}")
    
    with col2:
        st.markdown("#### Desvantagens")
        for dis in disadvantages.get(strategy_key, ["Nenhuma desvantagem específica listada"]):
            st.markdown(f"- {dis}")
    
    # When to use this strategy
    st.markdown("### Quando Usar Esta Estratégia")
    
    when_to_use = {
        "Compra de Call (Long Call)": """
        - Quando você está fortemente altista sobre o ativo subjacente
        - Quando você espera um aumento significativo de preço
        - Quando você quer limitar o risco mantendo exposição à alta
        - Quando você quer alavancagem sem tomar dinheiro emprestado
        - Antes de eventos positivos antecipados (resultados, lançamento de produtos, etc.)
        """,
        "Compra de Put (Long Put)": """
        - Quando você está fortemente baixista sobre o ativo subjacente
        - Quando você espera uma queda significativa de preço
        - Quando você quer limitar o risco enquanto ganha com movimento de queda
        - Quando você quer proteger posições compradas existentes sem vendê-las
        - Antes de eventos negativos antecipados (resultados, fraqueza setorial, etc.)
        """,
        "Venda de Call (Short Call)": """
        - Quando você está neutro a levemente baixista sobre o subjacente
        - Quando você quer gerar renda com prêmio de opções
        - Quando você acredita que a volatilidade está superestimada
        - Quando você está disposto a vender ações (ou ficar vendido) no preço de exercício
        - Quando você espera que o decaimento temporal trabalhe a seu favor
        """,
        "Venda Coberta de Call (Covered Call)": """
        - Quando você já possui a ação subjacente
        - Quando você está neutro a levemente altista sobre a ação
        - Quando você quer gerar renda adicional das suas posições
        - Quando você está disposto a vender ações no preço de exercício
        - Em ambientes de baixa volatilidade onde você quer aumentar retornos
        """,
        "Trava de Alta com Calls (Bull Call Spread)": """
        - Quando você está moderadamente altista sobre o subjacente
        - Quando você quer reduzir o custo de comprar calls
        - Quando você está disposto a limitar seu potencial de alta para reduzir custo
        - Quando a volatilidade implícita está alta (tornando calls diretas caras)
        - Quando você quer risco e recompensa definidos
        """,
        "Trava de Baixa com Puts (Bear Put Spread)": """
        - Quando você está moderadamente baixista sobre o subjacente
        - Quando você quer reduzir o custo de comprar puts
        - Quando você está disposto a limitar seu potencial de lucro para reduzir custo
        - Quando a volatilidade implícita está alta (tornando puts diretas caras)
        - Quando você quer risco e recompensa definidos
        """,
        "Compra de Straddle (Long Straddle)": """
        - Quando você espera um grande movimento de preço mas está incerto sobre a direção
        - Antes de grandes eventos de notícias, anúncios de resultados ou lançamentos de produtos
        - Quando a volatilidade implícita está baixa (tornando a estratégia mais acessível)
        - Quando você antecipa um aumento na volatilidade
        - Quando você quer lucrar com uma saída de uma faixa de negociação
        """,
        "Condor de Ferro (Iron Condor)": """
        - Quando você espera que o subjacente permaneça dentro de uma faixa específica de preço
        - Quando a volatilidade implícita está alta (tornando as opções vendidas mais valiosas)
        - Quando você quer lucrar com o decaimento temporal
        - Em ambientes de baixa volatilidade onde os preços tendem a andar de lado
        - Quando você quer risco e recompensa definidos
        """
    }
    
    st.markdown(when_to_use.get(strategy_key, "Nenhuma orientação específica disponível para esta estratégia."))


def render_educational_tab():
    """Render the educational resources tab content."""
    st.title("Recursos Educacionais")
    
    st.markdown("""
    ### Quiz de Conceitos Básicos de Opções
    
    Teste seu entendimento sobre opções com este quiz rápido:
    """)
    
    q1 = st.radio(
        "1. Qual opção dá ao titular o direito de comprar o ativo subjacente?",
        ["Opção de Compra (Call)", "Opção de Venda (Put)", "Ambas", "Nenhuma"],
        index=None,
        key="opcoes_quiz_q1"
    )
    
    if q1:
        if q1 == "Opção de Compra (Call)":
            st.success("Correto! Uma opção de compra (call) dá ao titular o direito de comprar o ativo subjacente pelo preço de exercício.")
        else:
            st.error("Incorreto. Uma opção de compra (call) dá ao titular o direito de comprar o ativo subjacente pelo preço de exercício.")
    
    q2 = st.radio(
        "2. Qual é a perda máxima para um comprador de opção de compra (call)?",
        ["Ilimitada", "Preço de Exercício", "Prêmio Pago", "Preço de Exercício + Prêmio"],
        index=None,
        key="opcoes_quiz_q2"
    )
    
    if q2:
        if q2 == "Prêmio Pago":
            st.success("Correto! A perda máxima para um comprador de call é limitada ao prêmio pago.")
        else:
            st.error("Incorreto. A perda máxima para um comprador de call é limitada ao prêmio pago.")
    
    q3 = st.radio(
        "3. O que significa ter uma posição 'comprada' (long) em opções?",
        ["Você está esperando que o preço suba", "Você comprou a opção", "Você está segurando a opção por muito tempo", "Você vendeu a opção"],
        index=None,
        key="opcoes_quiz_q3"
    )
    
    if q3:
        if q3 == "Você comprou a opção":
            st.success("Correto! Ter uma posição 'comprada' (long) significa que você comprou a opção.")
        else:
            st.error("Incorreto. Ter uma posição 'comprada' (long) significa que você comprou a opção.")
    
    q4 = st.radio(
        "4. Qual estilo de opção só pode ser exercido no vencimento?",
        ["Opção Americana", "Opção Europeia", "Opção Asiática", "Opção Bermuda"],
        index=None,
        key="opcoes_quiz_q4"
    )
    
    if q4:
        if q4 == "Opção Europeia":
            st.success("Correto! Opções europeias só podem ser exercidas no vencimento.")
        else:
            st.error("Incorreto. Opções europeias só podem ser exercidas no vencimento.")
    
    q5 = st.radio(
        "5. Qual grega mede a sensibilidade de uma opção ao decaimento temporal?",
        ["Delta", "Gamma", "Theta", "Vega"],
        index=None,
        key="opcoes_quiz_q5"
    )
    
    if q5:
        if q5 == "Theta":
            st.success("Correto! Theta mede a taxa na qual uma opção perde valor com a passagem do tempo.")
        else:
            st.error("Incorreto. Theta mede a taxa na qual uma opção perde valor com a passagem do tempo.")
    
    # Additional resources
    st.markdown("""
    ### Recursos Adicionais
    
    #### Estratégias de Opções para Diferentes Condições de Mercado
    
    | Estratégia | Perspectiva de Mercado | Risco | Recompensa Potencial |
    | --- | --- | --- | --- |
    | Compra de Call | Altista | Limitado (Prêmio) | Ilimitado |
    | Compra de Put | Baixista | Limitado (Prêmio) | Limitado mas substancial |
    | Venda de Call | Neutro a Baixista | Ilimitado | Limitado (Prêmio) |
    | Venda de Put | Neutro a Altista | Limitado mas substancial | Limitado (Prêmio) |
    | Venda Coberta de Call | Levemente Altista | Substancial | Limitado |
    | Put Protetora | Altista com proteção de queda | Limitado | Ilimitado menos prêmio |
    | Trava de Alta com Calls | Moderadamente Altista | Limitado (Prêmio Líquido) | Limitado (Spread - Prêmio) |
    | Trava de Baixa com Puts | Moderadamente Baixista | Limitado (Prêmio Líquido) | Limitado (Spread - Prêmio) |
    | Compra de Straddle | Volátil (Qualquer Direção) | Limitado (Prêmio Total) | Ilimitado para cima, Limitado para baixo |
    | Condor de Ferro | Neutro (Lateral) | Limitado (Largura do spread - Prêmio) | Limitado (Prêmio) |
    
    #### Comparando Estratégias Básicas de Opções
    
    **Estratégias Direcionais:**
    - **Altista:** Compra de Call > Trava de Alta com Calls > Trava de Alta com Puts > Venda de Put
    - **Baixista:** Compra de Put > Trava de Baixa com Puts > Trava de Baixa com Calls > Venda de Call
    
    **Estratégias de Volatilidade:**
    - **Espera Alta Volatilidade:** Compra de Straddle > Compra de Strangle > Long Guts
    - **Espera Baixa Volatilidade:** Condor de Ferro > Venda de Straddle > Venda de Strangle > Borboleta
    
    **Estratégias de Gestão de Risco:**
    - **Proteger Ação Comprada:** Put Protetora > Collar > Married Put
    - **Aumentar Retornos:** Venda Coberta de Call > Cash-Secured Put > Covered Strangle
    
    #### Explicação da Fórmula de Black-Scholes
    
    A fórmula de Black-Scholes é usada para calcular o preço teórico de opções estilo europeu. As principais entradas são:
    
    - **S**: Preço atual da ação
    - **K**: Preço de exercício
    - **T**: Tempo até o vencimento (em anos)
    - **r**: Taxa de juros livre de risco (anual)
    - **σ**: Volatilidade do ativo subjacente
    
    A fórmula calcula:
    
    Para uma opção de compra: C = S⋅N(d₁) - K⋅e^(-rT)⋅N(d₂)
    Para uma opção de venda: P = K⋅e^(-rT)⋅N(-d₂) - S⋅N(-d₁)
    
    Onde d₁ e d₂ são calculados com base nas entradas, e N() é a função de distribuição acumulada da distribuição normal padrão.
    """)


def render():
    """
    Função principal que renderiza o módulo de Opções.
    Esta função deve ser chamada pelo hub principal.
    """
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Create tabs for different sections of the app
    tabs = st.tabs(["Introdução", "Simulador de Opções", "Estratégias com Opções", "Recursos Educacionais"])
    
    # Introduction Tab
    with tabs[0]:
        render_introduction_tab()
    
    # Option Simulator Tab
    with tabs[1]:
        render_simulator_tab()
    
    # Option Strategies Tab
    with tabs[2]:
        render_strategies_tab()
    
    # Educational Resources Tab
    with tabs[3]:
        render_educational_tab()


# Permitir execução standalone para testes
if __name__ == "__main__":
    render()