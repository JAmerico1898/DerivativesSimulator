# Derivatives Simulator

A comprehensive interactive educational tool for understanding and visualizing various financial derivatives.

## Overview

The Derivatives Simulator is an educational Streamlit application designed to help students and finance professionals understand the mechanics and behaviors of different financial derivatives. The application provides interactive simulations, visualizations, and explanations for:

- Options (European and American)
- Forwards
- Futures
- Swaps

Each module allows users to manipulate parameters and immediately see the impact on pricing, payoffs, and risk profiles.

## Features

### Options Module

- **Option Simulator**: Interactive tool to visualize option payoffs and profits
  - Supports both European and American options
  - Buy/Sell positions for Calls and Puts
  - Real-time calculation of option premium using Black-Scholes
  - Visualization of payoff and profit diagrams
  - Greeks calculation (Delta, Gamma, Theta, Vega)

- **Option Strategies**: Explore complex option strategies based on market outlook
  - Long Call/Put
  - Short Call/Put
  - Covered Call
  - Protective Put
  - Bull Call Spread
  - Bear Put Spread
  - Long Straddle
  - Iron Condor
  - And more

- **Educational Resources**: Learn option basics through quizzes and reference materials

### Forward Contracts Module

- Brazilian-style forward contract simulator
- Interactive visualization of hedging effectiveness
- Adjustable parameters for notional amount, time period, and rates
- Support for both floating and fixed rate exposures

### Futures Module

- Oil futures contract simulation
- Margin account evolution tracking
- Mark-to-market settlement calculations
- Comparison of speculative vs. hedging applications

### Swaps Module

- Brazilian swap calculator with detailed analysis
- Support for various indexer types (pre-fixed, post-fixed, exchange rate)
- Asset and liability leg configurations
- Visualization of position evolution over time
- Comprehensive reports with exposure and hedge results

## How to Use

1. **Installation**: Clone the repository and install the required packages:
   ```bash
   pip install streamlit numpy pandas plotly scipy matplotlib
   ```

2. **Run the application**:
   ```bash
   streamlit run DerivativesSimulator.py
   ```

3. **Navigation**: Select your desired derivative type from the top navigation menu and explore the interactive tools.

## Educational Purpose

This application is designed primarily for educational purposes to help students understand:

- The mechanics of different derivative contracts
- Risk-reward profiles of various derivatives and strategies
- The impact of parameter changes on derivative pricing
- Hedging applications of derivatives
- Advanced concepts like option Greeks and strategies

## Technical Implementation

The application is built using:
- Streamlit for the interactive web interface
- Pandas and NumPy for data handling and calculations
- Plotly and Matplotlib for interactive visualizations
- SciPy for statistical calculations (notably in the Black-Scholes implementation)
- Python dataclasses and enums for structured data management

## Acknowledgements

This project was developed as a teaching tool for post-graduate finance education. Special thanks to all contributors who helped improve the application's functionality and educational content.

## License

This project is available for educational use.

## Contact

For questions or feedback about this application, please contact [tesouraria.rj@gmail.com].
