"""
Módulo 6: Derivativos Embutidos
Visualização e explicação de derivativos embutidos em produtos estruturados.
"""

import streamlit as st
import streamlit.components.v1 as components


# Dictionary with alternatives, descriptions, and file paths
DERIVATIVES_INFO = {
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
    "Efeito das Margens no Mercado Futuro": {
        "file": "efeito_margens_futuro.html",
        "description": """
        **Efeito das Margens no Mercado Futuro** demonstra como ajustes nas exigências de margem 
        pela bolsa de derivativos (CME) podem desencadear quedas abruptas no preço à vista de um ativo.
        \n**Caso Real: O Crash da Prata de Janeiro/Fevereiro de 2026**
        \nEm janeiro de 2026, a prata atingiu um pico recorde de **US$ 121,67/oz**, impulsionada por 
        especulação intensa, compras de investidores chineses e expectativas de política monetária 
        frouxa nos EUA. O rali acumulou ganhos de mais de 60% em poucas semanas.
        \n**O Gatilho:** Em 30 de janeiro, a CME (Chicago Mercantile Exchange) anunciou aumento nas 
        margens iniciais para contratos de metais preciosos: **prata de 11% para 15%** e **ouro de 6% para 8%**.
        \n**O Efeito Cascata:**
        \n1. **Chamadas de margem em massa** — especuladores alavancados não conseguiram depositar 
        as garantias adicionais exigidas.
        \n2. **Liquidações forçadas** — posições foram fechadas compulsoriamente, gerando vendas 
        maciças nos futuros.
        \n3. **Contágio para o preço spot** — por arbitragem, a queda nos futuros arrastou o preço 
        à vista do metal.
        \n4. **Espiral descendente** — novas quedas geraram mais margin calls, mais liquidações e 
        mais quedas, num ciclo vicioso de desalavancagem.
        \n**Resultado:** A prata despencou **31,4% em um único dia** (30/jan) — a segunda pior queda 
        diária da história do metal — e acumulou perda de **~40% em 4 dias**, caindo para US$ 71,33/oz.
        \n**Lição Pedagógica:** As regras do mercado de derivativos (como exigências de margem) podem 
        ser mais poderosas que a oferta e demanda do ativo subjacente. O episódio evoca paralelos com 
        o crash da prata de 1980 (caso dos irmãos Hunt), quando a COMEX também elevou margens 
        dramaticamente para conter especulação.
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


def render():
    """
    Função principal que renderiza o módulo de Derivativos Embutidos.
    Esta função deve ser chamada pelo hub principal.
    """
    st.subheader("📊 Derivativos Embutidos em Produtos Estruturados")
    
    # Selection box
    selected_derivative = st.selectbox(
        "Selecione o tipo de derivativo embutido:",
        options=list(DERIVATIVES_INFO.keys()),
        key="embutidos_derivative_selector"
    )
    
    # Show description in expander
    with st.expander("ℹ️ Explicação sobre " + selected_derivative, expanded=True):
        st.markdown(DERIVATIVES_INFO[selected_derivative]["description"])
    
    # Determine appropriate height for the animation
    # The margin effect animation is taller due to its multi-section layout
    animation_height = 1200 if selected_derivative == "Efeito das Margens no Mercado Futuro" else 1100
    
    # Button to run animation
    if st.button("🎬 Executar Animação", key="embutidos_run_animation"):
        html_file = DERIVATIVES_INFO[selected_derivative]["file"]
        
        try:
            # Read and display HTML file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            components.html(html_content, height=animation_height, scrolling=True)
            
        except FileNotFoundError:
            st.error(f"❌ Arquivo '{html_file}' não encontrado. Verifique se o arquivo está no diretório correto.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar animação: {str(e)}")


# Permitir execução standalone para testes
if __name__ == "__main__":
    render()