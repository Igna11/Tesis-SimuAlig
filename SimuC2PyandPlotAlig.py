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
os.system("gcc -Wall -o SimuAlig SimuScatteringAlig.c auxiliares_Alig.c -lm -lgsl")

# =============================================================================
# Parámetros para el programa de C
Cprogram = "./SimuAlig "
trials = "1000 "
Energia = "677 "
A = "1 "

# =============================================================================
# string que escribo en consola para correr el programa de C
path = Cprogram + Energia + A +  trials
# un simple cronómetro
t0 = time.time()
# =============================================================================
# llamo al programa de C y
a = os.system(path)
# =============================================================================
# veo cuánto tardó en correr
print(time.time() - t0)

# =============================================================================
# Levanto datos con numpy y los ordeno
datos = np.loadtxt("datos_simulacion_alig.txt", skiprows=1)
choques_e = datos

# =============================================================================
# Armo los gráficos
x0 = min(choques_e)         # desde donde grafico
xf = max(choques_e)         # hasta donde grafico
x = np.arange(x0, xf, 1)    # vector para graficar la gaussiana
bins = len(x)               # cantidad de bines igual a la longitud del vector
mu = np.mean(choques_e)     # media de la distribución
sigma = np.std(choques_e)   # desviación estandar de la dist
normal = norm.pdf(x, mu, sigma)


fig, axs = plt.subplots(1, 2, figsize=(20, 9))
axs[0].hist(choques_e, bins=bins,
            density=True,
            label="choques_e",
            width=.6,
            align="mid",
            color="#56B4E9")
axs[0].plot(x, normal,
            ".-",
            label="Gaussiana",
            markersize=9,
            color="#E69F00")
###################
axs[0].plot(x, poisson.pmf(x, mu),
            ".-",
            label="Poissoniana",
            markersize=15,
            color="#009E73")
axs[0].legend(fontsize=19)
fano = np.std(choques_e)**2/np.mean(choques_e)
axs[0].text((xf+x0)/2, max(normal)/2,
            "fano = %.4f" % fano,
            fontsize=15)

# axs[2].hist(choques_n, bins=50,
#             density=True,
#             label="choques_n",
#             width=.6,
#             align="mid")
# axs[2].legend(fontsize=15)
plt.show()
# fig.savefig("hist_ev_dist_2Modif_0_noatr_2e.pdf")
