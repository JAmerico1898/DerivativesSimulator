"""
Módulo 4: Swaps
Calculadora de operações de swap no mercado brasileiro.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from enum import Enum
from dataclasses import dataclass


# Enums for swap types
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
    """Calculator for swap operations."""
    
    def __init__(self, swap_params: SwapParameters, hedge_params: HedgeParameters):
        self.swap_params = swap_params
        self.hedge_params = hedge_params
    
    def _calculate_pre_fixed_adjustment(self, rate, quarters):
        return (1 + rate) ** (quarters / 4) - 1
    
    def _calculate_exposure_exchange_rate_adjustment(self, initial_rate, final_rate, rate, quarters):
        if initial_rate is None or final_rate is None:
            raise ValueError("Exchange rates must be provided for exchange rate calculations")
            
        # Calculate exchange rate variation
        exchange_variation = (final_rate / initial_rate) - 1
        
        # Calculate the rate adjustment using compound interest
        rate_adjustment = (1 + rate) ** (quarters / 4) - 1
        
        # Combine both effects using compound interest
        total_adjustment = (1 + exchange_variation) * (1 + rate_adjustment) - 1
        
        return total_adjustment
    
    def _calculate_hedge_exchange_rate_adjustment(self, initial_rate, final_rate, cupom_cambial, quarters):
        if initial_rate is None or final_rate is None:
            raise ValueError("Exchange rates must be provided for exchange rate calculations")
            
        # Calculate exchange rate variation
        exchange_variation = (final_rate / initial_rate) - 1
        
        # Calculate the cupom cambial adjustment
        cupom_adjustment = (1 + cupom_cambial) ** (quarters / 4) - 1
        
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
                self.swap_params.rate,
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
                self.hedge_params.asset_cupom_cambial,
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
                self.hedge_params.liability_cupom_cambial,
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
                rate_adj = (1 + self.swap_params.rate) ** (q / 4) - 1
                exposure_adj = (1 + exchange_variation) * (1 + rate_adj) - 1
            
            exposure_value = self.swap_params.notional * exposure_adj
            exposure_values.append(-exposure_value if self.swap_params.exposure_type == ExposureType.LIABILITY else exposure_value)
            
            # Calculate asset leg values
            if self.hedge_params.asset_indexer == IndexerType.PRE_FIXED:
                asset_adj = self._calculate_pre_fixed_adjustment(self.hedge_params.asset_rate, q)
            elif self.hedge_params.asset_indexer == IndexerType.POST_FIXED:
                asset_adj = self.hedge_params.asset_rate * (q / self.swap_params.quarters)
            else:  # Exchange Rate
                cupom_adj = (1 + self.hedge_params.asset_cupom_cambial) ** (q / 4) - 1
                asset_adj = (1 + exchange_variation) * (1 + cupom_adj) - 1
            
            asset_values.append(self.swap_params.notional * asset_adj)
            
            # Calculate liability leg values (now making it negative)
            if self.hedge_params.liability_indexer == IndexerType.PRE_FIXED:
                liability_adj = self._calculate_pre_fixed_adjustment(self.hedge_params.liability_rate, q)
            elif self.hedge_params.liability_indexer == IndexerType.POST_FIXED:
                liability_adj = self.hedge_params.liability_rate * (q / self.swap_params.quarters)
            else:  # Exchange Rate
                cupom_adj = (1 + self.hedge_params.liability_cupom_cambial) ** (q / 4) - 1
                liability_adj = (1 + exchange_variation) * (1 + cupom_adj) - 1
            
            # Make liability negative since it's a payment obligation
            liability_values.append(-self.swap_params.notional * liability_adj)
        
        # Calculate net position
        net_values = [e + a + l for e, a, l in zip(exposure_values, asset_values, liability_values)]
        
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
Period: {self.swap_params.quarters} quarters ({self.swap_params.quarters / 4:.2f} years)

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


def criar_grafico_evolucao(time_series):
    """Cria o gráfico de evolução das posições."""
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
    
    return fig


def render():
    """
    Função principal que renderiza o módulo de Swaps.
    Esta função deve ser chamada pelo hub principal.
    """
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
            key="swaps_exposure_type"
        )
        
        notional = st.number_input(
            "Notional Amount (R$)",
            min_value=0.0,
            value=1000000.0,
            step=100000.0,
            format="%f",
            key="swaps_notional"
        )
        
        exposure_indexer = st.selectbox(
            "Indexer",
            options=[idx.value for idx in IndexerType],
            key="swaps_exposure_indexer"
        )
        
        exposure_rate = st.number_input(
            "Rate (as decimal, e.g., 0.12 for 12%)",
            min_value=0.0,
            max_value=1.0,
            value=0.12,
            step=0.01,
            format="%f",
            key="swaps_exposure_rate"
        )
        
        exposure_exchange_rate = None
        if exposure_indexer == IndexerType.EXCHANGE_RATE.value:
            exposure_exchange_rate = st.number_input(
                "Initial Exchange Rate (BRL/USD)",
                min_value=0.0,
                value=5.0,
                step=0.1,
                format="%f",
                key="swaps_exposure_exchange_rate"
            )
        
        quarters = st.number_input(
            "Number of Quarters",
            min_value=1,
            max_value=40,  # 10 years
            value=4,  # Default to 1 year
            step=1,
            key="swaps_quarters"
        )

    with col2:
        st.header("Hedge Details")
        
        # Asset leg
        st.subheader("Asset Leg")
        asset_indexer = st.selectbox(
            "Asset Indexer",
            options=[idx.value for idx in IndexerType],
            key="swaps_asset_indexer"
        )
        
        asset_rate = 0.0
        if asset_indexer != IndexerType.EXCHANGE_RATE.value:
            asset_rate = st.number_input(
                "Asset Rate (as decimal)",
                min_value=0.0,
                max_value=1.0,
                value=0.115,
                step=0.01,
                format="%f",
                key="swaps_asset_rate"
            )
        
        asset_cupom = None
        if asset_indexer == IndexerType.EXCHANGE_RATE.value:
            asset_cupom = st.number_input(
                "Asset Cupom Cambial (as decimal)",
                min_value=0.0,
                max_value=1.0,
                value=0.05,
                step=0.01,
                format="%f",
                key="swaps_asset_cupom"
            )
        
        # Liability leg
        st.subheader("Liability Leg")
        liability_indexer = st.selectbox(
            "Liability Indexer",
            options=[idx.value for idx in IndexerType],
            key="swaps_liability_indexer"
        )
        
        liability_rate = 0.0
        if liability_indexer != IndexerType.EXCHANGE_RATE.value:
            liability_rate = st.number_input(
                "Liability Rate (as decimal)",
                min_value=0.0,
                max_value=1.0,
                value=0.12,
                step=0.01,
                format="%f",
                key="swaps_liability_rate"
            )
        
        liability_cupom = None
        if liability_indexer == IndexerType.EXCHANGE_RATE.value:
            liability_cupom = st.number_input(
                "Liability Cupom Cambial (as decimal)",
                min_value=0.0,
                max_value=1.0,
                value=0.05,
                step=0.01,
                format="%f",
                key="swaps_liability_cupom"
            )

        # Exchange rate at maturity (shown if any leg uses exchange rate)
        exchange_rate_maturity = None
        if (asset_indexer == IndexerType.EXCHANGE_RATE.value or 
            liability_indexer == IndexerType.EXCHANGE_RATE.value or 
            exposure_indexer == IndexerType.EXCHANGE_RATE.value):
            exchange_rate_maturity = st.number_input(
                "Exchange Rate at Maturity (BRL/USD)",
                min_value=0.0,
                value=5.2,
                step=0.1,
                format="%f",
                key="swaps_exchange_rate_maturity"
            )

    # Calculate button
    if st.button("Calculate Swap Results", key="swaps_calculate_btn"):
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
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric(
                "Exposure Result",
                f"R$ {results['exposure_result']:,.2f}",
                delta=None
            )
        
        with res_col2:
            st.metric(
                "Swap P&L",
                f"R$ {results['hedge_result']:,.2f}",
                delta=None
            )
        
        with res_col3:
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
        
        # Create and display the plot
        fig = criar_grafico_evolucao(time_series)
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


# Permitir execução standalone para testes
if __name__ == "__main__":
    render()