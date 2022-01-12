#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02/06/2021

@author: igna
"""

import os
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson
from scipy.stats import norm

directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory)

# =============================================================================
# compilo el script siempre antes de correrlo porque por qué no
os.system("make")

# =============================================================================
# Parámetros para el programa de C
Cprogram = "./SimuAlig "
Energia = "677 "
A = "20 "
E_loss = "0 "
trials = "10000 "
c_prog = "1 "

# =============================================================================
# string que escribo en consola para correr el programa de C
path = Cprogram + Energia + A + E_loss + trials + c_prog
# un simple cronómetro
t0 = time.time()
# =============================================================================
# llamo al programa de C y
a = os.system(path)
# =============================================================================
# veo cuánto tardó en correr
print("Tiempo: %.2f" % (time.time() - t0))

# =============================================================================
# Levanto datos con numpy y los ordeno
datos = np.loadtxt("datos_simulacion_alig.txt", skiprows=1)
choques_e = datos
np.savetxt("Distribucion_carga_simulada_10k.txt", choques_e)
# =============================================================================
# Armo los gráficos
x0 = min(choques_e)  # desde donde grafico
xf = max(choques_e)  # hasta donde grafico
x = np.arange(x0, xf, 1)  # vector para graficar la gaussiana
bins = len(x)  # cantidad de bines igual a la longitud del vector
mu = np.mean(choques_e)  # media de la distribución
sigma = np.std(choques_e)  # desviación estandar de la dist
normal = norm.pdf(x, mu, sigma)


fig, ax = plt.subplots(figsize=(11, 9))
ax.hist(
    choques_e,
    bins=bins,
    density=True,
    label="Carga ionizada",
    width=0.6,
    align="mid",
    color="#56B4E9",
)
ax.plot(x, normal, "s-", label="Ajuste Gaussiano", markersize=9, color="#E69F00")
###################
ax.plot(
    x,
    poisson.pmf(x, mu),
    ".-",
    label="Ajuste Poissoniano",
    markersize=15,
    color="#009E73",
)
ax.legend(fontsize=19)
fano = np.std(choques_e) ** 2 / np.mean(choques_e)
ax.text(
    mu + sigma * 1.5,
    max(normal) / 2,
    "Fano = %.4f\n $\mu$ = %.0f" % (fano, mu),
    fontsize=15,
)

ax.tick_params(axis='both', which='major', labelsize=15)


plt.show()
# fig.savefig("hist_ev_dist_SIatr_fononOFF_loop3.png", transparent = True)
