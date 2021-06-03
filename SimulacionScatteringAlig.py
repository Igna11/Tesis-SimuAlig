#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 18:36:10 2021

@author: igna
"""

import numpy as np

import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.stats import beta
from scipy.stats import norm
import time
# %%


def Peh(E_r, A=5.2):
    """
    Probabilidad de ionizar, es función de la energía de recoil (recoil energy)
    y del parámetro A para que sea tuneable.
    A = 5.2 eV^3 por defecto, según el paper Ionization Yield
    Devuelve una probabilidad
    """
    h_omega = 0.063  # eV Energía de los fonones
    E_g = 1.1  # eV Energía del gap
    if E_r > E_g:
        Gamma_ph = 105*(E_r - h_omega)**(1/2)
        Gamma_eh = 2*np.pi*(E_r - E_g)**(7/2)
        return 1/(1 + A*Gamma_ph/Gamma_eh)
    else:
        return 0


def alpha(E_r):
    """
    Devuelve el valor de alpha a usar en la distribución beta, dada una energía
    de recoil

    ESTO NO SÉ SI ES COMO DARÍO PLANEABA QUE LO HICIERA, creo que él quería un
    alpha fijo
    """
    E_g = 1.1
    if E_r < E_g:
        alpha_val = 0.1
    elif E_g <= E_r and E_r <= 3.75:
        alpha_val = 1
    else:
        alpha_val = 0.0207*E_r + 0.95435
    return alpha_val


def evolucionar(E_r, A=5.2):
    """
    ==========================================================================
    Usando la recoil energy E_r, se fija cuántas ionizaciones hace el primer
    electrón y arma un generador con las energías de los electrones ionizados.
    ==========================================================================
    Calcula la probabilidad p_eh de generar un electrón-hueco usando la
    función Peh(E_r, A=5.2).

    Calcula el valor de alpha con alpha(E_r)

    Genera un numero random uniforme para comparar con p_eh para ver si se
    acepta o no la ionización. Si p_eh > p_rand, se acepta. Si no, se emite
    un fonón y no se guarda esa energía en la lista. Se repite el loop hasta
    que la E_r < E_g = 1.1, donde ya no se pueden generar mas pares e-h.
    """
    E_g = 1.1        # eV la energía del gap
    h_omega = 0.063  # eV la energía de los fonones
    while E_r > E_g:
        p_eh = Peh(E_r)
        p_rand = np.random.rand()
        alpha_val = alpha(E_r)
        E_transf = beta.rvs(a=alpha_val, b=alpha_val)*(E_r - E_g)
        # E_transf > E_g o E_transf > 3.75????
        if p_rand < p_eh and E_transf > 3.75:
            # lista.append(E_transf)
            # E_r -= E_transf o E_r -= E_transf + E_g?
            E_r -= E_transf
            yield E_transf
        else:
            E_r -= h_omega


def evolucionar_aux(energia):
    """
    función auxiliar y trivial:
    ¿Cómo usar esta función par saber si recursion(energia) hace lo que se
    necesita?
    Dada una energia inicial E, genero una cascada con N ramas en el nivel
    inicial:
        regla 1: La energia de cada rama será E/2**i, con i = 0,1,2,...,N
        regla 2: La última rama (de energia E/2**N) no puede generar más ramas
    Esto implica que si tengo una energía tal que, por ejemplo, en el primer
    nivel tengo 4 ramas, la rama de mayor energia de las 4 podrá generar 3
    ramas más en el 2do nivel, la rama siguiente podrá generar 2 ramas en el
    2do nivel, la siguiente podrá generar solo 1 rama y la última no podrá
    generar ninguna. Siguiendo con esta lógica, el número total de ramas que se
    pueden generar será de 2**N, con N el número de ramificaciones iniciales.

    Entonces, si a esta función le doy una energía que me genera 5 ramas (30
    por ejemplo: evolucionar_aux(30)), al usar esta energia en la función
    "recursion" con el modo test = True, el output de recursion deberia ser
    2**5 = 32 (recursion devuelve 31, pero no importa), y esa es la prueba
    de que recursion hace lo que yo quiero que haga.
    """
    while energia > 1:
        energia /= 2
        yield energia


def recursion(energia, test=False):
    """
    Esta función se ve sencilla pero no es trivial de entender (de hecho, no
    creo entenderla perfectamente, pero hace lo que se necesita, para verlo,
    probarla con la función de prueba evolucion(auxiliar)).

    Esta función toma una energia inicial (Recoil Energy, 677 eV) y le aplica
    la funcion evolucionar. La función "evolucionar" devuelve un generador con
    las energias que fueron distribuidas por ionización por el primer electrón,
    es decir, si el primer electrón tiene 677 eV, cada vez que ionizó otro le
    transfirió un dada cantidad de energia (aleatoria y definida por el
    algoritmo de evolucionar), digamos
        266.57
        181.44
        73.62
        96.72
        34.62
        4.41
        16.32
    Notar que estos valores de energia no son necesariamente decrecientes, esto
    es porque la energia repartida NO ES necesariamente decreciente, ni tiene
    por qué serlo.
    Luego, a cada una de esas energias se le vuelve a aplicar la función
    evolucionar, con lo cual se vuelve a armar un generador con las energias
    que salen de las ionizaciones que produjo un electron con una nueva energia
    inicial de 266.57, digamos
        180.59
        45.98
        29.62
        1.87
        4.62
        2.01
    Hay que repetir este proceso sobre estas energias, pero también hay que
    repetirlo sobre las energías restantes de la primera tanda de energias
    (181.44, 73.62, etc).
    Este proceso se repite para todas las energias hasta que el algoritmo de
    evolucionar decide que no se generaron más ionizaciones y se cuenta el
    numero total de electrones ionizados.
    """
    if test is True:
        energias = evolucionar_aux(energia)
    else:
        energias = evolucionar(energia)
    i = 0
    for E in energias:
        i += 1
        i += recursion(E, test)
    return i

# %%


t0 = time.time()
lista_electrones = [recursion(677) for i in range(1000)]
tiempo_t = time.time() - t0

# =============================================================================
# Armo los gráficos
choques_e = lista_electrones
x0 = min(choques_e)                   # desde donde grafico
xf = max(choques_e)                   # hasta donde grafico
x = np.arange(x0, xf, 1)            # vector para graficar la gaussiana
bins = len(x)              # cantidad de bines igual a la longitud del vector
mu = np.mean(choques_e)               # media de la distribución
sigma = np.std(choques_e)             # desviación estandar de la dist
normal = norm.pdf(x, mu, sigma)


fig, ax = plt.subplots(figsize=(11, 9))
ax.hist(choques_e, bins=bins,
        density=True,
        label="choques_e",
        width=.6,
        align="mid",
        color="#56B4E9")
ax.plot(x, normal,
        ".-",
        label="Gaussiana",
        markersize=9,
        color="#E69F00")
###################
ax.plot(x, poisson.pmf(x, mu),
        ".-",
        label="Poissoniana",
        markersize=15,
        color="#009E73")
ax.legend(fontsize=19)
fano = np.std(choques_e)**2/np.mean(choques_e)
ax.text((xf+x0)/2, max(normal)/2,
        "fano = %.4f\n $\mu$ = %.0f" % (fano, mu),
        fontsize=15)

# axs[2].hist(choques_n, bins=50,
#             density=True,
#             label="choques_n",
#             width=.6,
#             align="mid")
# axs[2].legend(fontsize=15)
plt.show()
print(tiempo_t)
