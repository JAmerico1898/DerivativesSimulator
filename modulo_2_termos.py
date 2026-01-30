"""
Módulo 2: Contratos a Termo (NDF)
Simulador interativo de Non-Deliverable Forwards de USD/BRL.
"""

import streamlit as st
import plotly.graph_objects as go


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
    
    .currency-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.2rem;
    }
</style>
"""


def formatar_moeda_brl(valor):
    """Formata valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_moeda_usd(valor):
    """Formata valor como dólares americanos."""
    return f"US$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_cotacao(valor):
    """Formata cotação com 2 casas decimais."""
    return f"R$ {valor:.2f}"


def calcular_resultado_ndf(operacao, cotacao_contratacao, cotacao_vencimento, valor_nocional_usd):
    """
    Calcula o resultado da operação NDF conforme as fórmulas:
    Compra: (Cotação Vencimento - Cotação Contratação) × N
    Venda: (Cotação Contratação - Cotação Vencimento) × N
    """
    if operacao == "Compra":
        resultado = (cotacao_vencimento - cotacao_contratacao) * valor_nocional_usd
    else:  # Venda
        resultado = (cotacao_contratacao - cotacao_vencimento) * valor_nocional_usd
    
    return resultado


def calcular_valor_inicial_brl(cotacao_contratacao, valor_nocional_usd):
    """Calcula valor inicial em reais para referência."""
    return cotacao_contratacao * valor_nocional_usd


def calcular_valor_final_brl(cotacao_vencimento, valor_nocional_usd):
    """Calcula valor final em reais para referência."""
    return cotacao_vencimento * valor_nocional_usd


def criar_grafico_evolucao(operacao, cotacao_contratacao, cotacao_vencimento, 
                           valor_nocional_milhoes, resultado_operacao):
    """Cria o gráfico de evolução da cotação USD/BRL."""
    fig = go.Figure()

    # Cotação à vista do dólar (apenas ilustrativa)
    cotacao_vista = 5.00

    # Linha mostrando a evolução da cotação NDF
    periodos = ['Contratação (D0)', 'Vencimento (1 ano)']
    cotacoes = [cotacao_contratacao, cotacao_vencimento]
    cores_linha = ['#3498db', '#27ae60' if cotacao_vencimento > cotacao_contratacao else '#e74c3c']

    fig.add_trace(go.Scatter(
        x=periodos,
        y=cotacoes,
        mode='lines+markers',
        name='Cotação NDF (Contrato)',
        line=dict(color='#3498db', width=4),
        marker=dict(
            color=cores_linha,
            size=15,
            line=dict(color='white', width=3)
        ),
        hovertemplate='<b>%{x}</b><br>Cotação NDF: R$ %{y:.2f}<extra></extra>'
    ))

    # Linha horizontal mostrando a cotação à vista (apenas ilustrativa)
    fig.add_trace(go.Scatter(
        x=periodos,
        y=[cotacao_vista, cotacao_vencimento],
        mode='lines+markers',
        name='Cotação à Vista (Referência)',
        line=dict(color='#95a5a6', width=2, dash='dash'),
        marker=dict(
            color='#95a5a6',
            size=10,
            symbol='square',
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{x}</b><br>Cotação à Vista: R$ %{y:.2f}<br><i>(Apenas referência)</i><extra></extra>'
    ))

    # Adicionar área sombreada para mostrar a variação
    fig.add_trace(go.Scatter(
        x=periodos + periodos[::-1],
        y=[min(cotacoes), min(cotacoes)] + [max(cotacoes), max(cotacoes)],
        fill='tonexty',
        fillcolor='rgba(52, 152, 219, 0.1)' if resultado_operacao >= 0 else 'rgba(231, 76, 60, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        title={
            'text': f'Contrato NDF vs Cotação à Vista - {operacao} de US$ {valor_nocional_milhoes:.0f} milhões',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis_title="Período",
        yaxis_title="Cotação (R$/US$)",
        height=400,
        showlegend=True,
        hovermode='x unified',
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
    Função principal que renderiza o módulo de Termos (NDF).
    Esta função deve ser chamada pelo hub principal.
    """
    # Aplicar CSS customizado
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Cabeçalho da aplicação
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">💱 Simulador de Contratos NDF</h1>
        <p class="header-subtitle">Ferramenta educacional para entender Non-Deliverable Forwards de USD/BRL</p>
    </div>
    """, unsafe_allow_html=True)

    # Caixa de informações
    st.markdown("""
    <div class="info-box">
        <h3>ℹ️ O que é um NDF?</h3>
        <p>O <strong>NDF (Non-Deliverable Forward)</strong> é um contrato a termo de câmbio com liquidação financeira. 
        A diferença entre a cotação acordada e a cotação de referência no vencimento é liquidada em moeda local (reais), 
        <strong>sem entrega física</strong> da moeda americana.</p>
    </div>
    """, unsafe_allow_html=True)

    # Layout de inputs
    st.markdown("## 🎯 Parâmetros da Operação NDF")

    st.write("A cotação da moeda americana no mercado à vista na data da contratação é de 5,00 (BRL/USD)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Dados da Operação")
        
        operacao = st.selectbox(
            "Tipo de Operação:",
            ["Compra", "Venda"],
            help="Compra: Você lucra se o dólar subir. Venda: Você lucra se o dólar descer.",
            key="termos_operacao"
        )
        
        valor_nocional_milhoes = st.number_input(
            "Valor Nocional (US$ milhões):",
            min_value=1.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
            format="%.0f",
            help="Valor da operação em milhões de dólares americanos",
            key="termos_valor_nocional"
        )
        
        st.markdown('<div class="currency-label">Valor em USD para cálculo dos resultados</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("💲 Cotações USD/BRL")
        
        cotacao_contratacao = st.number_input(
            "Cotação do NDF na data da contratação (BRL/USD):",
            min_value=1.0000,
            max_value=10.0000,
            value=5.2000,
            step=0.0100,
            format="%.2f",
            help="Taxa de câmbio BRL/USD acordada no momento da contratação",
            key="termos_cotacao_contratacao"
        )
        
        cotacao_vencimento = st.number_input(
            "Cotação do NDF no Vencimento (BRL/USD):",
            min_value=1.0000,
            max_value=10.0000,
            value=5.5000,
            step=0.0100,
            format="%.2f",
            help="Taxa de câmbio BRL/USD na data de vencimento (1 ano depois)",
            key="termos_cotacao_vencimento"
        )
        
        st.markdown('<div class="currency-label">Valores em Reais por Dólar</div>', unsafe_allow_html=True)

    # Realizar cálculos
    valor_nocional_usd = valor_nocional_milhoes * 1000000  # Converter para valor total em USD
    resultado_operacao = calcular_resultado_ndf(operacao, cotacao_contratacao, cotacao_vencimento, valor_nocional_usd)
    valor_inicial_brl = calcular_valor_inicial_brl(cotacao_contratacao, valor_nocional_usd)
    valor_final_brl = calcular_valor_final_brl(cotacao_vencimento, valor_nocional_usd)
    diferenca_cotacao = cotacao_vencimento - cotacao_contratacao
    variacao_percentual = (diferenca_cotacao / cotacao_contratacao) * 100

    # Exibir resultados em cartões coloridos
    st.markdown("## 📊 Resultados da Operação NDF")

    # Layout dos resultados em colunas
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)

    with res_col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Valor Nocional</div>
            <div class="metric-value">{formatar_moeda_usd(valor_nocional_usd)}</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Variação do USD</div>
            <div class="metric-value">{variacao_percentual:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Diferença de Cotação</div>
            <div class="metric-value">{formatar_cotacao(diferenca_cotacao)}</div>
        </div>
        """, unsafe_allow_html=True)

    with res_col4:
        profit_class = "profit-positive" if resultado_operacao >= 0 else "profit-negative"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Resultado da Operação</div>
            <div class="metric-value {profit_class}">{formatar_moeda_brl(resultado_operacao)}</div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico da evolução das cotações
    st.markdown("## 📈 Evolução da Cotação USD/BRL")

    fig = criar_grafico_evolucao(operacao, cotacao_contratacao, cotacao_vencimento, 
                                  valor_nocional_milhoes, resultado_operacao)
    st.plotly_chart(fig, use_container_width=True)

    # Análise detalhada do resultado
    st.markdown("## 🎯 Análise Detalhada")

    col_analise1, col_analise2 = st.columns(2)

    with col_analise1:
        st.markdown("### 📊 Resumo Financeiro")
        
        if resultado_operacao > 0:
            st.success(f"✅ **Operação Lucrativa**: A {operacao.lower()} do NDF resultou em um **ganho** de {formatar_moeda_brl(resultado_operacao)}.")
        elif resultado_operacao < 0:
            st.error(f"❌ **Operação com Prejuízo**: A {operacao.lower()} do NDF resultou em uma **perda** de {formatar_moeda_brl(abs(resultado_operacao))}.")
        else:
            st.info("⚖️ **Operação Neutra**: A operação não resultou em ganho nem perda.")
        
        st.markdown(f"""
        **Detalhes da Operação:**
        - **Valor Nocional**: {formatar_moeda_usd(valor_nocional_usd)}
        - **Cotação no Mercado à Vista**: R$5.00
        - **Cotação na Data da Contratação**: {formatar_cotacao(cotacao_contratacao)}
        - **Cotação no Vencimento**: {formatar_cotacao(cotacao_vencimento)}
        - **Variação**: {diferenca_cotacao:+.2f} ({variacao_percentual:+.2f}%)
        """)

    with col_analise2:
        st.markdown("### 🧮 Como foi Calculado")
        
        if operacao == "Compra":
            st.markdown(f"""
            **Fórmula para Compra de NDF:**
            
            `Resultado = (Cotação Vencimento - Cotação Contratação) × N`
            
            **Aplicando os valores:**
            - Cotação no Vencimento: {formatar_cotacao(cotacao_vencimento)}
            - Cotação na Data da Contratação: {formatar_cotacao(cotacao_contratacao)}
            - Valor Nocional (N): {formatar_moeda_usd(valor_nocional_usd)}
            
            **Cálculo:**
            `({cotacao_vencimento:.2f} - {cotacao_contratacao:.2f}) × {valor_nocional_usd:,.0f}`
            `= {diferenca_cotacao:+.2f} × {valor_nocional_usd:,.0f}`
            `= {formatar_moeda_brl(resultado_operacao)}`
            """)
        else:
            st.markdown(f"""
            **Fórmula para Venda de NDF:**
            
            `Resultado = (Cotação Contratação - Cotação Vencimento) × N`
            
            **Aplicando os valores:**
            - Cotação Contratação: {formatar_cotacao(cotacao_contratacao)}
            - Cotação Vencimento: {formatar_cotacao(cotacao_vencimento)}
            - Valor Nocional (N): {formatar_moeda_usd(valor_nocional_usd)}
            
            **Cálculo:**
            `({cotacao_contratacao:.2f} - {cotacao_vencimento:.2f}) × {valor_nocional_usd:,.0f}`
            `= {-diferenca_cotacao:+.2f} × {valor_nocional_usd:,.0f}`
            `= {formatar_moeda_brl(resultado_operacao)}`
            """)

    # Seção educacional com fórmulas
    st.markdown("## 📚 Fórmulas e Conceitos")

    col_form1, col_form2 = st.columns(2)

    with col_form1:
        st.markdown("""
        **Fórmulas do NDF:**
        <div class="formula-box">
        <strong>Compra de NDF:</strong><br>
        Resultado = (Cotação Vencimento - Cotação Contratação) × N
        </div>
        
        <div class="formula-box">
        <strong>Venda de NDF:</strong><br>
        Resultado = (Cotação Contratação - Cotação Vencimento) × N
        </div>
        """, unsafe_allow_html=True)

    with col_form2:
        st.markdown("""
        **Interpretação dos Resultados:**
        <div class="formula-box">
        <strong>Compra:</strong> Lucra se USD subir<br>
        <strong>Venda:</strong> Lucra se USD descer<br>
        <strong>N:</strong> Valor Nocional em USD<br>
        <strong>Liquidação:</strong> Sempre em BRL
        </div>
        """, unsafe_allow_html=True)

    # Explicação adicional
    with st.expander("📖 Entenda o NDF em Detalhes"):
        st.markdown("""
        **Características do NDF:**
        - **Sem entrega física**: Apenas liquidação financeira da diferença
        - **Proteção cambial**: Usado para hedge de exposição ao dólar
        - **Derivativo de balcão**: Negociado diretamente entre as partes
        - **Duração fixa**: 1 ano no nosso exemplo
        
        **Estratégias:**
        - **Compra**: Proteção contra alta do dólar (importadores)
        - **Venda**: Proteção contra queda do dólar (exportadores)
        - **Especulação**: Apostas direcionais na cotação do USD/BRL
        
        **Riscos:**
        - **Risco de mercado**: Variações adversas da cotação
        - **Risco de contraparte**: Possibilidade de inadimplência
        - **Risco de liquidez**: Dificuldade para desfazer a posição
        """)


# Permitir execução standalone para testes
if __name__ == "__main__":
    render()