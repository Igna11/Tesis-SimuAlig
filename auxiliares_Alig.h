//=============================================================================
// 02/06/2021
#ifndef AUXILIARES_ALIG_H
#define AUXILIARES_ALIG_H
#include "math.h"

double Random();	
double Gaussiana(double mu, double sigma);
double Peh(double E_r, double A); 
double alpha(double E_r);
double *evolucionar(double E_r, double A, void * rand_beta);
double *evolucionar_aux(double E_r, double A);
int recursion(double E_r, double A, void * rand_beta);

#endif