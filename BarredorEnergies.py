#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 22:30:38 2022

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

# ============================================================================
# compilo el script siempre antes de correrlo porque por qué no
os.system("make")
# ============================================================================
# Parámetros para el programa de C
Energies = np.linspace(200,7000,20)
fano_vec = []
i = 0
progreso = 0
t0 = time.time()
for energy in Energies:
    # ========================================================================
    # progreso de los experimentos
    print("\rEnergia: %.2f - %.2f%% terminado" %(energy, progreso*100/len(Energies)), end = "")
    progreso += 1
    # ========================================================================
    # Experimentos
    i += 1
    Cprogram = "./SimuAlig "
    Energia = str(energy) + " "
    A = "5.2 "
    E_loss = "0 "
    trials = "10000 "
    atraviesa = "0 "
    c_prog = "0 "
    run_command = Cprogram + Energia + A + E_loss + trials + atraviesa + c_prog
    # llamo al programa de C y
    b = os.system(run_command)
    datos = np.loadtxt("datos_simulacion_alig.txt", skiprows=1)
    choques_e = datos
    mu = np.mean(choques_e)
    sigma = np.std(choques_e)
    fano_vec.append(sigma ** 2 / mu)
#%%
t1 = time.time()
T = t1-t0
fano_np_vec = np.array(fano_vec)
min_energy = Energies[0]
max_energy = Energies[-1]
np.savetxt(f"fano_np_vec_E{min_energy}_E{max_energy}.txt", fano_np_vec)
print(f"\ntarde {T:.2f}s en hacer {len(Energies)} corridas")
#Fano = np.array(sigma_vec)**2/np.array(mu_vec)
plt.figure()
plt.plot(Energies, np.array(fano_vec), '.')
plt.title("Factor de Fano vs Trials")
plt.xlabel("Energias", fontsize = 15)
plt.ylabel("$F = \sigma^2/\mu$", fontsize = 18)
plt.grid()
plt.show()