"""
Módulo 1: Introdução aos Derivativos
Quiz interativo sobre conceitos básicos de derivativos financeiros.
"""

import streamlit as st
import random


def gerar_banco_questoes():
    """Gera o banco de questões com alternativas embaralhadas."""
    
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


# Mensagens de feedback
FEEDBACK_CORRETO = [
    "🎉 Acertou! Você está mandando bem nos derivativos!",
    "✅ Correto! Está no caminho certo para se tornar um especialista!",
    "🔥 Resposta correta! Isso aí, continue assim!",
    "👍 Exato! Seu professor ficaria orgulhoso!",
    "🌟 Perfeito! Você entendeu o conceito muito bem!"
]

FEEDBACK_INCORRETO = [
    "❌ Ops! Não foi dessa vez. Mas não desanime!",
    "😅 Resposta incorreta, mas errar faz parte do aprendizado!",
    "🤔 Hmm, não está certo. Vamos revisar esse conceito?",
    "📚 Incorreto! Sugestão: reveja esta parte do material!",
    "🧐 Não é essa a resposta. Mas você está aprendendo!"
]


def selecionar_questoes_aleatorias(banco_questoes, quantidade=10):
    """Seleciona questões aleatórias do banco, filtrando menções a opções."""
    # Filtrar questões para remover qualquer menção a opções
    banco_filtrado = [q for q in banco_questoes if "opção" not in q["pergunta"].lower() and 
                    "call" not in q["pergunta"].lower() and 
                    "put" not in q["pergunta"].lower()]
    
    if quantidade > len(banco_filtrado):
        quantidade = len(banco_filtrado)
    return random.sample(banco_filtrado, quantidade)


def exibir_questao(questao, indice):
    """Exibe uma questão individual com opções de resposta."""
    st.subheader(f"Questão {indice + 1}")
    st.write(questao["pergunta"])
    opcao_selecionada = st.radio("Escolha uma opção:", questao["opcoes"], key=f"intro_q{indice}")
    indice_opcao = questao["opcoes"].index(opcao_selecionada)
    
    if st.button("Responder", key=f"intro_responder{indice}"):
        if indice_opcao == questao["resposta"]:
            st.success(random.choice(FEEDBACK_CORRETO))
            st.session_state[f"intro_pontos_q{indice}"] = 1
        else:
            st.error(random.choice(FEEDBACK_INCORRETO))
            st.session_state[f"intro_pontos_q{indice}"] = 0
        
        st.info(f"**Explicação:** {questao['explicacao']}")
        
        # Mostre a resposta correta se o usuário errou
        if indice_opcao != questao["resposta"]:
            st.write(f"**Resposta correta:** {questao['opcoes'][questao['resposta']]}")
    
    # Adicionar espaçador entre questões
    st.markdown("---")


def render():
    """
    Função principal que renderiza o módulo de Introdução.
    Esta função deve ser chamada pelo hub principal.
    """
    st.title("Quiz de Derivativos")
    st.markdown("""
    ### Bem-vindo ao questionário interativo sobre Introdução aos Derivativos!
    
    Este quiz contém 10 questões de múltipla escolha para testar seus conhecimentos sobre derivativos financeiros.
    Cada vez que você clicar em "Gerar Novo Questionário", um conjunto diferente de perguntas será selecionado.
    
    Boa sorte! 📊📈
    """)
    
    # Inicializar ou resetar o quiz
    if st.button("Gerar Novo Questionário") or "intro_questoes" not in st.session_state:
        banco_questoes = gerar_banco_questoes()
        st.session_state.intro_questoes = selecionar_questoes_aleatorias(banco_questoes)
        
        # Resetar pontuação
        for i in range(len(st.session_state.intro_questoes)):
            st.session_state[f"intro_pontos_q{i}"] = 0
    
    # Exibir as questões
    for i, questao in enumerate(st.session_state.intro_questoes):
        exibir_questao(questao, i)
    
    # Calcular e exibir pontuação total
    if "intro_questoes" in st.session_state:
        pontos_total = sum([st.session_state.get(f"intro_pontos_q{i}", 0) for i in range(len(st.session_state.intro_questoes))])
        
        # Só mostrar pontuação se pelo menos uma questão foi respondida
        if sum([1 for i in range(len(st.session_state.intro_questoes)) if f"intro_pontos_q{i}" in st.session_state]) > 0:
            st.sidebar.header("Seu Desempenho")
            st.sidebar.metric("Pontuação", f"{pontos_total}/{len(st.session_state.intro_questoes)}")
            
            # Mostrar mensagem baseada na pontuação
            porcentagem = (pontos_total / len(st.session_state.intro_questoes)) * 100
            if porcentagem >= 90:
                st.sidebar.success("🏆 Excelente! Você domina os derivativos!")
            elif porcentagem >= 70:
                st.sidebar.success("🎓 Muito bom! Você tem um bom conhecimento!")
            elif porcentagem >= 50:
                st.sidebar.info("📚 Bom trabalho! Continue estudando!")
            else:
                st.sidebar.warning("📝 Continue praticando. Você consegue melhorar!")


# Permitir execução standalone para testes
if __name__ == "__main__":
    render()