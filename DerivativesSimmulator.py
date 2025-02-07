import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum

st.markdown("<h5 style='text-align: center;'>Escolha sua Opção</h5>", unsafe_allow_html=True)
st.markdown('---')
options = ["Forward", "Futures", "Swaps"]

# Create three columns with the middle column wider
col1, col2, col3 = st.columns([1, 2, 1])

# Place the radio button in the middle column to center it
with col2:
    geral = st.radio("", options, index=0, disabled=False, horizontal=True, captions=None)
    
if geral == "Swaps":

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
    - Hedge Result: R$ {results['hedge_result']:,.2f}
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
                "Initial Exchange Rate (R$/US$)",
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
                "Exchange Rate at Maturity (R$/US$)",
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
                "Hedge Result",
                f"R$ {results['hedge_result']:,.2f}",
                delta=None
            )
        
        with col3:
            st.metric(
                "Total Result",
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

elif geral == "Forward":

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

    st.sidebar.header("1. Define Contract Parameters")

    # Notional and period length
    notional = st.sidebar.number_input("Notional Amount ($)", min_value=10000, step=10000, value=1_000_000)
    delta = st.sidebar.number_input(r"Time Period \(Delta\) (in years)", min_value=0.01, max_value=2.0, step=0.05, value=0.25)

    # Forward (FWD) fixed rate (annualized)
    F_rate_percent = st.sidebar.number_input("Forward (FWD) Fixed Rate [%] (annualized)", min_value=0.0, max_value=20.0, step=0.1, value=5.0)
    F = F_rate_percent / 100.0

    # Exposure type: Floating vs. Fixed
    exposure_type = st.sidebar.selectbox("Hedged Exposure Type", ("Floating Rate Exposure", "Fixed Rate Exposure"))
    if exposure_type == "Fixed Rate Exposure":
        fixed_exposure_rate_percent = st.sidebar.number_input("Fixed Exposure Rate [%] (annualized)", min_value=0.0, max_value=20.0, step=0.1, value=5.0)
        fixed_exposure_rate = fixed_exposure_rate_percent / 100.0

    st.sidebar.header("2. Vary the Market Rate")

    # Slider for the effective market (floating) rate L for the period.
    # Note: Here L is the effective rate for the entire period (e.g., a quarterly effective rate).
    L_rate_percent = st.sidebar.slider("Effective Market Rate (L) for the Period [%]", min_value=0.0, max_value=15.0, value=1.5, step=0.1)
    L = L_rate_percent / 100.0

    st.subheader("Calculated Results")
    st.markdown("#### FWD (Forward) Payoff")

    # Calculate the effective fixed rate for the period from the annualized FWD fixed rate, using compound interest.
    effective_fixed_rate = (1 + F)**delta - 1

    # Compute the FWD payoff using the new formula
    FWD_payoff = notional * (L - effective_fixed_rate)
    st.write(f"**FWD Payoff:** ${FWD_payoff:,.2f}")

    # Compute the exposure’s cost
    if exposure_type == "Floating Rate Exposure":
        # For a floating exposure, the cost is based on the effective rate L.
        exposure_cost = notional * L
        st.write(f"**Floating Exposure Cost:** ${exposure_cost:,.2f}")
    elif exposure_type == "Fixed Rate Exposure":
        # For a fixed exposure, adjust the annualized fixed rate using compound interest.
        effective_fixed_exposure_rate = (1 + fixed_exposure_rate)**delta - 1
        exposure_cost = notional * effective_fixed_exposure_rate
        st.write(f"**Fixed Exposure Cost:** ${exposure_cost:,.2f}")

    # The net combined outcome (hedged portfolio)
    net_outcome = exposure_cost - FWD_payoff
    st.markdown("#### Net Hedged Outcome")
    st.write(f"**Net Outcome:** ${net_outcome:,.2f}")

    st.markdown("---")
    st.markdown(r"""
    ### Graphical Overview

    The graph below shows how the FWD payoff, the exposure cost, and the net outcome vary as the effective market rate \(L\) for the period changes.
    A vertical dashed line indicates the currently selected market rate.
    """)

    # Prepare a range of effective market rates for plotting
    L_values = np.linspace(0.0, 0.15, 300)  # from 0% to 15% effective rate for the period
    FWD_payoffs = notional * (L_values - ((1 + F)**delta - 1))

    if exposure_type == "Floating Rate Exposure":
        exposure_costs = notional * L_values
    elif exposure_type == "Fixed Rate Exposure":
        exposure_costs = notional * ((1 + fixed_exposure_rate)**delta - 1) * np.ones_like(L_values)

    net_outcomes = exposure_costs - FWD_payoffs

    # Plot the curves
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(L_values * 100, FWD_payoffs, label="FWD Payoff", color="C1")
    ax.plot(L_values * 100, exposure_costs, label="Exposure Cost", color="C2")
    ax.plot(L_values * 100, net_outcomes, label="Net Outcome", color="C0", linestyle="--")
    ax.axvline(L_rate_percent, color="gray", linestyle="--", label=f"Current L = {L_rate_percent:.1f}%")
    ax.set_xlabel("Effective Market Rate (L) for the Period (%)")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

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
    
elif geral == "Futures":
    
    def calculate_theoretical_price(spot_price, rate, days=5):
        T = days/252
        return spot_price * np.exp(rate * T)

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
            
            with col1:
                st.metric("Theoretical Price", f"${theoretical_price:.2f}/barrel")
            with col2:
                st.metric("Futures P&L", f"${futures_pnl:.2f}")
            with col3:
                st.metric("Hedge Result", f"${net_result:.2f}")
            
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
                st.write(f"- The hedge result: ${net_result:.2f}")

    if __name__ == "__main__":
        main()

    
