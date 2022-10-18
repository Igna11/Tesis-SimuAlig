Programa escrito en C que coexiste con un script en python para levantar los datos que simula el programa y graficarlos. A su vez, hay un script en python que hace la simulación y grafica. Estos son:
```
    ARCHIVOS PROGRAMA C         |         SCRIPT EN PYTHON
--------------------------------|----------------------------------
    SimuScatteringAlig.c        |
    auxiliares_Alig.c           |
    auxiliares_Alig.h           |
    ----------------------      |    SimulacionScatteringAlig.py
    SimuC2PyandPlotAlig.py      |
    ----------------------      |
    datos_simulacion_alig.txt   |
--------------------------------|---------------------------------
```
Se supone que ambos hacen exactamente lo mismo. Pero la idea con la que estan codeados ambos es idéntica. Se hace una recursión para contar todos los electrones que son ionizados en un proceso de scattering muy simplificado, hasta que la energía se agota completamente tanto por ionización como por emisión de fonones.