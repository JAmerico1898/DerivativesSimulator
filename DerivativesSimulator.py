import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
        # Lista de questões não-embaralhadas
        questoes_base = [
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
        ]
        # Agora vamos adicionar mais questões para chegar a 50
        questoes_adicionais = [
            {
                "pergunta": "Qual é a principal função do mercado de derivativos na economia?",
                "opcoes": [
                    "Substituir completamente o mercado de ações",
                    "Transferir riscos entre diferentes participantes do mercado",
                    "Garantir lucros para todos os investidores",
                    "Aumentar a volatilidade dos mercados financeiros"
                ],
                "resposta": 1,
                "explicacao": "A principal função do mercado de derivativos é transferir riscos entre diferentes participantes, permitindo que aqueles que desejam se proteger contra certos riscos possam transferi-los para aqueles dispostos a assumi-los em troca de potenciais retornos."
            },
            {
                "pergunta": "O que significa 'vender a descoberto' no mercado de derivativos?",
                "opcoes": [
                    "Vender um derivativo a qualquer preço disponível no mercado",
                    "Vender um derivativo sem possuir o ativo subjacente",
                    "Vender um derivativo em um mercado não regulamentado",
                    "Vender um derivativo com garantia de recompra"
                ],
                "resposta": 1,
                "explicacao": "Vender a descoberto significa vender um contrato derivativo sem possuir o ativo subjacente, assumindo uma posição especulativa baseada na expectativa de queda no preço do ativo."
            },
            {
                "pergunta": "Qual é a diferença entre derivativos lineares e não-lineares?",
                "opcoes": [
                    "Derivativos lineares têm prazo definido, enquanto não-lineares não têm",
                    "Derivativos lineares são apenas futuros e a termo, enquanto não-lineares incluem swaps",
                    "Derivativos lineares têm payoff proporcional ao preço do ativo subjacente, enquanto não-lineares têm payoff assimétrico",
                    "Derivativos lineares são negociados em bolsa, enquanto não-lineares são OTC"
                ],
                "resposta": 2,
                "explicacao": "Derivativos lineares (como futuros e a termo) têm payoff que varia proporcionalmente com o preço do ativo subjacente, enquanto derivativos não-lineares têm payoff assimétrico que não varia proporcionalmente com o preço do ativo subjacente."
            },
            {
                "pergunta": "Qual a relação entre liquidez e spread bid-ask nos derivativos?",
                "opcoes": [
                    "Maior liquidez geralmente resulta em spreads bid-ask mais amplos",
                    "Não há relação entre liquidez e spread bid-ask",
                    "Maior liquidez geralmente resulta em spreads bid-ask mais estreitos",
                    "Spreads bid-ask são fixos em derivativos, independentemente da liquidez"
                ],
                "resposta": 2,
                "explicacao": "Maior liquidez geralmente resulta em spreads bid-ask mais estreitos, pois há mais participantes dispostos a comprar e vender, aumentando a competição e reduzindo os custos de transação."
            },
            {
                "pergunta": "O que é a 'data de vencimento' em um contrato futuro?",
                "opcoes": [
                    "A data em que o contrato foi originalmente negociado",
                    "A última data em que o contrato pode ser negociado ou liquidado",
                    "A data em que a margem inicial deve ser depositada",
                    "A data em que a bolsa cancela automaticamente contratos não liquidados"
                ],
                "resposta": 1,
                "explicacao": "A data de vencimento é a última data em que um contrato futuro pode ser negociado ou liquidado, seja por entrega física do ativo subjacente ou por liquidação financeira."
            },
            {
                "pergunta": "Qual é o significado do termo 'contango' no mercado de futuros?",
                "opcoes": [
                    "Quando o preço futuro está acima do preço à vista esperado no futuro",
                    "Quando o preço futuro está abaixo do preço à vista esperado no futuro",
                    "Quando o preço futuro e o preço à vista são exatamente iguais",
                    "Quando o mercado futuro está temporariamente fechado para negociação"
                ],
                "resposta": 0,
                "explicacao": "Contango é uma situação em que o preço futuro está acima do preço à vista esperado no futuro, refletindo custos de carregamento como armazenamento, seguro e custo de capital."
            },
            {
                "pergunta": "O que é 'backwardation' no mercado de futuros?",
                "opcoes": [
                    "Quando os contratos futuros são negociados apenas na direção de queda",
                    "Quando o preço futuro está abaixo do preço à vista esperado no futuro",
                    "Quando o preço futuro e o preço à vista são exatamente iguais",
                    "Quando há mais vendedores do que compradores no mercado futuro"
                ],
                "resposta": 1,
                "explicacao": "Backwardation é uma situação em que o preço futuro está abaixo do preço à vista esperado no futuro, geralmente refletindo escassez atual ou expectativa de oferta futura maior do ativo subjacente."
            },
            {
                "pergunta": "Quais fatores afetam o preço dos contratos futuros?",
                "opcoes": [
                    "Apenas o preço atual do ativo subjacente",
                    "Preço do ativo subjacente, taxa de juros, tempo até o vencimento e custos de carregamento",
                    "Apenas a oferta e demanda no mercado futuro",
                    "Exclusivamente as decisões dos especuladores"
                ],
                "resposta": 1,
                "explicacao": "Os preços dos contratos futuros são afetados por vários fatores, incluindo o preço à vista do ativo subjacente, taxas de juros, tempo até o vencimento, custos de carregamento (armazenamento, seguro) e expectativas de mercado."
            },
            {
                "pergunta": "Quais são os riscos associados aos derivativos?",
                "opcoes": [
                    "Apenas risco de preço do ativo subjacente",
                    "Risco de mercado, risco de contraparte, risco de liquidez e risco operacional",
                    "Apenas risco de taxa de juros",
                    "Não há riscos significativos em derivativos quando usados para hedge"
                ],
                "resposta": 1,
                "explicacao": "Os derivativos envolvem múltiplos riscos, incluindo risco de mercado (mudanças no valor do ativo subjacente), risco de contraparte (inadimplência da outra parte), risco de liquidez (dificuldade de sair da posição) e risco operacional (falhas nos processos)."
            },
            {
                "pergunta": "Por que empresas utilizam derivativos de commodities?",
                "opcoes": [
                    "Apenas para especular com preços de matérias-primas",
                    "Para garantir preços estáveis de insumos ou produtos e reduzir a incerteza orçamentária",
                    "Para aumentar artificialmente o preço de suas ações",
                    "Para evitar pagamento de impostos sobre commodities"
                ],
                "resposta": 1,
                "explicacao": "Empresas utilizam derivativos de commodities principalmente para garantir preços estáveis de matérias-primas (se forem consumidoras) ou de seus produtos (se forem produtoras), reduzindo a incerteza orçamentária e facilitando o planejamento financeiro."
            },
            {
                "pergunta": "Qual é o papel dos especuladores no mercado de derivativos?",
                "opcoes": [
                    "Apenas desestabilizar os preços de mercado",
                    "Fornecer liquidez e absorver riscos que os hedgers desejam transferir",
                    "Garantir que os preços dos derivativos sejam sempre iguais aos preços à vista",
                    "Eliminar completamente a necessidade de hedgers no mercado"
                ],
                "resposta": 1,
                "explicacao": "Os especuladores desempenham um papel importante ao fornecer liquidez ao mercado e estar dispostos a assumir riscos que os hedgers desejam transferir, facilitando a descoberta de preços e melhorando a eficiência de mercado."
            },
            {
                "pergunta": "O que é a 'convergência de preços' em contratos futuros?",
                "opcoes": [
                    "Quando os preços de todos os contratos futuros se tornam iguais",
                    "Quando o preço futuro e o preço à vista se aproximam à medida que o contrato se aproxima do vencimento",
                    "Quando todos os participantes do mercado concordam com um preço único",
                    "Quando o regulador impõe um preço fixo para equilibrar o mercado"
                ],
                "resposta": 1,
                "explicacao": "Convergência de preços refere-se ao fenômeno onde o preço do contrato futuro e o preço à vista do ativo subjacente convergem à medida que o contrato se aproxima da data de vencimento, devido à possibilidade de arbitragem."
            },
            {
                "pergunta": "Como os bancos centrais podem usar derivativos?",
                "opcoes": [
                    "Para manipular taxas de câmbio de forma ilegal",
                    "Como ferramentas de intervenção no mercado cambial e gerenciamento de reservas",
                    "Para financiar déficits governamentais",
                    "Bancos centrais nunca utilizam derivativos"
                ],
                "resposta": 1,
                "explicacao": "Bancos centrais podem usar derivativos como ferramentas de política monetária, para intervenções no mercado cambial, gerenciamento de reservas internacionais e para obter informações de mercado através dos preços dos derivativos."
            },
            {
                "pergunta": "Qual é o significado do termo 'exposição nocional' em derivativos?",
                "opcoes": [
                    "O valor máximo que pode ser perdido em um derivativo",
                    "O valor hipotético do ativo subjacente usado para calcular pagamentos",
                    "O valor do prêmio pago pelo derivativo",
                    "O valor da margem inicial depositada"
                ],
                "resposta": 1,
                "explicacao": "Exposição nocional refere-se ao valor hipotético do ativo subjacente usado como referência para calcular os pagamentos em um contrato de derivativo, não representando necessariamente o risco real ou o valor efetivamente trocado."
            },
            {
                "pergunta": "O que é o 'custo de carregamento' em contratos futuros?",
                "opcoes": [
                    "O custo de transporte físico de produtos entre diferentes mercados",
                    "Os custos associados à manutenção da posição no ativo subjacente, como armazenamento e juros",
                    "O custo das chamadas de margem durante a vida do contrato",
                    "O custo das tarifas de negociação impostas pela bolsa"
                ],
                "resposta": 1,
                "explicacao": "Custo de carregamento refere-se aos custos associados à posse do ativo subjacente durante o período do contrato, incluindo armazenamento, seguro, custos de financiamento e custos de oportunidade."
            },
            {
                "pergunta": "Como o risco de crédito é gerenciado em derivativos negociados em bolsa?",
                "opcoes": [
                    "Não há gerenciamento de risco de crédito em derivativos",
                    "Através de análises de crédito detalhadas de cada contraparte",
                    "Através da câmara de compensação, margem inicial e chamadas de margem",
                    "Exclusivamente através de garantias governamentais"
                ],
                "resposta": 2,
                "explicacao": "Em derivativos negociados em bolsa, o risco de crédito é gerenciado principalmente através da câmara de compensação que atua como contraparte central, exigindo depósitos de margem inicial e realizando chamadas de margem diárias baseadas nas movimentações de preços."
            },
            {
                "pergunta": "Qual dessas NÃO é uma estratégia válida de hedge com futuros?",
                "opcoes": [
                    "Hedge de compra (long hedge)",
                    "Hedge de venda (short hedge)",
                    "Hedge de correlação",
                    "Hedge de eliminação total de risco"
                ],
                "resposta": 3,
                "explicacao": "O 'hedge de eliminação total de risco' não é uma estratégia válida, pois hedges com derivativos geralmente não eliminam todos os riscos, especialmente o risco de base. As estratégias legítimas incluem hedge de compra, hedge de venda e hedge de correlação (cross hedging)."
            },
            {
                "pergunta": "O que é um 'rollover' de contrato futuro?",
                "opcoes": [
                    "Encerrar uma posição em um contrato prestes a vencer e abrir uma posição similar em um contrato com vencimento posterior",
                    "Solicitar a entrega física do ativo subjacente",
                    "Cancelar um contrato futuro antes do vencimento sem penalidades",
                    "Transferir um contrato futuro para outra bolsa de valores"
                ],
                "resposta": 0,
                "explicacao": "Rollover refere-se à prática de encerrar uma posição em um contrato futuro prestes a vencer e simultaneamente abrir uma posição similar em um contrato com vencimento posterior, permitindo manter a exposição ao mercado sem lidar com o vencimento do contrato original."
            },
            {
                "pergunta": "O que significa 'netting' em transações de derivativos?",
                "opcoes": [
                    "O processo de combinar múltiplas posições ou obrigações para reduzir o risco e as transferências de valor",
                    "A prática de adicionar novas posições para aumentar a exposição",
                    "O cálculo de lucros líquidos de todas as transações de derivativos",
                    "A inclusão de taxas adicionais em contratos de derivativos"
                ],
                "resposta": 0,
                "explicacao": "Netting refere-se ao processo de combinar múltiplas posições ou obrigações entre contrapartes para chegar a um valor líquido a ser transferido, reduzindo o risco de contraparte e o número/volume de liquidações necessárias."
            },
            {
                "pergunta": "O que é um contrato futuro 'cash settled'?",
                "opcoes": [
                    "Um contrato que só pode ser comprado com dinheiro à vista",
                    "Um contrato onde a liquidação ocorre financeiramente sem entrega física do ativo subjacente",
                    "Um contrato que exige pagamento antecipado completo",
                    "Um contrato onde apenas instituições financeiras podem participar"
                ],
                "resposta": 1,
                "explicacao": "Um contrato futuro 'cash settled' (liquidação financeira) é aquele em que, no vencimento, não há entrega física do ativo subjacente, mas sim a liquidação financeira baseada na diferença entre o preço contratado e o preço de referência final do ativo."
            },
            {
                "pergunta": "Qual é a diferença entre hedge estático e hedge dinâmico?",
                "opcoes": [
                    "Hedge estático é feito apenas uma vez, enquanto hedge dinâmico envolve ajustes frequentes da posição",
                    "Hedge estático usa apenas um tipo de derivativo, enquanto hedge dinâmico usa múltiplos tipos",
                    "Hedge estático é apenas para commodities, enquanto hedge dinâmico é para instrumentos financeiros",
                    "Hedge estático é ilegal na maioria dos países, enquanto hedge dinâmico é permitido"
                ],
                "resposta": 0,
                "explicacao": "Hedge estático envolve estabelecer uma posição de hedge e mantê-la inalterada até o vencimento, enquanto hedge dinâmico envolve ajustes frequentes da posição de hedge em resposta às mudanças no mercado e nas condições do ativo sendo protegido."
            },
        ]
        
        # Combinar as listas de questões
        todas_questoes = questoes_base + questoes_adicionais
        
        # Embaralhar as alternativas de cada questão para distribuir as respostas corretas
        for questao in todas_questoes:
            # Guarda a resposta correta
            resposta_correta = questao["opcoes"][questao["resposta"]]
            
            # Embaralha as opções
            opcoes_embaralhadas = questao["opcoes"].copy()
            random.shuffle(opcoes_embaralhadas)
            
            # Atualiza a questão com as opções embaralhadas
            questao["opcoes"] = opcoes_embaralhadas
            
            # Encontra o novo índice da resposta correta
            questao["resposta"] = opcoes_embaralhadas.index(resposta_correta)
        
        return todas_questoes

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
        st.button("Termos", type='primary', use_container_width=True, on_click=select_option, args=("Termos",))
            
    with col3:
        st.button("Futuros", type='primary', use_container_width=True, on_click=select_option, args=("Futuros",))

    col4, col5, col6 = st.columns([4, 1, 4])
    with col4:
        st.button("Swaps", type='primary', use_container_width=True, on_click=select_option, args=("Swaps",))

    with col6:
        st.button("Options", type='primary', use_container_width=True, on_click=select_option, args=("Options",))
        
    col7, col8, col9 = st.columns([2, 3, 2])
    with col8:
        st.button("Derivativos Embutidos", type='primary', use_container_width=True, on_click=select_option, args=("Derivativos Embutidos",))

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
        if st.session_state.selected_option == "Termos":

            # CSS customizado para melhorar o visual
            st.markdown("""
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
            """, unsafe_allow_html=True)

            # Funções auxiliares
            def formatar_moeda_brl(valor):
                """Formata valor como moeda brasileira"""
                return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            def formatar_moeda_usd(valor):
                """Formata valor como dólares americanos"""
                return f"US$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

            def formatar_cotacao(valor):
                """Formata cotação com 2 casas decimais"""
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
                """Calcula valor inicial em reais para referência"""
                return cotacao_contratacao * valor_nocional_usd

            def calcular_valor_final_brl(cotacao_vencimento, valor_nocional_usd):
                """Calcula valor final em reais para referência"""
                return cotacao_vencimento * valor_nocional_usd

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
                    help="Compra: Você lucra se o dólar subir. Venda: Você lucra se o dólar descer."
                )
                
                valor_nocional_milhoes = st.number_input(
                    "Valor Nocional (US$ milhões):",
                    min_value=1.0,
                    max_value=100.0,
                    value=10.0,
                    step=1.0,
                    format="%.0f",
                    help="Valor da operação em milhões de dólares americanos"
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
                    help="Taxa de câmbio BRL/USD acordada no momento da contratação"
                )
                
                cotacao_vencimento = st.number_input(
                    "Cotação do NDF no Vencimento (BRL/USD):",
                    min_value=1.0000,
                    max_value=10.0000,
                    value=5.5000,
                    step=0.0100,
                    format="%.2f",
                    help="Taxa de câmbio BRL/USD na data de vencimento (1 ano depois)"
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

            # Criar gráfico mostrando a evolução da cotação
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

            ##########################################################################################################
            ##########################################################################################################
            
        # Instructions based on selection
        if st.session_state.selected_option == "Futuros":
            
            # CSS customizado para melhorar o visual
            st.markdown("""
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
            """, unsafe_allow_html=True)

            # Funções auxiliares
            def formatar_moeda(valor):
                """Formata valor como moeda brasileira"""
                return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            def formatar_numero(valor):
                """Formata número com separador de milhares"""
                return f"{valor:,.0f}".replace(",", ".")

            def calcular_pu_contratacao(taxa_contratacao, prazo_vencimento):
                """Calcula o PU na contratação"""
                return 100000 / ((1 + taxa_contratacao) ** (prazo_vencimento / 252))

            def calcular_numero_contratos(valor_nocional, pu_contratacao):
                """Calcula número de contratos (arredondado para baixo)"""
                return math.floor(valor_nocional / pu_contratacao)

            def calcular_pu_vencimento(pu_contratacao, taxa_efetiva):
                """Calcula PU no vencimento"""
                return pu_contratacao * (1 + taxa_efetiva)

            def calcular_resultado(operacao, pu_contratacao, pu_vencimento, numero_contratos):
                """Calcula resultado da operação"""
                if operacao == "Compra":
                    return (pu_vencimento - 100000) * numero_contratos
                else:
                    return (100000 - pu_vencimento) * numero_contratos

            def calcular_taxa_efetiva_anual(taxa_efetiva):
                """Taxa Efetiva Anual no Período"""
                return ((1 + taxa_efetiva/100)**(252/prazo_vencimento)-1)*100

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
                #st.subheader("🎯 Parâmetros da Operação")
                
                operacao = st.selectbox(
                    "Tipo de Operação:",
                    ["Compra", "Venda"],
                    help="Escolha se você está comprando ou vendendo contratos DI futuro"
                )
                
                valor_nocional_milhoes = st.number_input(
                    "Valor Nocional (R$ milhões):",
                    min_value=10.0,
                    max_value=100.0,
                    value=50.0,
                    step=1.0,
                    help="Valor total da operação em milhões de reais"
                )

                prazo_vencimento = st.number_input(
                    "Prazo para Vencimento (dias úteis):",
                    min_value=1,
                    max_value=252,
                    value=10,
                    step=1,
                    help="Número de dias úteis até o vencimento (ano = 252 dias úteis)"
                )

            with col2:
                #st.subheader("📊 Taxas de Juros")
                
                taxa_contratacao = st.number_input(
                    "Taxa de Juros na Contratação (% a.a.):",
                    min_value=0.0,
                    max_value=50.0,
                    value=12.0,
                    step=0.01,
                    format="%.2f",
                    help="Taxa de juros anual no momento da contratação"
                )
                
                taxa_efetiva = st.number_input(
                    "Taxa Efetiva no Período (%):",
                    min_value=-10.0,
                    max_value=10.0,
                    value=0.50,
                    step=0.01,
                    format="%.2f",
                    help="Taxa efetiva realizada no período"
                )

                taxa_efetiva_anual_periodo = calcular_taxa_efetiva_anual(taxa_efetiva)
                taxa_efetiva_anual = st.number_input(
                    "Taxa Efetiva Anual no Período (%):",
                    value=taxa_efetiva_anual_periodo,
                    format="%.2f",
                    help="Taxa efetiva anual realizada no período"
                )

            #    taxa_efetiva_anual_periodo 
                


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

            # Criar gráfico com Plotly - Duas linhas distintas
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

            ##########################################################################################################
            ##########################################################################################################
            
        # Instructions based on selection
        if st.session_state.selected_option == "Derivativos Embutidos":

            st.subheader("📊 Derivativos Embutidos em Produtos Estruturados")
            
            # Dictionary with alternatives, descriptions, and file paths
            derivatives_info = {
                "Contrato a Termo Embutido": {
                    "file": "termo_embutido.html",
                    "description": """
                    **Contrato a Termo (Forward) Embutido** é um compromisso de comprar/vender algo em data futura 
                    a preço fixado, dentro de outro contrato. Comum em contratos de fornecimento com cláusulas de ajuste de preço 
                    e operações de hedge cambial embutidas em contratos comerciais. O comprador se protege contra 
                    alta de preços, enquanto o vendedor garante o preço de venda futuro.
                    \n**Exemplo na Animação:**
                    \n**O Cenário:** 
                    Uma empresa brasileira de energia aluga turbinas de uma empresa americana.
                    \n**Contrato Anfitrião:** Contrato de Aluguel (Leasing).
                    \n**O Derivativo (Termo):** O contrato diz que o aluguel mensal é de R$ 500.000,00, mas 
                    esse valor será reajustado trimestralmente pela variação do Dólar.
                    \n**Por que é embutido?** 
                    Não é um contrato de câmbio puro. É um aluguel. Mas, na prática, a empresa brasileira 
                    "vendeu um termo de dólar" (ficou vendida em real, comprada em dólar) dentro do aluguel. Se o dólar subir, 
                    o aluguel fica mais caro, replicando a mecânica de um contrato a termo de moeda.
                    """
                },
                "Futuro Embutido": {
                    "file": "futuro_embutido.html",
                    "description": """
                    **Contrato Futuro Embutido** é similar ao termo, mas com ajustes diários (marcação a mercado). 
                    Frequentemente encontrado em estruturas de financiamento atreladas a commodities e em alguns 
                    produtos de investimento que replicam índices futuros. A diferença crucial está na liquidação 
                    diária das diferenças de preço, gerando fluxos de caixa intermediários.
                    \n**Exemplo na Animação:**
                    \n**O Cenário:**
                    Um Certificado de Depósito Bancário (CDB) ou Nota Promissória indexada a Commodities.
                    \n**Contrato Anfitrião:** Título de Dívida (Renda Fixa).
                    \n**O Derivativo (Futuro):** O banco emite um CDB que não paga CDI, mas sim a variação do Contrato Futuro de Ouro na B3.
                    \n**Mecânica:** Se o ouro subir 10%, seu CDB rende 10%. Se cair 10%, seu principal diminui 10% (assumindo que não há capital protegido).
                    \n**Análise:** O investidor comprou, efetivamente, um contrato futuro de ouro, mas "embalado" como um CDB para facilitar o acesso ou tributação.
                    """
                },
                "Swap Embutido": {
                    "file": "swap_embutido.html",
                    "description": """
                    **Swap Embutido** envolve a troca de fluxos financeiros, como câmbio por taxa fixa ou 
                    taxa pré por pós-fixada. Muito comum em debêntures que permitem troca de indexador 
                    (ex: CDI por IPCA) e em operações de financiamento com swap cambial implícito. 
                    Permite que emissores e investidores ajustem seus perfis de risco sem alterar o título base.
                    \n**Exemplo na Animação:**
                    \n**O Cenário:**
                    Emissão de dívida internacional com proteção cambial interna.
                    \n**Contrato Anfitrião:** Título de Dívida em Moeda Estrangeira.
                    \n**O Derivativo (Swap):** Imagine que uma empresa emite um título que paga "Libor + 2%", 
                    mas insere uma cláusula de Cap (teto) na taxa de juros, onde se a Libor passar de 5%, a 
                    taxa se converte automaticamente para uma taxa fixa de 7%.
                    \n**Mecânica:** Isso é um **Swap de Taxa de Juros** embutido. Em determinado momento, o 
                    fluxo de caixa "troca" de flutuante para fixo automaticamente, alterando a natureza do risco do investidor.
                    """
                },
                "Opção de Compra (Call) - Callable Bond": {
                    "file": "opção_callable_bond.html",
                    "description": """
                    **Callable Bond (Opção de Compra/Call do Emissor)** é um título de dívida que dá ao emissor o direito de resgatá-lo antecipadamente 
                    a um preço predeterminado. O emissor possui uma opção de compra embutida, que 
                    é valiosa quando as taxas de juros caem, permitindo refinanciamento a custo menor. 
                    Investidores exigem prêmio de rendimento (yield) maior para compensar este risco de resgate.
                    \n**Exemplo na Animação:**
                    \n**O Cenário:**
                    Emissão de dívida internacional a 10%a.a. com cláusula de recompra a 9%a.a.. O preço é de 1020, o que impõe uma pequena multa rescisória.
                    \n**Contrato Anfitrião:** Título de dívida (Bond).
                    \n**O Derivativo (Opção):** o emissor tem o direito de recomprar a dívida antecipadamente 
                    se os juros de mercado caírem a 9%a.a..
                    \n**Análise:** O investidor vendeu uma Opção de Compra para o emissor. Por isso, esse 
                    título costuma pagar juros maiores (o prêmio da opção).
                    """
                },
                "Opção de Conversão - Debênture Conversível": {
                    "file": "opção_debênture_conversível.html",
                    "description": """
                    **Debênture Conversível** concede ao investidor o direito de converter o título de dívida 
                    em ações da empresa emissora a uma razão predeterminada. Combina características de renda 
                    fixa (cupons) com potencial de valorização acionária. O investidor possui uma opção de compra 
                    \n**Exemplo na Animação:**
                    \n**O Cenário:**
                    Emissão de dívida com cláusula de conversão em ações ao preço fixo de R$20,00.
                    \n**Contrato Anfitrião:** Dívida corporativa (Debênture).
                    \n**O Derivativo (Opção):** O investidor tem o direito de, no vencimento, trocar o valor da 
                    dívida por ações da empresa a um preço pré-fixado.
                    \n**Análise:** O investidor comprou uma dívida + uma Opção de Compra (Call) da ação.
                    """
                },
                "COE com Proteção de Capital": {
                    "file": "opção_COE_capital_protegido.html",
                    "description": """
                    **COE (Certificado de Operações Estruturadas) com Proteção de Capital** garante ao investidor 
                    a devolução de pelo menos 100% do capital investido no vencimento, mais potencial de ganho 
                    atrelado a um ativo de referência. Estruturado como zero-coupon bond + opção de compra. 
                    Popular no varejo brasileiro, transfere risco do emissor bancário para o investidor através 
                    de estruturas complexas de opções.
                    \n**Exemplo na Animação:**
                    \n**O Cenário:**
                    Aplicação em instrumento com principal garantido e potencial upside.
                    \n**Contrato Anfitrião:** COE.
                    \n**O Derivativo (Opção):**
                    \n**Análise:** O banco usa 95% do seu dinheiro para garantir o principal em Renda Fixa e usa 
                    5% para comprar Opções de Compra (Call) da Bolsa Americana. Se subir, você ganha a valorização 
                    multiplicada. Se cair, a opção vira pó, mas você tem o principal de volta.
                    """
                },
                "Credit-Linked Note (CLN)": {
                    "file": "credit_linked_note.html",
                    "description": """
                    **Credit-Linked Note** é um título de dívida cujo retorno depende do risco de crédito de 
                    uma entidade de referência. Se ocorrer evento de crédito (default, reestruturação), o 
                    investidor sofre perdas. Embute um Credit Default Swap (CDS), permitindo que bancos 
                    transfiram risco de crédito de suas carteiras para investidores que buscam yield premium.
                    \nEm resumo: O investidor está agindo como uma seguradora.
                    \nO investidor compra o instrumento.
                    \nEm troca, ele recebe juros muito altos (os juros do títulos de dívida que lastreia o 
                    instrumento, acrescido do prêmio do seguro).
                    \nSe a empresa de referência pagar suas dívidas, o investidor ganha acima do mercado.
                    \nSe a empresa der calote, o investidor paga a conta (perde o principal).
                    """
                },
                "Caso Braskem - COE Estruturado": {
                    "file": "braskem.html",
                    "description": """
                    **Caso Braskem** ilustra o colapso de COEs estruturados emitidos por bancos brasileiros 
                    atrelados a títulos de dívida da Braskem. Quando a empresa enfrentou grave crise, investidores de 
                    varejo sofreram perdas significativas, revelando como derivativos embutidos transferem 
                    risco complexo de mercado dos bancos para clientes que muitas vezes não compreendem 
                    plenamente a estrutura do produto.
                    """
                }
            }
            
            # Selection box
            selected_derivative = st.selectbox(
                "Selecione o tipo de derivativo embutido:",
                options=list(derivatives_info.keys()),
                key="derivative_selector"
            )
            
            # Show description in expander
            with st.expander("ℹ️ Explicação sobre " + selected_derivative, expanded=True):
                st.markdown(derivatives_info[selected_derivative]["description"])
            
            # Button to run animation
            if st.button("🎬 Executar Animação", key="run_derivative_animation"):
                html_file = derivatives_info[selected_derivative]["file"]
                
                try:
                    # Read and display HTML file
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    st.components.v1.html(html_content, height=1100, scrolling=True)
                    
                except FileNotFoundError:
                    st.error(f"❌ Arquivo '{html_file}' não encontrado. Verifique se o arquivo está no diretório correto.")
                except Exception as e:
                    st.error(f"❌ Erro ao carregar animação: {str(e)}")


# Footer
st.divider()
st.caption("© 2025 Derivatives Teaching Tool | Prof. José Américo – Coppead")
st.caption("Note: This tool is for educational purposes only. Real-world trading involves additional complexities.")
