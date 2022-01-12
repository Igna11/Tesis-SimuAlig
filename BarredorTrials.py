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

# =============================================================================
# compilo el script siempre antes de correrlo porque por qué no
os.system("make")
# =============================================================================
# Parámetros para el programa de C
Trials = np.arange(100000,101000,100)
fano_vec = []
i = 0
progreso = 0
t0 = time.time()
for trial in Trials:
    # ========================================================
    # progreso de los experimentos
    print("\r%.2f%% terminado" %(progreso*100/len(Trials)), end = "")
    progreso += 1
    # ========================================================
    # Experimentos
    i += 1
    Cprogram = "./SimuAlig "
    Energia = "677 "
    A = "5.2 "
    E_loss = "0 "
    trials = str(trial) + " "
    atraviesa = "0 "
    c_prog = "0 "
    path = Cprogram + Energia + A + E_loss + trials + atraviesa + c_prog
    # llamo al programa de C y
    b = os.system(path)
    datos = np.loadtxt("datos_simulacion_alig.txt", skiprows=1)
    choques_e = datos
    mu = np.mean(choques_e)
    sigma = np.std(choques_e)
    fano_vec.append(sigma ** 2 / mu)
#%%
t1 = time.time()
T = t1-t0
fano_np_vec = np.array(fano_vec)
min_trial = Trials[0]
max_trial = Trials[-1]
np.savetxt(f"fano_np_vec_{min_trial}_{max_trial}.txt", fano_np_vec)
print(f"\ntarde {T:.2f}s en hacer {len(Trials)} corridas")
#Fano = np.array(sigma_vec)**2/np.array(mu_vec)
plt.figure()
plt.plot(Trials, np.array(fano_vec), '.')
plt.title("Factor de Fano vs Trials")
plt.xlabel("Numero de trials", fontsize = 15)
plt.ylabel("$F = \sigma^2/\mu$", fontsize = 18)
plt.grid()
#plt.savefig("fanovsEloss.png", transparent=True)
#%%  
#plt.figure()
#plt.plot(Trials, mu_vec, '.')
#plt.title("$\mu$ vs E_loss")
#plt.xlabel("$E_{loss}$", fontsize = 15)
#plt.ylabel("$\mu$", fontsize = 18)
#plt.grid()
#plt.savefig("MuvsEloss.png", transparent=True)
#%%
#plt.figure()
#plt.plot(Trials, 677/np.array(mu_vec), '.')
#plt.title("$\epsilon_{eh}$ vs $E_{loss}$")
#plt.xlabel("$E_{loss}$", fontsize = 15)
#plt.ylabel("$\epsilon_{eh}$", fontsize = 18)
#plt.grid()
#plt.savefig("MuvsEloss.png", transparent=True)
#print("Fano = %.2f \pm %.2f", (np.mean(Fano), np.std(Fano)))
#del i, t0, trials, path, Energia, atraviesa, A, b, datos
plt.show()