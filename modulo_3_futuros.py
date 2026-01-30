"""
Módulo 3: Contratos Futuros (DI Futuro)
Simulador interativo de contratos DI futuro.
"""

import streamlit as st
import plotly.graph_objects as go
import math


# CSS customizado para melhorar o visual
CUSTOM_CSS = """
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .stNumberInput > div > div {
        background-color: #f8f9fa;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 0.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.8rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        margin: 0.3rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        opacity: 1;
    }
    
    .profit-positive {
        color: green;
    }
    
    .profit-negative {
        color: gold;
    }
    
    .info-box {
        background: #e8f6ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .formula-box {
        background: #f8f9fa;
        padding: 0.3rem;
        border-radius: 8px;
        border-left: 1px solid #17a2b8;
        font-family: 'Courier New', monospace;
        margin: 0.2rem 0;
    }
    
    .header-container {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -2rem -3rem 2rem -3rem;
        border-radius: 0 0 20px 20px;
        color: white;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
</style>
"""


def formatar_moeda(valor):
    """Formata valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor):
    """Formata número com separador de milhares."""
    return f"{valor:,.0f}".replace(",", ".")


def calcular_pu_contratacao(taxa_contratacao, prazo_vencimento):
    """Calcula o PU na contratação."""
    return 100000 / ((1 + taxa_contratacao) ** (prazo_vencimento / 252))


def calcular_numero_contratos(valor_nocional, pu_contratacao):
    """Calcula número de contratos (arredondado para baixo)."""
    return math.floor(valor_nocional / pu_contratacao)


def calcular_pu_vencimento(pu_contratacao, taxa_efetiva):
    """Calcula PU no vencimento."""
    return pu_contratacao * (1 + taxa_efetiva)


def calcular_resultado(operacao, pu_contratacao, pu_vencimento, numero_contratos):
    """Calcula resultado da operação."""
    if operacao == "Compra":
        return (pu_vencimento - 100000) * numero_contratos
    else:
        return (100000 - pu_vencimento) * numero_contratos


def calcular_taxa_efetiva_anual(taxa_efetiva, prazo_vencimento):
    """Taxa Efetiva Anual no Período."""
    return ((1 + taxa_efetiva / 100) ** (252 / prazo_vencimento) - 1) * 100


def criar_grafico_pu(operacao, pu_contratacao, pu_vencimento, prazo_vencimento):
    """Cria o gráfico de evolução do PU."""
    fig = go.Figure()

    # Linha horizontal: D0 até o prazo (base do retângulo)
    fig.add_trace(go.Scatter(
        x=['D0', f'{prazo_vencimento} DU', 'Vcto'],
        y=[pu_contratacao, pu_contratacao, pu_contratacao],
        mode='lines',
        line=dict(color="#000406", width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Linha vertical esquerda: PU contratação
    fig.add_trace(go.Scatter(
        x=['D0', 'Vcto'],
        y=[pu_contratacao, 100000],
        mode='lines+markers',
        name=f'PU = {formatar_moeda(pu_contratacao)}',
        line=dict(color='#3498db', width=2),
        marker=dict(color='#3498db', size=8),
        hovertemplate='<b>D0</b><br>PU: %{y:,.2f}<extra></extra>'
    ))

    # Linha vertical direita: PU vencimento
    fig.add_trace(go.Scatter(
        x=['D0', 'Vcto'],
        y=[pu_contratacao, pu_vencimento],
        mode='lines+markers',
        name=f'PU = {formatar_moeda(pu_vencimento)}',
        line=dict(color='#e74c3c' if pu_vencimento < 100000 else '#27ae60', width=3),
        marker=dict(color='#e74c3c' if pu_vencimento < 100000 else '#27ae60', size=8),
        hovertemplate='<b>%{x}</b><br>PU: %{y:,.2f}<extra></extra>'
    ))

    # Linha pontilhada mostrando valor teórico de 100.000
    fig.add_trace(go.Scatter(
        x=['D0', f'{prazo_vencimento} DU', 'Vcto'],
        y=[100000, 100000, 100000],
        mode='lines',
        name='PU = R$ 100.000 (Teórico)',
        line=dict(color='gray', width=1, dash='dot'),
        hovertemplate='<b>Valor Teórico</b><br>PU: R$ 100.000,00<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': f'Comportamento do PU - {operacao} de Contratos DI',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title="Período",
        yaxis_title="Preço Unitário (R$)",
        height=400,
        showlegend=True,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        tickformat=',.2f'
    )

    return fig


def render():
    """
    Função principal que renderiza o módulo de Futuros (DI Futuro).
    Esta função deve ser chamada pelo hub principal.
    """
    # Aplicar CSS customizado
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Cabeçalho da aplicação
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">📈 Simulador de Contratos DI Futuro</h1>
        <p class="header-subtitle">Ferramenta educacional para entender o comportamento de contratos DI futuro</p>
    </div>
    """, unsafe_allow_html=True)

    # Caixa de informações
    st.markdown("""
    <div class="info-box">
        <h3>ℹ️ Como funciona:</h3>
        <p>O contrato DI futuro é um derivativo que representa a expectativa sobre a taxa CDI futura. 
        Ajuste os parâmetros abaixo e veja como eles afetam o resultado da operação.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("🎯 Parâmetros da Operação")

    # Layout de inputs em colunas
    col1, col2 = st.columns(2)

    with col1:
        operacao = st.selectbox(
            "Tipo de Operação:",
            ["Compra", "Venda"],
            help="Escolha se você está comprando ou vendendo contratos DI futuro",
            key="futuros_operacao"
        )
        
        valor_nocional_milhoes = st.number_input(
            "Valor Nocional (R$ milhões):",
            min_value=10.0,
            max_value=100.0,
            value=50.0,
            step=1.0,
            help="Valor total da operação em milhões de reais",
            key="futuros_valor_nocional"
        )

        prazo_vencimento = st.number_input(
            "Prazo para Vencimento (dias úteis):",
            min_value=1,
            max_value=252,
            value=10,
            step=1,
            help="Número de dias úteis até o vencimento (ano = 252 dias úteis)",
            key="futuros_prazo_vencimento"
        )

    with col2:
        taxa_contratacao = st.number_input(
            "Taxa de Juros na Contratação (% a.a.):",
            min_value=0.0,
            max_value=50.0,
            value=12.0,
            step=0.01,
            format="%.2f",
            help="Taxa de juros anual no momento da contratação",
            key="futuros_taxa_contratacao"
        )
        
        taxa_efetiva = st.number_input(
            "Taxa Efetiva no Período (%):",
            min_value=-10.0,
            max_value=10.0,
            value=0.50,
            step=0.01,
            format="%.2f",
            help="Taxa efetiva realizada no período",
            key="futuros_taxa_efetiva"
        )

        taxa_efetiva_anual_periodo = calcular_taxa_efetiva_anual(taxa_efetiva, prazo_vencimento)
        taxa_efetiva_anual = st.number_input(
            "Taxa Efetiva Anual no Período (%):",
            value=taxa_efetiva_anual_periodo,
            format="%.2f",
            help="Taxa efetiva anual realizada no período",
            key="futuros_taxa_efetiva_anual"
        )

    # Realizar cálculos
    valor_nocional = valor_nocional_milhoes * 1000000
    taxa_contratacao_decimal = taxa_contratacao / 100
    taxa_efetiva_decimal = taxa_efetiva / 100

    pu_contratacao = calcular_pu_contratacao(taxa_contratacao_decimal, prazo_vencimento)
    numero_contratos = calcular_numero_contratos(valor_nocional, pu_contratacao)
    pu_vencimento = calcular_pu_vencimento(pu_contratacao, taxa_efetiva_decimal)
    resultado_operacao = calcular_resultado(operacao, pu_contratacao, pu_vencimento, numero_contratos)

    # Exibir resultados em cartões coloridos
    st.markdown("## 📊 Resultados da Operação")

    # Layout dos resultados em colunas
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)

    with res_col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">PU na Contratação</div>
            <div class="metric-value">{formatar_moeda(pu_contratacao)}</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Número de Contratos</div>
            <div class="metric-value">{formatar_numero(numero_contratos)}</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">PU no Vencimento</div>
            <div class="metric-value">{formatar_moeda(pu_vencimento)}</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col4:
        profit_class = "profit-positive" if resultado_operacao >= 0 else "profit-negative"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Resultado da Operação</div>
            <div class="metric-value {profit_class}">{formatar_moeda(resultado_operacao)}</div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico da evolução do PU
    st.markdown("## 📈 Evolução do Preço Unitário (PU)")

    fig = criar_grafico_pu(operacao, pu_contratacao, pu_vencimento, prazo_vencimento)
    st.plotly_chart(fig, use_container_width=True)

    # Análise do resultado
    st.markdown("## 🎯 Análise do Resultado")

    diferenca_pu = pu_vencimento - 100000
    percentual_variacao = (diferenca_pu / 100000) * 100

    col_analise1, col_analise2 = st.columns(2)

    with col_analise1:
        if resultado_operacao > 0:
            st.success(f"✅ **Operação Lucrativa**: A {operacao.lower()} de contratos DI futuro resultou em um ganho de **{formatar_moeda(resultado_operacao)}**.")
        elif resultado_operacao < 0:
            st.error(f"❌ **Operação com Prejuízo**: A {operacao.lower()} de contratos DI futuro resultou em uma perda de **{formatar_moeda(abs(resultado_operacao))}**.")
        else:
            st.info("⚖️ **Operação Neutra**: A operação não resultou em ganho nem perda.")

    with col_analise2:
        st.info(f"""
        **Variação do PU:**
        - Diferença: {formatar_moeda(diferenca_pu)}
        - Percentual: {percentual_variacao:+.3f}%
        - Contratos: {formatar_numero(numero_contratos)}
        """)

    # Explicação das linhas do gráfico
    st.markdown("""
    **Interpretação do Gráfico:**
    - 🔵 **Linha Azul Pontilhada**: Mostra o desconto aplicado pela taxa de juros contratada (de R$ 100.000 para o PU na contratação)
    - 🟢/🔴 **Linha Contínua**: Mostra a realização efetiva (do PU contratado ao PU no vencimento)
    - A **diferença entre as linhas** representa o ganho/perda da operação
    """)

    # Seção educacional com fórmulas
    st.markdown("## 📚 Fórmulas Matemáticas")

    col_form1, col_form2 = st.columns(2)

    with col_form1:
        st.markdown("""
        **Cálculo do PU na Contratação:**
        <div class="formula-box">PU = 100.000 / (1 + R)^(t/252)</div>
        
        **Número de Contratos:**
        <div class="formula-box">N = floor(Valor Nocional / PU)</div>
        """, unsafe_allow_html=True)

    with col_form2:
        st.markdown("""
        **PU no Vencimento:**
        <div class="formula-box">PU_vcto = PU × (1 + R')</div>
        
        **Resultado da Operação:**
        <div class="formula-box">
        Compra: (PU_vcto - 100000) × N<br>
        Venda: (100000 - PU_vcto) × N
        </div>
        """, unsafe_allow_html=True)

    # Explicação adicional
    with st.expander("📖 Entenda os Conceitos"):
        st.markdown("""
        **Variáveis:**
        - **R**: Taxa de juros de mercado na contratação (% a.a.)
        - **t**: Prazo para vencimento em dias úteis
        - **R'**: Taxa de juros efetiva no período (%)
        - **PU**: Preço Unitário do contrato
        - **N**: Número de contratos negociados
        
        **Como Interpretar:**
        - **Compra**: Você lucra se a taxa efetiva for menor que a esperada (PU sobe)
        - **Venda**: Você lucra se a taxa efetiva for maior que a esperada (PU desce)
        - O resultado é proporcional ao número de contratos e à diferença entre o PU no vencimento e R$100.000
        """)


# Permitir execução standalone para testes
if __name__ == "__main__":
    render()