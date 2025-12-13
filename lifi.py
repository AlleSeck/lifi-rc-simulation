import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------
# PARAMÈTRES GÉNÉRAUX
# -----------------------
fs = 10000          # fréquence d’échantillonnage (Hz)
dt = 1/fs
Tb = 0.01           # durée d'un bit (s)
Nbit = int(fs * Tb) # nb d'échantillons par bit doonc j'aurai 100
Tau = 0.015         # constante de temps RC ( ms)
NoiseSigma = 0.15   # écart-type du bruit gaussien (à ajuster)


# 1) Génération des bits

bitsSent = np.random.randint(0, 2, 50)
print("Bits envoyés :", bitsSent)


# 2) Génération du signal carré LED

signal_Square = np.repeat(bitsSent, Nbit)

# 3) Équation différentielle RC
# dy/dt = (x - y) / Tau

def rc_diff(y, t, x, Tau):
    idx = min(int(t * fs), len(x) - 1)
    return (x[idx] - y) / Tau


# 4) Résolution par ODEINT

t_vec = np.arange(0, len(signal_Square) * dt, dt)
filtered_signal = odeint(rc_diff, 0, t_vec, args=(signal_Square, Tau)).flatten()


# 5) Ajout du bruit gaussien

noise = np.random.normal(0, NoiseSigma, len(filtered_signal))
noisy_signal = filtered_signal + noise


# 6) Décision (seuil fixe à 0.5)

samples = noisy_signal.reshape(-1, Nbit)
bit_decision = (np.mean(samples, axis=1) > 0.5).astype(int)


# 7) Calcul du BER

BER = np.mean(bit_decision != bitsSent)*100
print("Bits reçus :", bit_decision)
print("BER =", BER, "%")



# 8) Affichage

plt.figure(figsize=(12,5))

plt.plot(signal_Square[:1500], label="Signal LED", linewidth=0.8)
plt.plot(filtered_signal[:1500], label="Signal RC", linewidth=1.3)
plt.plot(noisy_signal[:1500], label="Signal bruité", linewidth=0.8)

plt.title("Chaîne optique : LED → RC → bruit")
plt.xlabel("Échantillons")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

