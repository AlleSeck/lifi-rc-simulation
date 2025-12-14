import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------
# PARAMÈTRES GÉNÉRAUX
# -----------------------
fs = 10000          # fréquence d’échantillonnage (Hz)
periode = 1/fs
Tb = 0.01           # durée d'un bit (s)
Nbit = int(fs * Tb) # nb d'échantillons par bit doonc j'aurai 100
Tau = 0.003         # constante de temps RC (5 ms)
NoiseSigma = 0.62   # écart-type du bruit gaussien (à ajuster)


# 1) Génération des bits

bitsSent = np.random.randint(0, 2, 50)
print("Bits envoyés :", bitsSent)


# 2) Génération du signal carré LED

signal_Square = np.repeat(bitsSent, Nbit)


# 3) Équation différentielle RC de la photodiode
# dSelec/dt = (Sled - Selec) / Tau

def PhotoDiode(Selec, t, Sled, Tau):
    idx = min(int(t * fs), len(Sled) - 1)
    return (Sled[idx] - Selec) / Tau


# 4) Résolution par ODEINT

t = np.arange(0, len(signal_Square) * periode, periode)
filtered_signal = odeint(PhotoDiode, 0, t, args=(signal_Square, Tau)).flatten()


# 5) Ajout du bruit gaussien

noise = np.random.normal(0, NoiseSigma, len(filtered_signal))
noisy_signal = filtered_signal + noise


# 6) Décision (seuil fixe à 0.5)
samples = noisy_signal.reshape(-1, Nbit)
bit_decision = (np.mean(samples, axis=1) > 0.5).astype(int)

# 7) Calcul du BER
BER = np.mean(bit_decision != bitsSent)
print("Bits reçus :", bit_decision)
print("BER =", BER)

# 8) Affichage
plt.figure(figsize=(12,5))

plt.plot(signal_Square[:1500], label="Signal LED", linewidth=0.8)
plt.plot(filtered_signal[:1500], label="Signal RC", linewidth=1.3)
plt.plot(noisy_signal[:1500], label="Signal bruité", linewidth=0.8)
plt.axhline(0.5, color='r', linestyle='--', label='Seuil(0.5)')

plt.title("Chaîne optique : LED → RC → bruit")
plt.xlabel("Échantillons (n)") 
plt.ylabel("Tension (V) ou Intensité Normalisée")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

