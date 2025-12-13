# LiFi Optical Communication Simulation

This project simulates a simplified LiFi communication chain using Python.

## Description

- Binary data transmitted using a LED (square signal)
- Photodiode modeled as a first-order RC circuit
- Differential equation solved using `odeint`
- Additive Gaussian noise
- Bit Error Rate (BER) computation

## Mathematical model

The photodiode is modeled as:
τ dS_elec/dt + S_elec = S_LED

## Tools

- Python
- NumPy
- Matplotlib
- SciPy

## Author

Allé Seck
