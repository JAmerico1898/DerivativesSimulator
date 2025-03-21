import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum
from scipy.stats import norm
import math
import random


st.markdown("<h2 style='text-align: center;'>📊 Simulador de Derivativos</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Ferramenta com fins pedagógicos</h3>", unsafe_allow_html=True)
#st.markdown("<h6 style='text-align: center;'>(dados Opta)</h6>", unsafe_allow_html=True)

st.markdown("---")

# Initialize session state variables if they don’t exist
if "step" not in st.session_state:
    st.session_state.step = "start"  # Initial state
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# Function to update the selected option
def select_option(option):
    st.session_state.selected_option = option

# Create three columns for the initial choices
col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    if st.button("Introdução", type='primary', use_container_width=True):
        st.session_state.step = "Introdução"
        st.session_state.selected_option = None  # Reset selection when switching

with col3:
    if st.button("Derivativos", type='primary', use_container_width=True):
        st.session_state.step = "Derivativos"
        st.session_state.selected_option = None  # Reset selection when switching

# Step 1: Introdução
if st.session_state.step == "Introdução":
    
    # Função para gerar o banco de questões
    def gerar_banco_questoes():
        questoes = [
            {
                "pergunta": "Qual é a definição básica de um derivativo?",
                "opcoes": [
                    "Um instrumento financeiro cujo valor depende de um ativo subjacente",
                    "Um título emitido pelo governo para financiar dívidas",
                    "Uma ação negociada em bolsa de valores",
                    "Um empréstimo bancário com juros fixos"
                ],
                "resposta": 0,
                "explicacao": "Derivativos são instrumentos financeiros cujo valor depende (ou deriva) do valor de outros ativos subjacentes, como ações, títulos, commodities, moedas, taxas de juros ou índices de mercado."
            },
            {
                "pergunta": "Quais são os dois tipos principais de derivativos em relação ao local de negociação?",
                "opcoes": [
                    "Derivativos primários e secundários",
                    "Derivativos de balcão (OTC) e negociados em bolsa",
                    "Derivativos financeiros e não-financeiros",
                    "Derivativos de curto e longo prazo"
                ],
                "resposta": 1,
                "explicacao": "Quanto à negociação, os derivativos podem ser classificados em derivativos de balcão (OTC - Over The Counter) e derivativos negociados em bolsa."
            },
            {
                "pergunta": "Qual é uma das principais funções dos derivativos no mercado financeiro?",
                "opcoes": [
                    "Aumentar os riscos de mercado para todos os participantes",
                    "Substituir completamente os mercados de ações e títulos",
                    "Oferecer proteção contra variações adversas de preços (hedge)",
                    "Eliminar a necessidade de análise de mercado"
                ],
                "resposta": 2,
                "explicacao": "Uma das principais funções dos derivativos é oferecer proteção (hedge) contra riscos de variações adversas nos preços dos ativos subjacentes."
            },
            {
                "pergunta": "O que caracteriza um contrato a termo (forward)?",
                "opcoes": [
                    "É negociado exclusivamente em bolsas de valores",
                    "Possui liquidez elevada e ajuste diário",
                    "É um acordo personalizado entre duas partes para comprar/vender um ativo em data futura",
                    "Sempre exige entrega física do ativo subjacente"
                ],
                "resposta": 2,
                "explicacao": "Um contrato a termo é um acordo personalizado entre duas partes para comprar ou vender um ativo em uma data futura específica por um preço predeterminado."
            },
            {
                "pergunta": "Qual a principal diferença entre contratos futuros e contratos a termo?",
                "opcoes": [
                    "Futuros não possuem data de vencimento específica",
                    "Futuros são negociados em bolsa e padronizados, enquanto a termo são personalizados e OTC",
                    "Contratos a termo oferecem maior liquidez que futuros",
                    "Contratos futuros não exigem depósito de margem"
                ],
                "resposta": 1,
                "explicacao": "A principal diferença é que contratos futuros são padronizados e negociados em bolsa, enquanto contratos a termo são personalizados e negociados no mercado de balcão (OTC)."
            },
            {
                "pergunta": "Quais são as principais características dos swaps?",
                "opcoes": [
                    "São sempre negociados em bolsa e exigem padronização",
                    "São contratos de curto prazo com vencimento máximo de 30 dias",
                    "São acordos para troca de fluxos de caixa entre duas partes por um período específico",
                    "Exigem sempre a entrega física do ativo subjacente"
                ],
                "resposta": 2,
                "explicacao": "Swaps são acordos entre duas partes para trocar fluxos de caixa ou obrigações de pagamento durante um período específico, conforme condições predeterminadas. São tipicamente negociados no mercado de balcão (OTC)."
            },
            {
                "pergunta": "Quais são os principais tipos de swaps no mercado financeiro?",
                "opcoes": [
                    "Swaps de commodities e swaps de ações",
                    "Swaps de taxa de juros e swaps de moeda",
                    "Swaps de curto prazo e swaps de longo prazo",
                    "Swaps simples e swaps compostos"
                ],
                "resposta": 1,
                "explicacao": "Os principais tipos de swaps são os swaps de taxa de juros (troca de fluxos baseados em taxas de juros diferentes) e swaps de moeda (troca de principal e pagamentos de juros em moedas diferentes)."
            },
            {
                "pergunta": "Qual a principal diferença entre contratos futuros e contratos a termo em termos de liquidação?",
                "opcoes": [
                    "Futuros têm ajustes diários, enquanto contratos a termo são liquidados apenas no vencimento",
                    "Contratos a termo são sempre liquidados diariamente",
                    "Futuros não possuem liquidação financeira, apenas física",
                    "Contratos a termo só podem ser liquidados por entrega física"
                ],
                "resposta": 0,
                "explicacao": "Contratos futuros possuem ajustes diários (marking-to-market) onde ganhos e perdas são liquidados diariamente, enquanto contratos a termo são tipicamente liquidados apenas no vencimento."
            },
            {
                "pergunta": "O que significa o termo 'swap' no contexto de derivativos?",
                "opcoes": [
                    "A compra de uma opção de compra e venda simultaneamente",
                    "A troca de fluxos de caixa ou obrigações de pagamento entre duas partes",
                    "A conversão de um contrato futuro em um contrato a termo",
                    "O cancelamento de um derivativo antes de seu vencimento"
                ],
                "resposta": 1,
                "explicacao": "Um swap é um acordo entre duas partes para trocar fluxos de caixa ou obrigações de pagamento de acordo com uma fórmula predeterminada durante um período específico."
            },
            {
                "pergunta": "Qual é o propósito do hedge com derivativos?",
                "opcoes": [
                    "Aumentar a exposição ao risco para obter maiores retornos",
                    "Remover completamente qualquer possibilidade de lucro ou perda",
                    "Proteger-se contra movimentos adversos de preços dos ativos",
                    "Manipular preços de mercado a favor do investidor"
                ],
                "resposta": 2,
                "explicacao": "O hedge com derivativos tem como propósito proteger investidores ou empresas contra movimentos adversos nos preços dos ativos, transferindo o risco para outras partes dispostas a assumi-lo."
            },
            {
                "pergunta": "O que caracteriza um derivativo negociado em bolsa?",
                "opcoes": [
                    "Contratos personalizados para necessidades específicas de cada cliente",
                    "Ausência de uma câmara de compensação",
                    "Contratos padronizados com especificações uniformes",
                    "Maior risco de contraparte comparado aos derivativos de balcão"
                ],
                "resposta": 2,
                "explicacao": "Derivativos negociados em bolsa são caracterizados por contratos padronizados com especificações uniformes quanto a quantidade, qualidade, data de entrega e local."
            },
            {
                "pergunta": "Qual é uma das vantagens dos derivativos de balcão (OTC) em relação aos negociados em bolsa?",
                "opcoes": [
                    "Maior padronização",
                    "Menor risco de contraparte",
                    "Maior liquidez",
                    "Flexibilidade para atender necessidades específicas"
                ],
                "resposta": 3,
                "explicacao": "Uma das principais vantagens dos derivativos OTC é a flexibilidade para personalizar os contratos de acordo com as necessidades específicas das partes envolvidas."
            },
            {
                "pergunta": "O que é a 'margem inicial' em contratos futuros?",
                "opcoes": [
                    "O lucro máximo possível do contrato",
                    "O depósito exigido pela bolsa para garantir o cumprimento do contrato",
                    "A diferença entre o preço à vista e o preço futuro",
                    "O valor do prêmio pago pelo comprador do contrato"
                ],
                "resposta": 1,
                "explicacao": "A margem inicial é um depósito de garantia exigido pela bolsa para assegurar que os participantes possam cumprir suas obrigações contratuais, funcionando como um mecanismo de gerenciamento de risco."
            },
            {
                "pergunta": "O que significa o termo 'ajuste diário' em contratos futuros?",
                "opcoes": [
                    "A revisão diária das cláusulas do contrato",
                    "A liquidação diária de ganhos e perdas baseada na variação do preço do contrato",
                    "A mudança diária no preço de exercício",
                    "O pagamento diário de dividendos pelo ativo subjacente"
                ],
                "resposta": 1,
                "explicacao": "O ajuste diário (ou marking-to-market) é o processo de liquidação diária de ganhos e perdas baseada na variação do preço de fechamento do contrato futuro em relação ao dia anterior."
            },
            {
                "pergunta": "Qual é a importância da padronização nos contratos futuros?",
                "opcoes": [
                    "Dificulta a negociação ao criar muitas variações de contratos",
                    "Aumenta o risco de contraparte no mercado",
                    "Facilita a liquidez e a formação de preços no mercado",
                    "Aumenta os custos de transação para todos os participantes"
                ],
                "resposta": 2,
                "explicacao": "A padronização dos contratos futuros facilita a liquidez do mercado e a formação de preços, pois cria um produto uniforme que pode ser facilmente negociado entre múltiplos participantes do mercado."
            },
            {
                "pergunta": "Qual é o papel da câmara de compensação nos derivativos negociados em bolsa?",
                "opcoes": [
                    "Determinar o preço de negociação dos derivativos",
                    "Atuar como contraparte central, reduzindo o risco de inadimplência",
                    "Fornecer financiamento para os participantes do mercado",
                    "Criar novos tipos de contratos derivativos"
                ],
                "resposta": 1,
                "explicacao": "A câmara de compensação atua como contraparte central para todas as transações, garantindo que as obrigações sejam cumpridas e reduzindo significativamente o risco de inadimplência nos derivativos negociados em bolsa."
            },
            {
                "pergunta": "O que é arbitragem no contexto de derivativos?",
                "opcoes": [
                    "A negociação de opções de compra e venda simultaneamente",
                    "O processo de resolução de disputas entre partes de um contrato",
                    "A exploração de discrepâncias de preços para obter lucro sem risco",
                    "A determinação do preço justo de um derivativo por especialistas"
                ],
                "resposta": 2,
                "explicacao": "Arbitragem é a estratégia de explorar discrepâncias de preços entre mercados ou instrumentos relacionados para obter lucro sem risco (ou com risco mínimo)."
            },
            {
                "pergunta": "Qual é o principal risco associado aos derivativos de balcão (OTC)?",
                "opcoes": [
                    "Risco de liquidez",
                    "Risco de contraparte",
                    "Risco de taxa de juros",
                    "Risco cambial"
                ],
                "resposta": 1,
                "explicacao": "O principal risco associado aos derivativos OTC é o risco de contraparte - a possibilidade de que uma das partes não cumpra suas obrigações contratuais."
            },
            {
                "pergunta": "O que é a alavancagem em derivativos?",
                "opcoes": [
                    "A capacidade de controlar um valor substancial de ativos com um investimento relativamente pequeno",
                    "O uso de dívida para financiar a compra de derivativos",
                    "A combinação de vários tipos de derivativos em uma única estratégia",
                    "O aumento automático do valor do contrato ao longo do tempo"
                ],
                "resposta": 0,
                "explicacao": "Alavancagem em derivativos refere-se à capacidade de controlar um valor substancial de ativos subjacentes com um investimento inicial relativamente pequeno, o que pode amplificar tanto ganhos quanto perdas."
            },
            {
                "pergunta": "Quais são os principais participantes do mercado de derivativos?",
                "opcoes": [
                    "Apenas especuladores e investidores de varejo",
                    "Apenas bancos centrais e governos",
                    "Hedgers, especuladores e arbitradores",
                    "Apenas empresas multinacionais"
                ],
                "resposta": 2,
                "explicacao": "Os principais participantes do mercado de derivativos são os hedgers (que buscam proteção contra riscos), especuladores (que assumem riscos em busca de lucro) e arbitradores (que exploram ineficiências de preços)."
            },
            {
                "pergunta": "Como os contratos futuros podem ser utilizados por produtores agrícolas?",
                "opcoes": [
                    "Apenas para especular com os preços das commodities",
                    "Para proteger-se contra quedas nos preços de seus produtos",
                    "Para aumentar a volatilidade de seus rendimentos",
                    "Para evitar a necessidade de vender seus produtos no mercado físico"
                ],
                "resposta": 1,
                "explicacao": "Produtores agrícolas podem utilizar contratos futuros para fazer hedge contra quedas nos preços de seus produtos, garantindo um preço de venda predeterminado e reduzindo a incerteza em relação à receita futura."
            },
            {
                "pergunta": "O que é a base no contexto de contratos futuros?",
                "opcoes": [
                    "O valor mínimo que um contrato futuro pode atingir",
                    "A diferença entre o preço à vista e o preço futuro",
                    "O custo de transação para negociar um contrato futuro",
                    "O valor da margem inicial exigida pela bolsa"
                ],
                "resposta": 1,
                "explicacao": "A base é a diferença entre o preço à vista (spot) do ativo subjacente e o preço do contrato futuro. A base tende a convergir para zero à medida que o contrato se aproxima do vencimento."
            }
        ]
        return questoes

    # Mensagens de feedback divertidas
    feedback_correto = [
        "🎉 Acertou! Você está mandando bem nos derivativos!",
        "✅ Correto! Está no caminho certo para se tornar um especialista!",
        "🔥 Resposta correta! Isso aí, continue assim!",
        "👍 Exato! Seu professor ficaria orgulhoso!",
        "🌟 Perfeito! Você entendeu o conceito muito bem!"
    ]

    feedback_incorreto = [
        "❌ Ops! Não foi dessa vez. Mas não desanime!",
        "😅 Resposta incorreta, mas errar faz parte do aprendizado!",
        "🤔 Hmm, não está certo. Vamos revisar esse conceito?",
        "📚 Incorreto! Sugestão: reveja esta parte do material!",
        "🧐 Não é essa a resposta. Mas você está aprendendo!"
    ]

        # Função para selecionar questões aleatórias
    def selecionar_questoes_aleatorias(banco_questoes, quantidade=10):
        # Filtrar questões para remover qualquer menção a opções
        banco_filtrado = [q for q in banco_questoes if "opção" not in q["pergunta"].lower() and 
                        "call" not in q["pergunta"].lower() and 
                        "put" not in q["pergunta"].lower()]
        
        if quantidade > len(banco_filtrado):
            quantidade = len(banco_filtrado)
        return random.sample(banco_filtrado, quantidade)

    # Função para exibir questão
    def exibir_questao(questao, indice):
        st.subheader(f"Questão {indice + 1}")
        st.write(questao["pergunta"])
        opcao_selecionada = st.radio("Escolha uma opção:", questao["opcoes"], key=f"q{indice}")
        indice_opcao = questao["opcoes"].index(opcao_selecionada)
        
        if st.button("Responder", key=f"responder{indice}"):
            if indice_opcao == questao["resposta"]:
                st.success(random.choice(feedback_correto))
                st.session_state[f"pontos_q{indice}"] = 1
            else:
                st.error(random.choice(feedback_incorreto))
                st.session_state[f"pontos_q{indice}"] = 0
            
            st.info(f"**Explicação:** {questao['explicacao']}")
            
            # Mostre a resposta correta se o usuário errou
            if indice_opcao != questao["resposta"]:
                st.write(f"**Resposta correta:** {questao['opcoes'][questao['resposta']]}")
        
        # Adicionar espaçador entre questões
        st.markdown("---")

    # Interface principal
    def main():
        st.title("Quiz de Derivativos")
        st.markdown("""
        ### Bem-vindo ao questionário interativo sobre Introdução aos Derivativos!
        
        Este quiz contém 10 questões de múltipla escolha para testar seus conhecimentos sobre derivativos financeiros.
        Cada vez que você clicar em "Gerar Novo Questionário", um conjunto diferente de perguntas será selecionado.
        
        Boa sorte! 📊📈
        """)
        
        # Inicializar ou resetar o quiz
        if st.button("Gerar Novo Questionário") or "questoes" not in st.session_state:
            banco_questoes = gerar_banco_questoes()
            st.session_state.questoes = selecionar_questoes_aleatorias(banco_questoes)
            
            # Resetar pontuação
            for i in range(len(st.session_state.questoes)):
                st.session_state[f"pontos_q{i}"] = 0
        
        # Exibir as questões
        for i, questao in enumerate(st.session_state.questoes):
            exibir_questao(questao, i)
        
        # Calcular e exibir pontuação total
        if "questoes" in st.session_state:
            pontos_total = sum([st.session_state.get(f"pontos_q{i}", 0) for i in range(len(st.session_state.questoes))])
            
            # Só mostrar pontuação se pelo menos uma questão foi respondida
            if sum([1 for i in range(len(st.session_state.questoes)) if f"pontos_q{i}" in st.session_state]) > 0:
                st.sidebar.header("Seu Desempenho")
                st.sidebar.metric("Pontuação", f"{pontos_total}/{len(st.session_state.questoes)}")
                
                # Mostrar mensagem baseada na pontuação
                porcentagem = (pontos_total / len(st.session_state.questoes)) * 100
                if porcentagem >= 90:
                    st.sidebar.success("🏆 Excelente! Você domina os derivativos!")
                elif porcentagem >= 70:
                    st.sidebar.success("🎓 Muito bom! Você tem um bom conhecimento!")
                elif porcentagem >= 50:
                    st.sidebar.info("📚 Bom trabalho! Continue estudando!")
                else:
                    st.sidebar.warning("📝 Continue praticando. Você consegue melhorar!")

    if __name__ == "__main__":
        main()


# Step 2: Derivativos
elif st.session_state.step == "Derivativos":

    st.write("---")
    st.markdown("<h5 style='text-align: center;'>Escolha seu Derivativo</h5>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([4, 1, 4])
    with col1:
        st.button("Forwards", type='primary', use_container_width=True, on_click=select_option, args=("Forwards",))
            
    with col3:
        st.button("Futures", type='primary', use_container_width=True, on_click=select_option, args=("Futures",))

    col4, col5, col6 = st.columns([4, 1, 4])
    with col4:
        st.button("Swaps", type='primary', use_container_width=True, on_click=select_option, args=("Swaps",))

    with col6:
        st.button("Options", type='primary', use_container_width=True, on_click=select_option, args=("Options",))
        
    # Handle button selection logic
    if st.session_state.selected_option:
        st.write("---")
        st.markdown(f"<h3 style='text-align: center;'><b>{st.session_state.selected_option}</b></h3>", unsafe_allow_html=True)
        st.write("---")

        # Instructions based on selection
        if st.session_state.selected_option == "Swaps":

            # Enums and dataclasses
            class IndexerType(Enum):
                PRE_FIXED = "Pre-fixed"
                POST_FIXED = "Post-fixed"
                EXCHANGE_RATE = "Exchange Rate"

            class ExposureType(Enum):
                ASSET = "Asset"
                LIABILITY = "Liability"

            @dataclass
            class SwapParameters:
                exposure_type: ExposureType
                notional: float
                indexer: IndexerType
                rate: float
                quarters: int
                cupom_cambial: float = None
                exchange_rate_start: float = None

            @dataclass
            class HedgeParameters:
                asset_indexer: IndexerType
                liability_indexer: IndexerType
                asset_rate: float
                liability_rate: float
                asset_cupom_cambial: float = None
                liability_cupom_cambial: float = None
                exchange_rate_maturity: float = None

            class SwapCalculator:
                def __init__(self, swap_params: SwapParameters, hedge_params: HedgeParameters):
                    self.swap_params = swap_params
                    self.hedge_params = hedge_params
                
                def _calculate_pre_fixed_adjustment(self, rate, quarters):
                    return (1 + rate) ** (quarters/4) - 1
                
                def _calculate_exposure_exchange_rate_adjustment(self, initial_rate, final_rate, rate, quarters):
                    if initial_rate is None or final_rate is None:
                        raise ValueError("Exchange rates must be provided for exchange rate calculations")
                        
                    # Calculate exchange rate variation
                    exchange_variation = (final_rate / initial_rate) - 1
                    
                    # Calculate the rate adjustment using compound interest
                    rate_adjustment = (1 + rate) ** (quarters/4) - 1
                    
                    # Combine both effects using compound interest
                    total_adjustment = (1 + exchange_variation) * (1 + rate_adjustment) - 1
                    
                    return total_adjustment
                
                def _calculate_hedge_exchange_rate_adjustment(self, initial_rate, final_rate, cupom_cambial, quarters):
                    if initial_rate is None or final_rate is None:
                        raise ValueError("Exchange rates must be provided for exchange rate calculations")
                        
                    # Calculate exchange rate variation
                    exchange_variation = (final_rate / initial_rate) - 1
                    
                    # Calculate the cupom cambial adjustment
                    cupom_adjustment = (1 + cupom_cambial) ** (quarters/4) - 1
                    
                    # Combine both effects using compound interest
                    total_adjustment = (1 + exchange_variation) * (1 + cupom_adjustment) - 1
                    
                    return total_adjustment
                
                def calculate_exposure_result(self):
                    if self.swap_params.indexer == IndexerType.PRE_FIXED:
                        adjustment = self._calculate_pre_fixed_adjustment(self.swap_params.rate, self.swap_params.quarters)
                    elif self.swap_params.indexer == IndexerType.POST_FIXED:
                        adjustment = self.swap_params.rate
                    else:  # Exchange Rate
                        adjustment = self._calculate_exposure_exchange_rate_adjustment(
                            self.swap_params.exchange_rate_start,
                            self.hedge_params.exchange_rate_maturity,
                            self.swap_params.rate,  # Using rate for exposure
                            self.swap_params.quarters
                        )
                        
                    result = self.swap_params.notional * adjustment
                    return result if self.swap_params.exposure_type == ExposureType.ASSET else -result
                
                def calculate_hedge_result(self):
                    # Calculate asset leg
                    if self.hedge_params.asset_indexer == IndexerType.PRE_FIXED:
                        asset_adjustment = self._calculate_pre_fixed_adjustment(self.hedge_params.asset_rate, self.swap_params.quarters)
                    elif self.hedge_params.asset_indexer == IndexerType.POST_FIXED:
                        asset_adjustment = self.hedge_params.asset_rate
                    else:  # Exchange Rate
                        asset_adjustment = self._calculate_hedge_exchange_rate_adjustment(
                            self.swap_params.exchange_rate_start,
                            self.hedge_params.exchange_rate_maturity,
                            self.hedge_params.asset_cupom_cambial,  # Using cupom cambial for hedge
                            self.swap_params.quarters
                        )
                        
                    # Calculate liability leg
                    if self.hedge_params.liability_indexer == IndexerType.PRE_FIXED:
                        liability_adjustment = self._calculate_pre_fixed_adjustment(self.hedge_params.liability_rate, self.swap_params.quarters)
                    elif self.hedge_params.liability_indexer == IndexerType.POST_FIXED:
                        liability_adjustment = self.hedge_params.liability_rate
                    else:  # Exchange Rate
                        liability_adjustment = self._calculate_hedge_exchange_rate_adjustment(
                            self.swap_params.exchange_rate_start,
                            self.hedge_params.exchange_rate_maturity,
                            self.hedge_params.liability_cupom_cambial,  # Using cupom cambial for hedge
                            self.swap_params.quarters
                        )
                        
                    asset_result = self.swap_params.notional * asset_adjustment
                    liability_result = self.swap_params.notional * liability_adjustment
                    return asset_result - liability_result
                
                def calculate_total_result(self):
                    exposure_result = self.calculate_exposure_result()
                    hedge_result = self.calculate_hedge_result()
                    return {
                        'exposure_result': exposure_result,
                        'hedge_result': hedge_result,
                        'total_result': exposure_result + hedge_result
                    }

                def generate_time_series(self):
                    """Generate time series data for plotting."""
                    # Create time points (one point per quarter)
                    quarters = np.arange(self.swap_params.quarters + 1)  # Include start point
                    
                    exposure_values = []
                    asset_values = []
                    liability_values = []
                    
                    # Check if we need to handle exchange rates
                    has_exchange_rate = (self.swap_params.indexer == IndexerType.EXCHANGE_RATE or 
                                        self.hedge_params.asset_indexer == IndexerType.EXCHANGE_RATE or 
                                        self.hedge_params.liability_indexer == IndexerType.EXCHANGE_RATE)
                    
                    for q in quarters:
                        # For quarter 0, all values are 0
                        if q == 0:
                            exposure_values.append(0)
                            asset_values.append(0)
                            liability_values.append(0)
                            continue
                        
                        # Initialize exchange variation
                        exchange_variation = 0
                            
                        # Calculate exchange rate at current quarter if needed
                        if has_exchange_rate:
                            current_fx = self.swap_params.exchange_rate_start + \
                                (self.hedge_params.exchange_rate_maturity - self.swap_params.exchange_rate_start) * \
                                (q / self.swap_params.quarters)
                            exchange_variation = (current_fx / self.swap_params.exchange_rate_start) - 1
                        
                        # Calculate exposure values
                        if self.swap_params.indexer == IndexerType.PRE_FIXED:
                            exposure_adj = self._calculate_pre_fixed_adjustment(self.swap_params.rate, q)
                        elif self.swap_params.indexer == IndexerType.POST_FIXED:
                            exposure_adj = self.swap_params.rate * (q / self.swap_params.quarters)
                        else:  # Exchange Rate
                            rate_adj = (1 + self.swap_params.rate) ** (q/4) - 1
                            exposure_adj = (1 + exchange_variation) * (1 + rate_adj) - 1
                        
                        exposure_value = self.swap_params.notional * exposure_adj
                        exposure_values.append(-exposure_value if self.swap_params.exposure_type == ExposureType.LIABILITY else exposure_value)
                        
                        # Calculate asset leg values
                        if self.hedge_params.asset_indexer == IndexerType.PRE_FIXED:
                            asset_adj = self._calculate_pre_fixed_adjustment(self.hedge_params.asset_rate, q)
                        elif self.hedge_params.asset_indexer == IndexerType.POST_FIXED:
                            asset_adj = self.hedge_params.asset_rate * (q / self.swap_params.quarters)
                        else:  # Exchange Rate
                            cupom_adj = (1 + self.hedge_params.asset_cupom_cambial) ** (q/4) - 1
                            asset_adj = (1 + exchange_variation) * (1 + cupom_adj) - 1
                        
                        asset_values.append(self.swap_params.notional * asset_adj)
                        
                        # Calculate liability leg values (now making it negative)
                        if self.hedge_params.liability_indexer == IndexerType.PRE_FIXED:
                            liability_adj = self._calculate_pre_fixed_adjustment(self.hedge_params.liability_rate, q)
                        elif self.hedge_params.liability_indexer == IndexerType.POST_FIXED:
                            liability_adj = self.hedge_params.liability_rate * (q / self.swap_params.quarters)
                        else:  # Exchange Rate
                            cupom_adj = (1 + self.hedge_params.liability_cupom_cambial) ** (q/4) - 1
                            liability_adj = (1 + exchange_variation) * (1 + cupom_adj) - 1
                        
                        # Make liability negative since it's a payment obligation
                        liability_values.append(-self.swap_params.notional * liability_adj)
                    
                    # Calculate net position
                    net_values = [e + a + l for e, a, l in zip(exposure_values, asset_values, liability_values)]  # Note: liability is already negative
                    
                    return {
                        'quarters': quarters,
                        'exposure': exposure_values,
                        'asset': asset_values,
                        'liability': liability_values,
                        'net': net_values
                    }   

                def generate_report(self):
                    results = self.calculate_total_result()
                    
                    report = f"""

            Swap Hedge Analysis Report
            -------------------------
            Period: {self.swap_params.quarters} quarters ({self.swap_params.quarters/4:.2f} years)

            Exposure Details:
            - Type: {self.swap_params.exposure_type.value}
            - Notional: R$ {self.swap_params.notional:,.2f}
            - Indexer: {self.swap_params.indexer.value}
            - Rate: {self.swap_params.rate:.2%}
            {f'- Cupom Cambial: {self.swap_params.cupom_cambial:.2%}' if self.swap_params.cupom_cambial else ''}
            {f'- Initial Exchange Rate: {self.swap_params.exchange_rate_start:.4f}' if self.swap_params.exchange_rate_start else ''}

            Hedge Details:
            Asset Leg:
            - Indexer: {self.hedge_params.asset_indexer.value}
            - Rate: {self.hedge_params.asset_rate:.2%}
            {f'- Cupom Cambial: {self.hedge_params.asset_cupom_cambial:.2%}' if self.hedge_params.asset_cupom_cambial else ''}

            Liability Leg:
            - Indexer: {self.hedge_params.liability_indexer.value}
            - Rate: {self.hedge_params.liability_rate:.2%}
            {f'- Cupom Cambial: {self.hedge_params.liability_cupom_cambial:.2%}' if self.hedge_params.liability_cupom_cambial else ''}
            {f'- Final Exchange Rate: {self.hedge_params.exchange_rate_maturity:.4f}' if self.hedge_params.exchange_rate_maturity else ''}

            Results:
            - Exposure Result: R$ {results['exposure_result']:,.2f}
            - Swap P&L: R$ {results['hedge_result']:,.2f}
            - Total Result: R$ {results['total_result']:,.2f}

            Analysis:
            The {self.swap_params.exposure_type.value.lower()} exposure generated a {'profit' if results['exposure_result'] > 0 else 'loss'} of R$ {abs(results['exposure_result']):,.2f}.
            The hedge operation generated a {'profit' if results['hedge_result'] > 0 else 'loss'} of R$ {abs(results['hedge_result']):,.2f}.
            The combined position resulted in a {'profit' if results['total_result'] > 0 else 'loss'} of R$ {abs(results['total_result']):,.2f}.
            """
                    return report



            st.title("Brazilian Swap Calculator")
            st.markdown("""
            This application helps you calculate and analyze swap operations in the Brazilian market.
            Please fill in the details below for both your exposure and the hedge operation.
            """)

            # Create two columns for exposure and hedge
            col1, col2 = st.columns(2)

            with col1:
                st.header("Exposure Details")
                
                exposure_type = st.selectbox(
                    "Exposure Type",
                    options=[ExposureType.ASSET.value, ExposureType.LIABILITY.value],
                    key="exposure_type"
                )
                
                notional = st.number_input(
                    "Notional Amount (R$)",
                    min_value=0.0,
                    value=1000000.0,
                    step=100000.0,
                    format="%f",
                    key="notional"
                )
                
                exposure_indexer = st.selectbox(
                    "Indexer",
                    options=[idx.value for idx in IndexerType],
                    key="exposure_indexer"
                )
                
                exposure_rate = st.number_input(
                    "Rate (as decimal, e.g., 0.12 for 12%)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.12,
                    step=0.01,
                    format="%f",
                    key="exposure_rate"
                )
                
                if exposure_indexer == IndexerType.EXCHANGE_RATE.value:
                    exposure_exchange_rate = st.number_input(
                        "Initial Exchange Rate (BRL/USD)",
                        min_value=0.0,
                        value=5.0,
                        step=0.1,
                        format="%f",
                        key="exposure_exchange_rate"
                    )
                
                quarters = st.number_input(
                    "Number of Quarters",
                    min_value=1,
                    max_value=40,  # 10 years
                    value=4,  # Default to 1 year
                    step=1,
                    key="quarters"
                )

            with col2:
                st.header("Hedge Details")
                
                # Asset leg
                st.subheader("Asset Leg")
                asset_indexer = st.selectbox(
                    "Asset Indexer",
                    options=[idx.value for idx in IndexerType],
                    key="asset_indexer"
                )
                
                if asset_indexer != IndexerType.EXCHANGE_RATE.value:
                    asset_rate = st.number_input(
                        "Asset Rate (as decimal)",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.115,
                        step=0.01,
                        format="%f",
                        key="asset_rate"
                    )
                
                if asset_indexer == IndexerType.EXCHANGE_RATE.value:
                    asset_cupom = st.number_input(
                        "Asset Cupom Cambial (as decimal)",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.05,
                        step=0.01,
                        format="%f",
                        key="asset_cupom"
                    )
                
                # Liability leg
                st.subheader("Liability Leg")
                liability_indexer = st.selectbox(
                    "Liability Indexer",
                    options=[idx.value for idx in IndexerType],
                    key="liability_indexer"
                )
                
                if liability_indexer != IndexerType.EXCHANGE_RATE.value:
                    liability_rate = st.number_input(
                        "Liability Rate (as decimal)",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.12,
                        step=0.01,
                        format="%f",
                        key="liability_rate"
                    )
                
                if liability_indexer == IndexerType.EXCHANGE_RATE.value:
                    liability_cupom = st.number_input(
                        "Liability Cupom Cambial (as decimal)",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.05,
                        step=0.01,
                        format="%f",
                        key="liability_cupom"
                    )

                # Exchange rate at maturity (shown if any leg uses exchange rate)
                if (asset_indexer == IndexerType.EXCHANGE_RATE.value or 
                    liability_indexer == IndexerType.EXCHANGE_RATE.value or 
                    exposure_indexer == IndexerType.EXCHANGE_RATE.value):
                    exchange_rate_maturity = st.number_input(
                        "Exchange Rate at Maturity (BRL/USD)",
                        min_value=0.0,
                        value=5.2,
                        step=0.1,
                        format="%f",
                        key="exchange_rate_maturity"
                    )

            # Calculate button
            if st.button("Calculate Swap Results"):
                # Create parameters objects
                swap_params = SwapParameters(
                    exposure_type=ExposureType(exposure_type),
                    notional=float(notional),
                    indexer=IndexerType(exposure_indexer),
                    rate=float(exposure_rate),
                    quarters=int(quarters),
                    exchange_rate_start=float(exposure_exchange_rate) if exposure_indexer == IndexerType.EXCHANGE_RATE.value else None
                )
                
                hedge_params = HedgeParameters(
                    asset_indexer=IndexerType(asset_indexer),
                    liability_indexer=IndexerType(liability_indexer),
                    asset_rate=float(asset_rate) if asset_indexer != IndexerType.EXCHANGE_RATE.value else 0.0,
                    liability_rate=float(liability_rate) if liability_indexer != IndexerType.EXCHANGE_RATE.value else 0.0,
                    asset_cupom_cambial=float(asset_cupom) if asset_indexer == IndexerType.EXCHANGE_RATE.value else None,
                    liability_cupom_cambial=float(liability_cupom) if liability_indexer == IndexerType.EXCHANGE_RATE.value else None,
                    exchange_rate_maturity=float(exchange_rate_maturity) if (asset_indexer == IndexerType.EXCHANGE_RATE.value or 
                                                                        liability_indexer == IndexerType.EXCHANGE_RATE.value or
                                                                        exposure_indexer == IndexerType.EXCHANGE_RATE.value) else None
                )
                
                # Calculate results
                calculator = SwapCalculator(swap_params, hedge_params)
                results = calculator.calculate_total_result()
                
                # Display results
                st.header("Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Exposure Result",
                        f"R$ {results['exposure_result']:,.2f}",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Swap P&L",
                        f"R$ {results['hedge_result']:,.2f}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Total Result / Net Position",
                        f"R$ {results['total_result']:,.2f}",
                        delta=None
                    )
                
                # Display detailed report
                st.header("Detailed Report")
                st.text(calculator.generate_report())


                # After displaying the detailed report, add the plot
                st.header("Position Evolution Over Time")
                
                # Generate time series data
                time_series = calculator.generate_time_series()
                
                # Create the plot
                fig = go.Figure()
                
                # Add traces
                fig.add_trace(go.Scatter(
                    x=time_series['quarters'],
                    y=time_series['exposure'],
                    name='Exposure',
                    line=dict(color='blue'),
                    mode='lines+markers'
                ))
                
                fig.add_trace(go.Scatter(
                    x=time_series['quarters'],
                    y=time_series['asset'],
                    name='Asset Leg',
                    line=dict(color='green'),
                    mode='lines+markers'
                ))
                
                fig.add_trace(go.Scatter(
                    x=time_series['quarters'],
                    y=time_series['liability'],
                    name='Liability Leg',
                    line=dict(color='red'),
                    mode='lines+markers'
                ))
                
                fig.add_trace(go.Scatter(
                    x=time_series['quarters'],
                    y=time_series['net'],
                    name='Net Position',
                    line=dict(color='purple', dash='dash'),
                    mode='lines+markers'
                ))
                
                # Update layout
                fig.update_layout(
                    title='Evolution of Positions Over Time',
                    xaxis_title='Quarters',
                    yaxis_title='Value (R$)',
                    hovermode='x unified',
                    xaxis=dict(
                        tickmode='array',
                        ticktext=[f'Q{q}' for q in time_series['quarters']],
                        tickvals=time_series['quarters']
                    )
                )
                
                # Display the plot
                st.plotly_chart(fig, use_container_width=True)
                
                # Add plot explanation
                st.markdown("""
                ### Plot Explanation
                - **Blue line**: Shows the exposure position over time
                - **Green line**: Shows the asset leg of the hedge over time
                - **Red line**: Shows the liability leg of the hedge over time
                - **Purple dashed line**: Shows the net position (Exposure + Asset - Liability)
                
                The plot shows the evolution of values from inception (Q0) to maturity, with points at each quarter.
                All values start at zero and evolve according to their respective rates and adjustments.
                """)

            # Add some helpful information at the bottom
            st.markdown("""
            ---
            ### How to use this calculator:

            1. Fill in the exposure details on the left side:
            - Select exposure type (Asset/Liability)
            - Enter notional amount
            - Choose indexer type
            - Enter the rate for all indexer types
            - For exchange rate indexer, also enter the initial exchange rate
            - Specify number of quarters

            2. Fill in the hedge details on the right side:
            - Configure both asset and liability legs
            - Enter rates for all legs
            - For exchange rate legs, also enter the cupom cambial
            - If any leg uses exchange rate, specify the exchange rate at maturity

            3. Click "Calculate Swap Results" to see the analysis

            Note: All rates should be entered as decimals (e.g., 0,12 for 12%)
            """)

        # Instructions based on selection
        if st.session_state.selected_option == "Forwards":

            st.title("Forward Contract / FWD Hedging Simulator (Brazilian Practice)")

            st.markdown(r"""
            This simulator demonstrates how a forward contract (FWD) can be used to hedge a liability exposure  under Brazilian practice, where:

            - The market (floating) rate \(L\) is given as the **effective rate for the period** (i.e. the accumulation factor is \(1+L\)).
            - The fixed rate is adjusted using **compound interest**. For an annualized forward rate \(F\), the effective fixed rate for a period of \(Delta\) years is
            \[
            (1+F)^Delta - 1.
            \]

            The FWD payoff is therefore calculated as:
            """)

            st.latex(r'\text{FWD Payoff} = N\left( L - \Big[(1+F)^\Delta - 1\Big] \right)')

            ("""
            where:
            - \(N\) is the notional amount,
            - \(L\) is the effective market (floating) rate for the period,
            - \(F\) is the annualized forward (fixed) rate, and
            - \(Delta\) is the time period (in years).
            """)

            st.header("1. Define Contract Parameters")

            # Notional and period length
            notional = st.number_input("Notional Amount ($)", min_value=10000, step=10000, value=1_000_000)
            delta = st.number_input(r"Time Period \(Delta\) (in years)", min_value=0.01, max_value=2.0, step=0.05, value=0.25)

            # Forward (FWD) fixed rate (annualized)
            F_rate_percent = st.number_input("Forward (FWD) Fixed Rate [%] (annualized)", min_value=0.0, max_value=20.0, step=0.1, value=5.0, help="Cotação de mercado do contrato a termo, ou expectativa de comportamento do DI para o período")
            F = F_rate_percent / 100.0

            # Exposure type: Floating vs. Fixed
            exposure_type = st.selectbox("Hedged Exposure Type", ("Floating Rate Exposure", "Fixed Rate Exposure"), help="Exposição original a ser hedgeada. Será sempre um passivo.")
            if exposure_type == "Fixed Rate Exposure":
                fixed_exposure_rate_percent = st.number_input("Fixed Exposure Rate [%] (annualized)", min_value=0.0, max_value=20.0, step=0.1, value=5.0, help="Taxa pré da exposição original a ser hedgeada.")
                fixed_exposure_rate = fixed_exposure_rate_percent / 100.0

            st.header("2. Vary the Market Rate")

            # Slider for the effective market (floating) rate L for the period.
            # Note: Here L is the effective rate for the entire period (e.g., a quarterly effective rate).
            L_rate_percent = st.slider("Effective Market Rate (L) for the Period [%]", min_value=0.0, max_value=15.0, value=1.5, step=0.1, help = "Taxa efetiva de juros (DI) do período.")
            L = L_rate_percent / 100.0


            # Compute the exposure’s cost
            if exposure_type == "Floating Rate Exposure":

                st.subheader("Calculated Results")
                st.markdown("#### FWD (Forward) Payoff")

                # Calculate the effective fixed rate for the period from the annualized FWD fixed rate, using compound interest.
                effective_fixed_rate = (1 + F)**delta - 1

                # Compute the FWD payoff using the new formula
                FWD_payoff = notional * (L - effective_fixed_rate)
                st.write(f"**FWD Payoff:** ${FWD_payoff:,.2f}")

                # For a floating exposure, the cost is based on the effective rate L.
                exposure_cost = - notional * L
                st.write(f"**Floating Exposure Cost:** ${exposure_cost:,.2f}")

                # The net combined outcome (hedged portfolio)
                net_outcome = exposure_cost + FWD_payoff
                st.markdown("#### Net Hedged Outcome")
                st.write(f"**Net Outcome:** ${net_outcome:,.2f}")


            elif exposure_type == "Fixed Rate Exposure":

                st.subheader("Calculated Results")
                st.markdown("#### FWD (Forward) Payoff")

                # Calculate the effective fixed rate for the period from the annualized FWD fixed rate, using compound interest.
                effective_fixed_rate = (1 + F)**delta - 1

                # Compute the FWD payoff using the new formula
                FWD_payoff = notional * (effective_fixed_rate - L)
                st.write(f"**FWD Payoff:** ${FWD_payoff:,.2f}")

                # For a fixed exposure, adjust the annualized fixed rate using compound interest.
                effective_fixed_exposure_rate = (1 + fixed_exposure_rate)**delta - 1
                exposure_cost = - notional * effective_fixed_exposure_rate
                st.write(f"**Fixed Exposure Cost:** ${exposure_cost:,.2f}")

                # The net combined outcome (hedged portfolio)
                net_outcome = exposure_cost + FWD_payoff
                st.markdown("#### Net Hedged Outcome")
                st.write(f"**Net Outcome:** ${net_outcome:,.2f}")


        
            # Prepare a range of effective market rates for plotting
            L_values = np.linspace(0.0, 0.15, 300)  # from 0% to 15% effective rate for the period

            if exposure_type == "Floating Rate Exposure":
                exposure_costs = - notional * L_values
                FWD_payoffs = notional * (L_values - ((1 + F)**delta - 1))        
            elif exposure_type == "Fixed Rate Exposure":
                exposure_costs = - notional * ((1 + fixed_exposure_rate)**delta - 1) * np.ones_like(L_values)
                FWD_payoffs = notional * (((1 + F)**delta - 1) - L_values)        

            net_outcomes = exposure_costs + FWD_payoffs

            # Create Plotly figure
            import plotly.graph_objects as go

            fig = go.Figure()

            # Add traces with hover templates
            fig.add_trace(go.Scatter(
                x=L_values * 100,
                y=FWD_payoffs,
                mode='lines',
                name='FWD Payoff',
                line=dict(color='#ff7f0e'),  # C1 color equivalent
                hovertemplate='FWD Payoff: $%{y:,.2f}<extra></extra>'
            ))

            fig.add_trace(go.Scatter(
                x=L_values * 100,
                y=exposure_costs,
                mode='lines',
                name='Exposure Cost',
                line=dict(color='#2ca02c'),  # C2 color equivalent
                hovertemplate='Exposure Cost: $%{y:,.2f}<extra></extra>'
            ))

            fig.add_trace(go.Scatter(
                x=L_values * 100,
                y=net_outcomes,
                mode='lines',
                name='Net Outcome',
                line=dict(color='#1f77b4', dash='dash'),  # C0 color with dash
                hovertemplate='Net Outcome: $%{y:,.2f}<extra></extra>'
            ))

            # Add vertical line for current rate
            fig.add_vline(
                x=L_rate_percent, 
                line=dict(color="gray", dash="dash")
            )

            # Add annotation for the vertical line - moved to top of the chart
            fig.add_annotation(
                x=L_rate_percent,
                y=max(max(FWD_payoffs), max(net_outcomes)) * 0.95,  # Position at 95% of the maximum y value
                text=f"Current L = {L_rate_percent:.1f}%",
                showarrow=False,
                yanchor="bottom",
                xanchor="center",
                bgcolor="rgba(255, 255, 255, 0.8)",  # Semi-transparent white background
                bordercolor="black",
                borderwidth=1
            )

            # Update layout
            fig.update_layout(
                xaxis_title="Effective Market Rate (L) for the Period (%)",
                yaxis_title="Amount ($)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified",
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )

            # Display the figure in Streamlit
            st.plotly_chart(fig, use_container_width=True)



















            st.markdown("---")
            st.markdown(r"""
            ### How to Interpret the Simulation

            - **FWD Payoff:**  
            The FWD payoff is computed as:
            """)

            st.latex(r'\text{FWD Payoff} = N\left( L - \Big[(1+F)^\Delta - 1\Big] \right)')

            ("""
            Here, \(L\) is the effective market rate for the period and 
            """)
            
            st.latex(r'(1+F)^\Delta - 1')

            ("""
            
            is the effective fixed rate using compound interest.
            A higher \(L\) compared to the compounded fixed rate yields a positive payoff.

            - **Exposure Cost:**  
            - For a floating–rate exposure, the cost is 
            """)
            
            st.latex(r'N \cdot L \quad (\text{since } L \text{ is the effective rate for the period})')
            
            ("""
            (since \(L\) is the effective rate for the period).  
            - For a fixed–rate exposure, the cost is computed as:
            """)

            st.latex(r'N\left((1+\text{Fixed Rate})^\Delta - 1\right)')

            ("""

            - **Net Outcome:**  
            The net outcome represents the overall effect of the hedge, calculated as the difference between the exposure cost and the FWD payoff.

            Use the sidebar controls to explore how varying the effective market rate \(L\) and adjusting other parameters affects the FWD payoff and the overall hedged outcome.
            """)


            st.markdown("---")
            st.markdown(r"""
            ### Hedging Results for the Selected Values
            """)

            # Create an interactive bar chart that shows only the chosen results.
            categories = ["FWD Payoff", "Exposure Cost", "Net Outcome"]
            values = [FWD_payoff, exposure_cost, net_outcome]

            fig = go.Figure(data=[
                go.Bar(
                    x=categories,
                    y=values,
                    text=[f"${val:,.2f}" for val in values],
                    textposition='auto',
                    marker_color=['royalblue', 'firebrick', 'green']
                )
            ])

            fig.update_layout(
                title="",
                xaxis_title="Metric",
                yaxis_title="Amount ($)",
                hovermode="closest"
            )

            st.plotly_chart(fig, use_container_width=True)

            ##########################################################################################################
            ##########################################################################################################
            
        # Instructions based on selection
        if st.session_state.selected_option == "Futures":
            
            def calculate_theoretical_price(spot_price, rate, days=5):
                T = days/252
                return round(spot_price * (1+rate)**T, 2)

            def simulate_daily_prices(initial_price, final_price, days=5):
                """Generate random daily prices between initial and final price"""
                np.random.seed(42)  # For reproducibility
                prices = [initial_price]
                
                for _ in range(days-1):
                    # Random price between current price and final price
                    min_price = min(initial_price, final_price)
                    max_price = max(initial_price, final_price)
                    daily_price = np.random.uniform(min_price, max_price)
                    prices.append(daily_price)
                
                prices.append(final_price)  # Ensure final price matches settlement price
                return np.array(prices)

            def calculate_margin_account(prices, notional_value, is_asset):
                initial_margin = notional_value * 0.1
                maintenance_margin = initial_margin * 0.5
                num_contracts = notional_value / (prices[0] * 1000)
                
                balance = initial_margin
                margin_history = [(0, balance, initial_margin, maintenance_margin)]
                total_margin_calls = 0
                
                for i in range(1, len(prices)):
                    price_change = prices[i] - prices[i-1]
                    daily_pnl = price_change * 1000 * num_contracts * (1 if is_asset else -1)
                    balance += daily_pnl
                    
                    if balance < maintenance_margin:
                        balance = initial_margin  # Reset to initial margin after call
                        
                    margin_history.append((i, balance, initial_margin, maintenance_margin))
                
                # Calculate final balance considering total P&L
                final_total_pnl = (prices[-1] - prices[0]) * 1000 * num_contracts * (1 if is_asset else -1)
                final_balance = max(0, initial_margin + final_total_pnl)  # Ensure minimum balance of 0
                margin_history[-1] = (len(prices)-1, final_balance, initial_margin, maintenance_margin)
                
                return pd.DataFrame(margin_history, columns=['Day', 'Balance', 'Initial Margin', 'Maintenance Margin'])

            def main():
                st.title("Futures Contract Simulator")
                st.write("### Oil Futures Contract (1,000 barrels)")
                
                st.markdown(r"""
                This simulator shows how a oil future contract (FWD) develops assuming that:

                - The future contract is 1,000 oil barrels
                - The oil contract expires in 5 days 
                - the contract will be kept for 5 trading days until settlement by difference
                - The initial margin is 10% of the notional value
                - The maintenance margin is 50% of the initial margin. Once reached, it must return to the initial margin.
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    notional_value = st.number_input("Notional Value ($)", min_value=1000, value=1000000)
                    contract_type = st.selectbox("Contract Type", ["Hedge", "Speculation"])
                    position_type = st.selectbox("Futures Position (Asset/Buy/Long or Liability/Sell/Short)", ["Asset", "Liability"])
                
                with col2:
                    spot_price = st.number_input("Spot Price ($/barrel)", min_value=1.0, value=80.0)
                    selic_rate = st.number_input("Selic Rate (%)", min_value=0.0, value=5.0) / 100
                    settlement_price = st.number_input("Settlement Price ($/barrel)", min_value=1.0, value=85.0)

                if st.button("Calculate Results"):
                    theoretical_price = calculate_theoretical_price(spot_price, selic_rate)
                    daily_prices = simulate_daily_prices(theoretical_price, settlement_price)
                    
                    is_asset = position_type == "Asset"
                    margin_df = calculate_margin_account(daily_prices, notional_value, is_asset)
                    
                    num_contracts = int(notional_value / (theoretical_price * 1000))  # Truncate to integer
                    futures_pnl = (settlement_price - theoretical_price) * 1000 * num_contracts * (1 if is_asset else -1)
                    hedge_result = -futures_pnl if contract_type == "Hedge" else 0
                    net_result = futures_pnl + hedge_result
                    
                    st.write("### Results")

                    col1, col2, col3 = st.columns(3)
                    with col2:          
                        st.metric("Number of Contracts", f"{num_contracts:.0f} contracts")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Theoretical Price", f"${theoretical_price:.2f}/barrel")
                    with col2:
                        st.metric("Futures P&L", f"${futures_pnl:.2f}")
                    with col3:
                        st.metric("Net Result", f"${net_result:.2f}")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=margin_df['Day'], y=margin_df['Balance'],
                                            mode='lines+markers', name='Balance'))
                    fig.add_trace(go.Scatter(x=margin_df['Day'], y=margin_df['Initial Margin'],
                                            mode='lines', name='Initial Margin', line=dict(dash='dash')))
                    fig.add_trace(go.Scatter(x=margin_df['Day'], y=margin_df['Maintenance Margin'],
                                            mode='lines', name='Maintenance Margin', line=dict(dash='dot')))
                    
                    fig.update_layout(title='Margin Account Evolution',
                                    xaxis_title='Day',
                                    yaxis_title='Balance ($)',
                                    height=500)
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.write("### Understanding the Results")
                    st.write(f"""
                    - The theoretical futures price (${theoretical_price:.2f}) is calculated using the non-arbitrage principle
                    - Daily mark-to-market settlements affect the margin account balance
                    - Initial margin is ${notional_value * 0.1:.0f} (10% of notional value)
                    - Maintenance margin is ${notional_value * 0.05:.0f} (50% of initial margin)
                    - The {'asset' if is_asset else 'liability'} position in futures {'gained' if futures_pnl > 0 else 'lost'} ${abs(futures_pnl):.2f}
                    """)
                    
                    if contract_type == "Hedge":
                        st.write(f"- Future P&L: ${net_result:.2f}")

            if __name__ == "__main__":
                main()

        # Instructions based on selection
        if st.session_state.selected_option == "Options":

            # Custom CSS for better styling
            st.markdown("""
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
            """, unsafe_allow_html=True)

            # Function to calculate option price using Black-Scholes model
            def black_scholes(S, K, T, r, sigma, option_type):
                """
                Calculate option price using Black-Scholes model
                
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

            # Function to calculate option payoff at expiration
            def option_payoff(S_T, K, option_type, position):
                """
                Calculate option payoff at expiration
                
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

            # Function to calculate option profit at expiration
            def option_profit(S_T, K, premium, option_type, position):
                """
                Calculate option profit at expiration
                
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

            # Function to calculate break-even point
            def break_even_point(K, premium, option_type, position):
                """
                Calculate break-even point
                
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


            # Create tabs for different sections of the app
            tabs = st.tabs(["Introduction", "Option Simulator", "Option Strategies", "Educational Resources"])

            # Introduction Tab
            with tabs[0]:
                st.title("Options Teaching Tool")
                st.markdown("### Welcome to the Interactive Options Teaching Tool!")
                
                st.markdown("""
                This tool is designed to help you understand and visualize option strategies, including:
                
                - **American vs European Options**: Understand the differences between these two option styles
                - **Calls vs Puts**: Learn how these option types work
                - **Buying vs Selling**: Visualize the payoff and profit for different positions
                
                Use the simulator tab to interact with different option parameters and see how they affect option pricing and profitability.
                """)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### European vs American Options")
                    st.markdown("""
                    - **European Options**: Can only be exercised at expiration
                    - **American Options**: Can be exercised any time before expiration
                    
                    This simulator focuses primarily on European options for simplicity in teaching the core concepts.
                    """)
                
                with col2:
                    st.markdown("### Calls vs Puts")
                    st.markdown("""
                    - **Call Option**: Gives the buyer the right (but not obligation) to buy the underlying asset at the strike price
                    - **Put Option**: Gives the buyer the right (but not obligation) to sell the underlying asset at the strike price
                    """)
                
                st.markdown("### Buying vs Selling")
                st.markdown("""
                - **Buying Options (Long Position)**: 
                - Limited risk (premium paid)
                - Unlimited potential profit (for calls)
                - Limited potential profit (for puts)
                
                - **Selling Options (Short Position)**:
                - Limited potential profit (premium received)
                - Unlimited potential loss (for calls)
                - Limited potential loss (for puts)
                """)
                
                st.markdown("### How to Use This Tool")
                st.markdown("""
                1. Go to the Option Simulator tab
                2. Select your option parameters
                3. View the payoff and profit diagrams
                4. Adjust parameters to see how they affect option valuation
                
                The tool will also provide educational explanations based on your selections.
                """)

            # Option Simulator Tab
            with tabs[1]:
                st.title("Option Simulator")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("### Option Parameters")
                    
                    # Option Type Selection
                    option_style = st.radio("Option Style", ["European", "American"], index=0, help="European options can only be exercised at expiration. American options can be exercised any time before expiration.")
                    
                    position = st.radio("Position", ["Buy", "Sell"], index=0, help="Buy (long) or Sell (short) the option")
                    
                    option_type = st.radio("Option Type", ["Call", "Put"], index=0, help="Call gives right to buy. Put gives right to sell.")
                    
                    # Market and Contract Parameters
                    st.markdown("### Market Parameters")
                    
                    S = st.slider("Current Price of Underlying Asset (S)", min_value=10.0, max_value=200.0, value=100.0, step=1.0, help="Current market price of the underlying asset")
                    
                    K = st.slider("Strike Price (K)", min_value=10.0, max_value=200.0, value=100.0, step=1.0, help="The price at which the option can be exercised")
                    
                    T = st.slider("Time to Maturity (years)", min_value=0.1, max_value=2.0, value=1.0, step=0.1, help="Time until the option expires (in years)")
                    
                    sigma = st.slider("Volatility (σ, %)", min_value=5.0, max_value=100.0, value=20.0, step=5.0, help="Annualized volatility of the underlying asset") / 100
                    
                    r = st.slider("Risk-Free Interest Rate (r, %)", min_value=0.0, max_value=10.0, value=2.0, step=0.5, help="Annual risk-free interest rate") / 100
                    
                    # Calculate option premium
                    premium = black_scholes(S, K, T, r, sigma, option_type.lower())
                    
                    st.markdown("### Option Premium")
                    st.markdown(f"#### ${premium:.2f}")
                    
                    if option_style == "American" and option_type == "Put" and K > S:
                        st.warning("Note: For American put options when strike price > current price, early exercise might be optimal. The Black-Scholes model may underestimate the premium.")
                
                with col2:
                    st.markdown("### Payoff and Profit Diagrams")
                    
                    # Generate price range for x-axis
                    range_percent = 0.5
                    price_min = max(1, K * (1 - range_percent))
                    price_max = K * (1 + range_percent)
                    
                    # Create price array
                    prices = np.linspace(price_min, price_max, 100)
                    
                    # Calculate payoffs and profits
                    payoffs = [option_payoff(price, K, option_type.lower(), position.lower()) for price in prices]
                    profits = [option_profit(price, K, premium, option_type.lower(), position.lower()) for price in prices]
                    
                    # Calculate break-even point
                    be_point = break_even_point(K, premium, option_type.lower(), position.lower())
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Payoff': payoffs,
                        'Profit': profits
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
                        name='Strike Price',
                        marker=dict(color='red', size=10)
                    ))
                    
                    fig1.update_layout(
                        title=f"Payoff Diagram: {position} {option_type} Option",
                        xaxis_title="Underlying Price at Expiration",
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
                        name='Profit',
                        line=dict(color='green', width=2)
                    ))
                    
                    fig2.add_trace(go.Scatter(
                        x=[K],
                        y=[option_profit(K, K, premium, option_type.lower(), position.lower())],
                        mode='markers',
                        name='Strike Price',
                        marker=dict(color='red', size=10)
                    ))
                    
                    fig2.add_trace(go.Scatter(
                        x=[be_point],
                        y=[0],
                        mode='markers',
                        name='Break-Even Point',
                        marker=dict(color='purple', size=10)
                    ))
                    
                    fig2.update_layout(
                        title=f"Profit Diagram: {position} {option_type} Option",
                        xaxis_title="Underlying Price at Expiration",
                        yaxis_title="Profit",
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
                st.markdown("### Explanation")
                
                st.markdown(f"""
                #### {position} {option_type} Option Explanation
                
                - **Premium**: ${premium:.2f}
                - **Break-Even Point**: ${be_point:.2f}
                """)
                
                if option_type == "Call":
                    if position == "Buy":
                        st.markdown("""
                        **Strategy Explanation:**
                        - You're paying a premium for the right to buy the underlying at the strike price
                        - Profit when the underlying price rises above the strike price plus premium
                        - Maximum risk is limited to the premium paid
                        - Maximum profit is theoretically unlimited (as the stock price can rise indefinitely)
                        """)
                    else:  # Sell
                        st.markdown("""
                        **Strategy Explanation:**
                        - You're receiving a premium for the obligation to sell the underlying at the strike price
                        - Profit when the underlying price stays below the strike price plus premium
                        - Maximum profit is limited to the premium received
                        - Maximum risk is theoretically unlimited (as the stock price can rise indefinitely)
                        """)
                else:  # Put
                    if position == "Buy":
                        st.markdown("""
                        **Strategy Explanation:**
                        - You're paying a premium for the right to sell the underlying at the strike price
                        - Profit when the underlying price falls below the strike price minus premium
                        - Maximum risk is limited to the premium paid
                        - Maximum profit is limited (as the stock price can only fall to zero)
                        """)
                    else:  # Sell
                        st.markdown("""
                        **Strategy Explanation:**
                        - You're receiving a premium for the obligation to buy the underlying at the strike price
                        - Profit when the underlying price stays above the strike price minus premium
                        - Maximum profit is limited to the premium received
                        - Maximum risk is limited (as the stock price can only fall to zero)
                        """)
                
                # Option Greeks Calculation
                st.markdown("### Option Greeks")
                
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
                
                if position == "Sell":
                    delta = -delta
                    gamma = -gamma
                    theta = -theta
                    vega = -vega
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Delta", f"{delta:.4f}")
                    st.caption("Change in option price for a $1 change in underlying")
                
                with col2:
                    st.metric("Gamma", f"{gamma:.4f}")
                    st.caption("Rate of change of Delta for a $1 change in underlying")
                
                with col3:
                    st.metric("Theta", f"{theta:.4f}")
                    st.caption("Daily time decay (change in option price as time passes)")
                
                with col4:
                    st.metric("Vega", f"{vega:.4f}")
                    st.caption("Change in option price for a 1% change in volatility")


            # Option Strategies Tab
            with tabs[2]:
                st.title("Option Strategies")
                
                st.markdown("""
                ### Explore Option Strategies Based on Market Outlook
                
                Option strategies can be tailored to different market expectations. Select your market outlook and 
                explore suitable strategies for that scenario.
                """)
                
                # Market outlook selection
                market_outlook = st.selectbox(
                    "Select Your Market Outlook",
                    [
                        "Bullish (Expecting prices to rise significantly)",
                        "Slightly Bullish (Expecting moderate upward movement)",
                        "Bearish (Expecting prices to fall significantly)",
                        "Slightly Bearish (Expecting moderate downward movement)",
                        "Neutral (Expecting prices to stay in a range)",
                        "Volatile (Expecting large price movements in either direction)",
                        "Low Volatility (Expecting minimal price movement)"
                    ]
                )
                
                # Dictionary mapping market outlooks to suitable strategies
                strategy_map = {
                    "Bullish (Expecting prices to rise significantly)": [
                        "Long Call", 
                        "Bull Call Spread",
                        "Risk Reversal (Buy Call, Sell Put)"
                    ],
                    "Slightly Bullish (Expecting moderate upward movement)": [
                        "Covered Call", 
                        "Bull Put Spread",
                        "Long Call Vertical Spread"
                    ],
                    "Bearish (Expecting prices to fall significantly)": [
                        "Long Put", 
                        "Bear Put Spread",
                        "Risk Reversal (Buy Put, Sell Call)"
                    ],
                    "Slightly Bearish (Expecting moderate downward movement)": [
                        "Bear Call Spread", 
                        "Covered Put",
                        "Short Call"
                    ],
                    "Neutral (Expecting prices to stay in a range)": [
                        "Iron Condor", 
                        "Short Straddle",
                        "Short Strangle",
                        "Butterfly Spread"
                    ],
                    "Volatile (Expecting large price movements in either direction)": [
                        "Long Straddle", 
                        "Long Strangle",
                        "Long Guts"
                    ],
                    "Low Volatility (Expecting minimal price movement)": [
                        "Iron Butterfly", 
                        "Short Straddle",
                        "Calendar Spread"
                    ]
                }
                
                # Strategy selection based on market outlook
                strategy_options = strategy_map[market_outlook]
                selected_strategy = st.selectbox("Select a Strategy", strategy_options)
                
                # Parameters for all strategies
                st.markdown("### Strategy Parameters")
                col1, col2 = st.columns(2)
                
                with col1:
                    S = st.slider("Current Price of Underlying Asset (S)", min_value=10.0, max_value=200.0, value=100.0, step=1.0, key="strat_S")
                    sigma = st.slider("Volatility (σ, %)", min_value=5.0, max_value=100.0, value=20.0, step=5.0, key="strat_sigma") / 100
                
                with col2:
                    T = st.slider("Time to Maturity (years)", min_value=0.1, max_value=2.0, value=1.0, step=0.1, key="strat_T")
                    r = st.slider("Risk-Free Interest Rate (r, %)", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="strat_r") / 100
                
                # Strategy-specific parameters and functions
                if "Long Call" in selected_strategy:
                    K_call = st.slider("Call Strike Price", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="K_call")
                    call_premium = black_scholes(S, K_call, T, r, sigma, "call")
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Long Call Strategy
                    
                    **Description:** Purchase a call option, giving you the right to buy the underlying at the strike price.
                    
                    **Parameters:**
                    - Call Strike Price: ${K_call:.2f}
                    - Call Premium: ${call_premium:.2f}
                    
                    **Maximum Risk:** Limited to premium paid (${call_premium:.2f})
                    
                    **Maximum Reward:** Unlimited (as the underlying price rises)
                    
                    **Breakeven Point:** Strike Price + Premium = ${K_call + call_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_call * 0.5), K_call * 1.5, 100)
                    
                    # Calculate payoffs and profits
                    payoffs = [max(0, price - K_call) for price in prices]
                    profits = [max(0, price - K_call) - call_premium for price in prices]
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Payoff': payoffs,
                        'Profit': profits
                    })
                    
                elif "Long Put" in selected_strategy:
                    K_put = st.slider("Put Strike Price", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="K_put")
                    put_premium = black_scholes(S, K_put, T, r, sigma, "put")
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Long Put Strategy
                    
                    **Description:** Purchase a put option, giving you the right to sell the underlying at the strike price.
                    
                    **Parameters:**
                    - Put Strike Price: ${K_put:.2f}
                    - Put Premium: ${put_premium:.2f}
                    
                    **Maximum Risk:** Limited to premium paid (${put_premium:.2f})
                    
                    **Maximum Reward:** Limited but substantial (Strike Price - Premium = ${K_put - put_premium:.2f})
                    
                    **Breakeven Point:** Strike Price - Premium = ${K_put - put_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_put * 0.5), K_put * 1.5, 100)
                    
                    # Calculate payoffs and profits
                    payoffs = [max(0, K_put - price) for price in prices]
                    profits = [max(0, K_put - price) - put_premium for price in prices]
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Payoff': payoffs,
                        'Profit': profits
                    })
                    
                elif "Short Call" in selected_strategy:
                    K_call = st.slider("Call Strike Price", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="K_call")
                    call_premium = black_scholes(S, K_call, T, r, sigma, "call")
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Short Call Strategy
                    
                    **Description:** Sell a call option, obligating you to sell the underlying at the strike price if the option is exercised.
                    
                    **Parameters:**
                    - Call Strike Price: ${K_call:.2f}
                    - Call Premium Received: ${call_premium:.2f}
                    
                    **Maximum Risk:** Unlimited (as the underlying price rises)
                    
                    **Maximum Reward:** Limited to premium received (${call_premium:.2f})
                    
                    **Breakeven Point:** Strike Price + Premium = ${K_call + call_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_call * 0.5), K_call * 1.5, 100)
                    
                    # Calculate payoffs and profits
                    payoffs = [-max(0, price - K_call) for price in prices]
                    profits = [call_premium - max(0, price - K_call) for price in prices]
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Payoff': payoffs,
                        'Profit': profits
                    })
                    
                elif "Short Put" in selected_strategy:
                    K_put = st.slider("Put Strike Price", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="K_put")
                    put_premium = black_scholes(S, K_put, T, r, sigma, "put")
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Short Put Strategy
                    
                    **Description:** Sell a put option, obligating you to buy the underlying at the strike price if the option is exercised.
                    
                    **Parameters:**
                    - Put Strike Price: ${K_put:.2f}
                    - Put Premium Received: ${put_premium:.2f}
                    
                    **Maximum Risk:** Limited but substantial (Strike Price - Premium = ${K_put - put_premium:.2f})
                    
                    **Maximum Reward:** Limited to premium received (${put_premium:.2f})
                    
                    **Breakeven Point:** Strike Price - Premium = ${K_put - put_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_put * 0.5), K_put * 1.5, 100)
                    
                    # Calculate payoffs and profits
                    payoffs = [-max(0, K_put - price) for price in prices]
                    profits = [put_premium - max(0, K_put - price) for price in prices]
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Payoff': payoffs,
                        'Profit': profits
                    })
                    
                elif "Covered Call" in selected_strategy:
                    K_call = st.slider("Call Strike Price", min_value=50.0, max_value=150.0, value=110.0, step=5.0, key="K_call")
                    call_premium = black_scholes(S, K_call, T, r, sigma, "call")
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Covered Call Strategy
                    
                    **Description:** Own the underlying asset and sell a call option against it.
                    
                    **Parameters:**
                    - Current Stock Price: ${S:.2f}
                    - Call Strike Price: ${K_call:.2f}
                    - Call Premium Received: ${call_premium:.2f}
                    
                    **Maximum Risk:** Substantial (Stock Price - Premium = ${S - call_premium:.2f}) if the stock price falls to zero
                    
                    **Maximum Reward:** Limited (Call Premium + (Strike - Stock Price) = ${call_premium + (K_call - S):.2f})
                    
                    **Breakeven Point:** Stock Price - Premium = ${S - call_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, S * 0.5), S * 1.5, 100)
                    
                    # Calculate profits
                    profits = []
                    for price in prices:
                        # Stock component: price change
                        stock_profit = price - S
                        # Short call component
                        call_profit = call_premium - max(0, price - K_call)
                        # Total profit
                        total_profit = stock_profit + call_profit
                        profits.append(total_profit)
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Profit': profits
                    })
                    
                elif "Protective Put" in selected_strategy:
                    K_put = st.slider("Put Strike Price", min_value=50.0, max_value=150.0, value=90.0, step=5.0, key="K_put")
                    put_premium = black_scholes(S, K_put, T, r, sigma, "put")
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Protective Put Strategy
                    
                    **Description:** Own the underlying asset and buy a put option as insurance.
                    
                    **Parameters:**
                    - Current Stock Price: ${S:.2f}
                    - Put Strike Price: ${K_put:.2f}
                    - Put Premium Paid: ${put_premium:.2f}
                    
                    **Maximum Risk:** Limited to (Stock Price - Strike Price + Premium = ${S - K_put + put_premium:.2f}) if price drops below strike
                    
                    **Maximum Reward:** Unlimited upside (minus the put premium)
                    
                    **Breakeven Point:** Stock Price + Premium = ${S + put_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, S * 0.5), S * 1.5, 100)
                    
                    # Calculate profits
                    profits = []
                    for price in prices:
                        # Stock component: price change
                        stock_profit = price - S
                        # Long put component
                        put_profit = max(0, K_put - price) - put_premium
                        # Total profit
                        total_profit = stock_profit + put_profit
                        profits.append(total_profit)
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Profit': profits
                    })
                    
                elif "Bull Call Spread" in selected_strategy:
                    K_long = st.slider("Long Call Strike Price", min_value=50.0, max_value=150.0, value=95.0, step=5.0, key="K_long")
                    K_short = st.slider("Short Call Strike Price", min_value=K_long, max_value=150.0, value=110.0, step=5.0, key="K_short")
                    
                    # Calculate premiums
                    long_premium = black_scholes(S, K_long, T, r, sigma, "call")
                    short_premium = black_scholes(S, K_short, T, r, sigma, "call")
                    net_premium = long_premium - short_premium
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Bull Call Spread Strategy
                    
                    **Description:** Buy a call option at a lower strike price and sell a call at a higher strike price.
                    
                    **Parameters:**
                    - Long Call Strike Price: ${K_long:.2f} (Premium: ${long_premium:.2f})
                    - Short Call Strike Price: ${K_short:.2f} (Premium: ${short_premium:.2f})
                    - Net Premium Paid: ${net_premium:.2f}
                    
                    **Maximum Risk:** Limited to net premium paid (${net_premium:.2f})
                    
                    **Maximum Reward:** Limited to difference between strikes minus net premium (${K_short - K_long - net_premium:.2f})
                    
                    **Breakeven Point:** Lower Strike + Net Premium = ${K_long + net_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_long * 0.8), K_short * 1.2, 100)
                    
                    # Calculate profits
                    profits = []
                    for price in prices:
                        # Long call profit
                        long_profit = max(0, price - K_long) - long_premium
                        # Short call profit
                        short_profit = short_premium - max(0, price - K_short)
                        # Total profit
                        total_profit = long_profit + short_profit
                        profits.append(total_profit)
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Profit': profits
                    })
                    
                elif "Bear Put Spread" in selected_strategy:
                    K_long = st.slider("Long Put Strike Price", min_value=50.0, max_value=150.0, value=110.0, step=5.0, key="K_long")
                    K_short = st.slider("Short Put Strike Price", min_value=50.0, max_value=K_long, value=95.0, step=5.0, key="K_short")
                    
                    # Calculate premiums
                    long_premium = black_scholes(S, K_long, T, r, sigma, "put")
                    short_premium = black_scholes(S, K_short, T, r, sigma, "put")
                    net_premium = long_premium - short_premium
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Bear Put Spread Strategy
                    
                    **Description:** Buy a put option at a higher strike price and sell a put at a lower strike price.
                    
                    **Parameters:**
                    - Long Put Strike Price: ${K_long:.2f} (Premium: ${long_premium:.2f})
                    - Short Put Strike Price: ${K_short:.2f} (Premium: ${short_premium:.2f})
                    - Net Premium Paid: ${net_premium:.2f}
                    
                    **Maximum Risk:** Limited to net premium paid (${net_premium:.2f})
                    
                    **Maximum Reward:** Limited to difference between strikes minus net premium (${K_long - K_short - net_premium:.2f})
                    
                    **Breakeven Point:** Higher Strike - Net Premium = ${K_long - net_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_short * 0.8), K_long * 1.2, 100)
                    
                    # Calculate profits
                    profits = []
                    for price in prices:
                        # Long put profit
                        long_profit = max(0, K_long - price) - long_premium
                        # Short put profit
                        short_profit = short_premium - max(0, K_short - price)
                        # Total profit
                        total_profit = long_profit + short_profit
                        profits.append(total_profit)
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Profit': profits
                    })
                    
                elif "Long Straddle" in selected_strategy:
                    K = st.slider("Strike Price", min_value=50.0, max_value=150.0, value=100.0, step=5.0, key="K_straddle")
                    
                    # Calculate premiums
                    call_premium = black_scholes(S, K, T, r, sigma, "call")
                    put_premium = black_scholes(S, K, T, r, sigma, "put")
                    total_premium = call_premium + put_premium
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Long Straddle Strategy
                    
                    **Description:** Buy both a call and a put at the same strike price, profiting from large price movements in either direction.
                    
                    **Parameters:**
                    - Strike Price: ${K:.2f}
                    - Call Premium: ${call_premium:.2f}
                    - Put Premium: ${put_premium:.2f}
                    - Total Premium: ${total_premium:.2f}
                    
                    **Maximum Risk:** Limited to total premium paid (${total_premium:.2f})
                    
                    **Maximum Reward:** Unlimited (as price moves far from strike in either direction)
                    
                    **Breakeven Points:** 
                    - Upside: Strike + Total Premium = ${K + total_premium:.2f}
                    - Downside: Strike - Total Premium = ${K - total_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K * 0.5), K * 1.5, 100)
                    
                    # Calculate profits
                    profits = []
                    for price in prices:
                        # Call profit
                        call_profit = max(0, price - K) - call_premium
                        # Put profit
                        put_profit = max(0, K - price) - put_premium
                        # Total profit
                        total_profit = call_profit + put_profit
                        profits.append(total_profit)
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Profit': profits
                    })
                    
                elif "Iron Condor" in selected_strategy:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        K_put_long = st.slider("Long Put Strike", min_value=50.0, max_value=90.0, value=80.0, step=5.0, key="K_put_long")
                        K_put_short = st.slider("Short Put Strike", min_value=K_put_long, max_value=100.0, value=90.0, step=5.0, key="K_put_short")
                    
                    with col2:
                        K_call_short = st.slider("Short Call Strike", min_value=K_put_short, max_value=150.0, value=110.0, step=5.0, key="K_call_short")
                        K_call_long = st.slider("Long Call Strike", min_value=K_call_short, max_value=150.0, value=120.0, step=5.0, key="K_call_long")
                    
                    # Calculate premiums
                    put_long_premium = black_scholes(S, K_put_long, T, r, sigma, "put")
                    put_short_premium = black_scholes(S, K_put_short, T, r, sigma, "put")
                    call_short_premium = black_scholes(S, K_call_short, T, r, sigma, "call")
                    call_long_premium = black_scholes(S, K_call_long, T, r, sigma, "call")
                    
                    net_premium = put_short_premium + call_short_premium - put_long_premium - call_long_premium
                    max_profit = net_premium
                    max_risk = (K_put_short - K_put_long) - net_premium
                    
                    # Display strategy information
                    st.markdown(f"""
                    ### Iron Condor Strategy
                    
                    **Description:** A market-neutral strategy that profits when the underlying price stays within a range.
                    
                    **Parameters:**
                    - Long Put Strike: ${K_put_long:.2f} (Premium: ${put_long_premium:.2f})
                    - Short Put Strike: ${K_put_short:.2f} (Premium: ${put_short_premium:.2f})
                    - Short Call Strike: ${K_call_short:.2f} (Premium: ${call_short_premium:.2f})
                    - Long Call Strike: ${K_call_long:.2f} (Premium: ${call_long_premium:.2f})
                    - Net Premium Received: ${net_premium:.2f}
                    
                    **Maximum Risk:** Limited to width of either spread minus net premium (${max_risk:.2f})
                    
                    **Maximum Reward:** Limited to net premium received (${max_profit:.2f})
                    
                    **Breakeven Points:** 
                    - Lower: Short Put Strike - Net Premium = ${K_put_short - net_premium:.2f}
                    - Upper: Short Call Strike + Net Premium = ${K_call_short + net_premium:.2f}
                    """)
                    
                    # Generate price range for visualization
                    prices = np.linspace(max(1, K_put_long * 0.8), K_call_long * 1.2, 100)
                    
                    # Calculate profits
                    profits = []
                    for price in prices:
                        # Long put profit
                        put_long_profit = max(0, K_put_long - price) - put_long_premium
                        # Short put profit
                        put_short_profit = put_short_premium - max(0, K_put_short - price)
                        # Short call profit
                        call_short_profit = call_short_premium - max(0, price - K_call_short)
                        # Long call profit
                        call_long_profit = max(0, price - K_call_long) - call_long_premium
                        # Total profit
                        total_profit = put_long_profit + put_short_profit + call_short_profit + call_long_profit
                        profits.append(total_profit)
                    
                    # Create DataFrame for displaying data
                    df = pd.DataFrame({
                        'Underlying Price': prices,
                        'Profit': profits
                    })
                
                # Display chart for all strategies
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['Underlying Price'],
                    y=df['Profit'],
                    mode='lines',
                    name='Profit',
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
                    name='Current Price',
                    marker=dict(color='blue', size=10)
                ))
                
                fig.update_layout(
                    title=f"{selected_strategy} - Profit/Loss Diagram",
                    xaxis_title="Underlying Price at Expiration",
                    yaxis_title="Profit/Loss",
                    height=500,
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Strategy advantages and disadvantages
                st.markdown("### Strategy Advantages and Disadvantages")
                
                advantages = {
                    "Long Call": [
                        "Unlimited profit potential as price rises",
                        "Limited risk (premium paid)",
                        "Leverage (control larger position with less capital)",
                        "No downside risk beyond premium"
                    ],
                    "Long Put": [
                        "Profits from downward price movement",
                        "Limited risk (premium paid)",
                        "Can be used as portfolio insurance",
                        "Leverage (control larger position with less capital)"
                    ],
                    "Short Call": [
                        "Profits from falling, flat, or slightly rising prices",
                        "Premium received upfront",
                        "Can be used to generate income on existing positions",
                        "Time decay works in your favor"
                    ],
                    "Short Put": [
                        "Profits from rising, flat, or slightly falling prices",
                        "Premium received upfront",
                        "Can be used to acquire stock at lower prices",
                        "Time decay works in your favor"
                    ],
                    "Covered Call": [
                        "Generate income from existing stock positions",
                        "Provides some downside protection (premium reduces cost basis)",
                        "Can increase overall portfolio yield",
                        "Benefits from time decay"
                    ],
                    "Protective Put": [
                        "Limits downside risk on existing stock positions",
                        "Allows participation in upside movement",
                        "Acts as portfolio insurance",
                        "Known maximum loss"
                    ],
                    "Bull Call Spread": [
                        "Lower cost than buying a call outright",
                        "Defined risk and reward",
                        "Lower breakeven point than a long call",
                        "Profitable in moderately bullish markets"
                    ],
                    "Bear Put Spread": [
                        "Lower cost than buying a put outright",
                        "Defined risk and reward",
                        "Profitable in moderately bearish markets",
                        "Short put helps offset cost of long put"
                    ],
                    "Long Straddle": [
                        "Profits from large moves in either direction",
                        "Limited risk (total premium paid)",
                        "Unlimited profit potential",
                        "Good for uncertain market conditions or ahead of major events"
                    ],
                    "Iron Condor": [
                        "Profits in range-bound markets",
                        "Premium received upfront",
                        "Defined risk and reward",
                        "Benefits from time decay"
                    ]
                }
                
                disadvantages = {
                    "Long Call": [
                        "Loses value as time passes (time decay)",
                        "Requires significant price movement to be profitable",
                        "Volatility decrease hurts position value",
                        "Can expire worthless (100% loss of premium)"
                    ],
                    "Long Put": [
                        "Loses value as time passes (time decay)",
                        "Requires significant price movement to be profitable",
                        "Volatility decrease hurts position value",
                        "Can expire worthless (100% loss of premium)"
                    ],
                    "Short Call": [
                        "Unlimited risk if price rises sharply",
                        "Requires margin (collateral)",
                        "Early assignment risk (for American options)",
                        "Volatility increase hurts position"
                    ],
                    "Short Put": [
                        "Substantial risk if price falls sharply",
                        "Potential obligation to buy shares at strike price",
                        "Requires margin (collateral)",
                        "Volatility increase hurts position"
                    ],
                    "Covered Call": [
                        "Caps upside potential",
                        "Limited downside protection",
                        "Opportunity cost if stock rises significantly",
                        "Stock can still decline substantially"
                    ],
                    "Protective Put": [
                        "Cost of protection reduces overall returns",
                        "Can be expensive during high volatility",
                        "Loses value due to time decay",
                        "Requires continuous renewal (ongoing cost)"
                    ],
                    "Bull Call Spread": [
                        "Limited profit potential",
                        "Requires moderate price increase to be profitable",
                        "Time decay works against position",
                        "Both options can expire worthless"
                    ],
                    "Bear Put Spread": [
                        "Limited profit potential",
                        "Requires moderate price decrease to be profitable",
                        "Time decay works against position",
                        "Both options can expire worthless"
                    ],
                    "Long Straddle": [
                        "Expensive strategy (two premiums)",
                        "Requires significant price movement in either direction",
                        "Suffers from time decay",
                        "Volatility decrease hurts position value"
                    ],
                    "Iron Condor": [
                        "Limited profit potential",
                        "Risk of significant loss if price moves beyond either short strike",
                        "Multiple legs increase transaction costs",
                        "Complex to manage"
                    ]
                }
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Advantages")
                    for adv in advantages.get(selected_strategy, ["No specific advantages listed"]):
                        st.markdown(f"- {adv}")
                
                with col2:
                    st.markdown("#### Disadvantages")
                    for dis in disadvantages.get(selected_strategy, ["No specific disadvantages listed"]):
                        st.markdown(f"- {dis}")
                
                # When to use this strategy
                st.markdown("### When to Use This Strategy")
                
                when_to_use = {
                    "Long Call": """
                    - When you're strongly bullish on the underlying asset
                    - When you expect a significant price increase
                    - When you want to limit risk while maintaining upside exposure
                    - When you want leverage without borrowing money
                    - Before anticipated positive events (earnings, product launches, etc.)
                    """,
                    "Long Put": """
                    - When you're strongly bearish on the underlying asset
                    - When you expect a significant price decrease
                    - When you want to limit risk while gaining from downside movement
                    - When you want to hedge existing long positions without selling them
                    - Before anticipated negative events (earnings, sector weakness, etc.)
                    """,
                    "Short Call": """
                    - When you're neutral to slightly bearish on the underlying
                    - When you want to generate income from option premium
                    - When you believe volatility is overpriced
                    - When you're willing to sell shares (or get short) at the strike price
                    - When you expect time decay to work in your favor
                    """,
                    "Short Put": """
                    - When you're neutral to slightly bullish on the underlying
                    - When you want to generate income from option premium
                    - When you believe volatility is overpriced
                    - When you're willing to buy shares at the strike price
                    - When you expect time decay to work in your favor
                    """,
                    "Covered Call": """
                    - When you already own the underlying stock
                    - When you're neutral to slightly bullish on the stock
                    - When you want to generate additional income from your holdings
                    - When you're willing to sell shares at the strike price
                    - In low volatility environments where you want to enhance returns
                    """,
                    "Protective Put": """
                    - When you own the underlying stock and want downside protection
                    - During periods of uncertainty or anticipated volatility
                    - When you want to protect gains in appreciated positions
                    - When you want to retain upside potential while limiting downside risk
                    - As insurance against unforeseen negative events
                    """,
                    "Bull Call Spread": """
                    - When you're moderately bullish on the underlying
                    - When you want to reduce the cost of buying calls
                    - When you're willing to cap your upside potential to reduce cost
                    - When implied volatility is high (making outright calls expensive)
                    - When you want defined risk and defined reward
                    """,
                    "Bear Put Spread": """
                    - When you're moderately bearish on the underlying
                    - When you want to reduce the cost of buying puts
                    - When you're willing to cap your profit potential to reduce cost
                    - When implied volatility is high (making outright puts expensive)
                    - When you want defined risk and defined reward
                    """,
                    "Long Straddle": """
                    - When you expect a significant price move but are uncertain about direction
                    - Before major news events, earnings announcements, or product launches
                    - When implied volatility is low (making the strategy more affordable)
                    - When you anticipate an increase in volatility
                    - When you want to profit from a breakout from a trading range
                    """,
                    "Iron Condor": """
                    - When you expect the underlying to remain within a specific price range
                    - When implied volatility is high (making the sold options more valuable)
                    - When you want to profit from time decay
                    - In low volatility environments where prices tend to move sideways
                    - When you want defined risk and defined reward
                    """
                }
                
                st.markdown(when_to_use.get(selected_strategy, "No specific guidance available for this strategy."))
                
                # Common mistakes section
                st.markdown("### Common Mistakes to Avoid")
                
                common_mistakes = {
                    "Long Call": """
                    - Buying options with too little time to expiration (severe time decay)
                    - Overpaying for options during high volatility periods
                    - Choosing strikes that are too far out-of-the-money
                    - Allocating too much capital to speculative options
                    - Not considering the impact of volatility changes
                    """,
                    "Long Put": """
                    - Buying puts after a market has already declined significantly
                    - Overpaying for options during high volatility periods
                    - Choosing strikes that are too far out-of-the-money
                    - Using puts inefficiently for hedging (wrong strike or expiration)
                    - Not accounting for dividends when applicable
                    """,
                    "Short Call": """
                    - Not understanding the unlimited risk potential
                    - Selling calls on high-volatility stocks without proper risk management
                    - Not having a plan for when the underlying rises sharply
                    - Ignoring early assignment risk near ex-dividend dates
                    - Trading illiquid options with wide bid-ask spreads
                    """,
                    "Short Put": """
                    - Underestimating potential losses if the underlying declines sharply
                    - Not having sufficient capital to buy shares if assigned
                    - Selling puts on securities you don't want to own
                    - Chasing premium by selling puts on high-volatility stocks
                    - Not having an exit strategy for adverse price movements
                    """,
                    "Covered Call": """
                    - Selling calls at strikes below your cost basis (risking losses if called)
                    - Focusing only on premium and ignoring underlying stock quality
                    - Selling calls with too little premium to compensate for capped upside
                    - Not considering ex-dividend dates when selecting expirations
                    - Failing to adjust strategy during sharp market declines
                    """,
                    "Protective Put": """
                    - Overpaying for protection (especially during high volatility)
                    - Using inappropriate strike prices (too far OTM provides little protection)
                    - Not properly timing protection (buying after market has already fallen)
                    - Not considering cost-efficient alternatives (e.g., collars, spreads)
                    - Keeping protection in place too long without reassessing
                    """,
                    "Bull Call Spread": """
                    - Setting strikes too far apart (increasing cost)
                    - Setting strikes too close together (limiting profit potential)
                    - Opening the position too close to expiration
                    - Not considering the breakeven point relative to current price
                    - Ignoring liquidity when selecting strikes
                    """,
                    "Bear Put Spread": """
                    - Setting strikes too far apart (increasing cost)
                    - Setting strikes too close together (limiting profit potential)
                    - Entering after a substantial price decline has already occurred
                    - Not considering the breakeven point relative to current price
                    - Ignoring liquidity when selecting strikes
                    """,
                    "Long Straddle": """
                    - Implementing before low-volatility events
                    - Buying straddles when implied volatility is already high
                    - Not giving enough time for the expected move to occur
                    - Underestimating the impact of time decay
                    - Not having an exit strategy for both directional outcomes
                    """,
                    "Iron Condor": """
                    - Setting wings too narrow (increasing risk)
                    - Setting wings too wide (reducing premium)
                    - Not accounting for upcoming events that may cause volatility
                    - Ignoring liquidity in the options chosen
                    - Not having adjustment strategies for when price approaches short strikes
                    """
                }
                
                st.markdown(common_mistakes.get(selected_strategy, "No specific mistakes listed for this strategy."))

            # Educational Resources Tab
            with tabs[3]:
                    
                st.title("Educational Resources")
                
                st.markdown("""
                ### Option Basics Quiz
                
                Test your understanding of options with this quick quiz:
                """)
                
                q1 = st.radio(
                    "1. Which option gives the holder the right to buy the underlying asset?",
                    ["Call Option", "Put Option", "Both", "Neither"],
                    index=None
                )
                
                if q1:
                    if q1 == "Call Option":
                        st.success("Correct! A call option gives the holder the right to buy the underlying asset at the strike price.")
                    else:
                        st.error("Incorrect. A call option gives the holder the right to buy the underlying asset at the strike price.")
                
                q2 = st.radio(
                    "2. What's the maximum loss for a buyer of a call option?",
                    ["Unlimited", "Strike Price", "Premium Paid", "Strike Price + Premium"],
                    index=None
                )
                
                if q2:
                    if q2 == "Premium Paid":
                        st.success("Correct! The maximum loss for a call option buyer is limited to the premium paid.")
                    else:
                        st.error("Incorrect. The maximum loss for a call option buyer is limited to the premium paid.")
                
                q3 = st.radio(
                    "3. What does it mean to have a 'long' position in options?",
                    ["You're expecting the price to go up", "You've bought the option", "You're holding the option for a long time", "You've sold the option"],
                    index=None
                )
                
                if q3:
                    if q3 == "You've bought the option":
                        st.success("Correct! Having a 'long' position means you've bought the option.")
                    else:
                        st.error("Incorrect. Having a 'long' position means you've bought the option.")
                
                q4 = st.radio(
                    "4. Which option style can only be exercised at expiration?",
                    ["American Option", "European Option", "Asian Option", "Bermuda Option"],
                    index=None
                )
                
                if q4:
                    if q4 == "European Option":
                        st.success("Correct! European options can only be exercised at expiration.")
                    else:
                        st.error("Incorrect. European options can only be exercised at expiration.")
                
                q5 = st.radio(
                    "5. What Greek measures an option's sensitivity to time decay?",
                    ["Delta", "Gamma", "Theta", "Vega"],
                    index=None
                )
                
                if q5:
                    if q5 == "Theta":
                        st.success("Correct! Theta measures the rate at which an option loses value as time passes.")
                    else:
                        st.error("Incorrect. Theta measures the rate at which an option loses value as time passes.")
                
                # Additional resources
                st.markdown("""
                ### Additional Resources
                
                #### Option Strategies for Different Market Conditions
                
                | Strategy | Market Outlook | Risk | Potential Reward |
                | --- | --- | --- | --- |
                | Long Call | Bullish | Limited (Premium) | Unlimited |
                | Long Put | Bearish | Limited (Premium) | Limited but substantial |
                | Short Call | Neutral to Bearish | Unlimited | Limited (Premium) |
                | Short Put | Neutral to Bullish | Limited but substantial | Limited (Premium) |
                | Covered Call | Slightly Bullish | Substantial | Limited |
                | Protective Put | Bullish with downside protection | Limited | Unlimited minus premium |
                | Bull Call Spread | Moderately Bullish | Limited (Net Premium) | Limited (Spread - Premium) |
                | Bear Put Spread | Moderately Bearish | Limited (Net Premium) | Limited (Spread - Premium) |
                | Long Straddle | Volatile (Either Direction) | Limited (Total Premium) | Unlimited upside, Limited downside |
                | Iron Condor | Neutral (Range-Bound) | Limited (Width of spread - Premium) | Limited (Premium) |
                
                #### Comparing Basic Option Strategies
                
                **Directional Strategies:**
                - **Bullish:** Long Call > Bull Call Spread > Bull Put Spread > Short Put
                - **Bearish:** Long Put > Bear Put Spread > Bear Call Spread > Short Call
                
                **Volatility Strategies:**
                - **Expect High Volatility:** Long Straddle > Long Strangle > Long Guts
                - **Expect Low Volatility:** Iron Condor > Short Straddle > Short Strangle > Butterfly
                
                **Risk Management Strategies:**
                - **Protect Long Stock:** Protective Put > Collar > Married Put
                - **Enhance Returns:** Covered Call > Cash-Secured Put > Covered Strangle
                
                #### Black-Scholes Formula Explanation
                
                The Black-Scholes formula is used to calculate the theoretical price of European-style options. The key inputs are:
                
                - **S**: Current stock price
                - **K**: Strike price
                - **T**: Time to expiration (in years)
                - **r**: Risk-free interest rate (annual)
                - **σ**: Volatility of the underlying asset
                
                The formula calculates:
                
                For a call option: C = S⋅N(d₁) - K⋅e^(-rT)⋅N(d₂)
                For a put option: P = K⋅e^(-rT)⋅N(-d₂) - S⋅N(-d₁)
                
                Where d₁ and d₂ are calculated based on the inputs, and N() is the cumulative distribution function of the standard normal distribution.
                """)

# Footer
st.divider()
st.caption("© 2025 Derivatives Teaching Tool | Prof. José Américo – Coppead")
st.caption("Note: This tool is for educational purposes only. Real-world trading involves additional complexities.")
