//=============================================================================
// 02/06/2021
#include "auxiliares_Alig.h"
#include "stdlib.h"
#include "math.h"
#include "gsl/gsl_randist.h"
#include "time.h"

double Random()
{
	// ========================================================================
	// Genera realizaciones de un variable aleatoria Uniforme entre 0 y 1
	// ========================================================================
	return ((double)rand()) / ((double) RAND_MAX);
}

double Gaussiana(double mu, double sigma)
{
	// ========================================================================
	// Genera realizaciones de un variable aleatoria Normal(mu, sigma)
	// ========================================================================
	int i;
	int n = 10;
	double z = 0;
	
	for(i = 0; i < n; i++)
	{
		z += Random();
	}
	z = sqrt(12 * (double)n) * (z / (double)n - 0.5);
	return z * sigma + mu;
}

double Peh(double E_r, double A)
{
	// ========================================================================
	// Calcula la probabilidad de ionizar usando la energia de Recoil:
	// ---------------------------------------------------------------
	// ______________________________________________________________
	// referencia: Ionization Yield in Silicon for eV-Scale Electron-Recoil
	// Processes - K. Ramanathan, N. kurinsky.
	// eq 10 - página 3.
	// ========================================================================
	double h_omega = 0.063;				// Energía de los fonones
	double E_g = 1.1;					// Energía del gap del Si
	double Gamma_ph = 0.0;				// Inicializo la variable
	double Gamma_eh = 0.0;				// Inicializo la variable
	double P = 0.0; 					// Inicializo la variable

	if(E_r > E_g){

		Gamma_ph = 105 * pow((E_r - h_omega), 1 / 2.0);
		Gamma_eh = 2 * M_PI * pow((E_r - h_omega), 7 / 2.0);

		P = 1 / (1 + A * Gamma_ph / Gamma_eh);
	}
	else{

		P = 0;
	}
	return P;
}

double alpha(double E_r)
{
	// ========================================================================
	// Calcula el valor del parámetro alpha para la distribución beta:
	// ---------------------------------------------------------------
	// Si la energía de recoil (E_r) es menor que la energía del gap (E_g),
	// alpha es pequeño (arbitrariamente elegido como 0.1)
	// *
	// Si la energía de recoil (E_r) está entre la energía del gap (E_g) y dos
	// veces la energía del gap (2*E_g), alpha = 1 y beta es una uniforme.
	// *
	// Si la energía de recoil (E_r) es mayor que dos veces la energía del gap
	// (2*E_g), entonces alpha es una función lineal tal que alpha(2E_g) = 1 y
	// alpha(677 eV) = 15 (donde se eligieron arbitrariamente. Según el paper
	// alpha tiende a infinito para valores muy grandes de energia. ¿Cuánto es
	// infinito en este contexto? bueno, no sé)
	// ______________________________________________________________
	// referencia: Ionization Yield in Silicon for eV-Scale Electron-Recoil
	// Processes - K. Ramanathan, N. kurinsky.
	// página 3, 3 casos listados, ecuación 7 y FIG 1.
	// ========================================================================
	double E_g = 1.1; 					// eV energía del gap
	double alpha_val = 0.0; 			// Inicializo la variable

	if(E_r < E_g)
	{
		alpha_val = .1;
	}
	else if(E_g <= E_r && E_r <= 2*E_g)
	{ 
		alpha_val = 1.0;
	}
	else if(3.4 <= E_r && E_r <= 4.2)
	{
		alpha_val = 1.0;
	}
	else
	{
		alpha_val = 0.0207*E_r + 0.95435;
	}
	return alpha_val;
}


double *evolucionar(double E_r, double A, double E_loss, void * rand_beta)
{
	// ========================================================================
	// Genera la evolución del sistema:
	// --------------------------------
	// Usando E_r, el parámetro A, se fija cuántas ionizaciones hace el primer
	// electrón y returnea todos los valores de energia que repartió.
	// ========================================================================
	

	// ==============================================================
	// Defino constantes iniciales
	double h_omega = 0.063;				// Energía de los fonones
	double E_g = 1.1;					// Energía del gap del

	double p_eh = 0.0;					// Inicializo variable
	double p_rand = 0.0;				// Inicializo variable
	double alpha_val = 0.0;				// Inicializo variable
	double E_transf = 0.0;				// Inicializo variable


	// ==============================================================
	// malloqueo el vector vec_ener donde se van a guardar las
	// energías repartidas. El tamaño 50 es arbitrario pero seguro 
	// nunca es superado
	double *vec_ener = malloc(sizeof(double)*50);


	// ==============================================================
	// inicializo el vec_ener[50] a 0
	int i;
	for(i = 0; i < 50; i++)
	{
		vec_ener[i] = 0;
	}
	// ==============================================================
	// re-inicializo i=0 como contador para los loops del while
	i = 0;

	// ==============================================================
	// si la variable atraviesa = 0, entonces uso el pedazo de codigo
	// con el while, ya que no seatraviesa el material


	// ==========================================================
	// Inicio el while hasta que se acabe energia para ionizar
	while(E_r > E_g)
	{
		// ======================================================
		// Calculo la probabilidad de ionizar. Genero un p_rand 
		// uniforme para comparar. Calculo el valor de alpha para
		// la beta. A partir de la beta calculo E_transferido
		p_eh = Peh(E_r, A);
		p_rand = Random();
		alpha_val = alpha(E_r);
		E_transf = gsl_ran_beta(rand_beta, alpha_val, alpha_val) * (E_r - E_g);


		// ======================================================
		// Si se cumple que la probabilidad de ionizar es mayor
		// que el p_rand y que la E_transferidaes mayor que una
		// energia A TUNEAR, entonces ionizo.

		if(p_rand < p_eh && E_transf > 3.75)
		{
			//printf("E_transf = %lf\n", E_transf);
			E_r -= E_transf;
			vec_ener[i] = E_transf - E_loss;
			i++;
		}
		else
		{
			E_r -= h_omega;
		}
	}
	
	return vec_ener;
}


double *evolucionar_aux(double E_r, double A)
{
	// ==============================================================
	// FUNCIÓN DE TESTEO PARA LA RECURSIÓN:
	// -----------------------------------
	// Genera la evolución del sistema pero divide cada energia en 2,
	// es decir: Si E_r = 500, entonces las divisiones de esa energía
	// serán: 
	//		250,
	//		125,
	//		62.5,
	//		31.25,
	// 		15.625,
	//		7.8125,
	//		3.90625,
	// 		1.953125,
	// 		0.9765625,
	// y resulta que siguiendo esa regla, si para una dada energía E
	// se generan N energías E_n > 1, entonces la cantidad total de
	// divisiones de energía que se pueden obtener es 2**N, de forma
	// que se puede calcular exactamente cuántas divisiones hubo.
	// Sabiendo exactamente cuantas divisiones hubo, si lo meto en la
	// recursión y obtengo ese valor, entonces la recursión hace lo
	// correcto.
	// ==============================================================
	

	//=================================
	// malloqueo el vector vec_ener
	// donde se van a guardar las
	// energías repartidas. El tamaño
	// 50 es arbitrario pero seguro 
	// nunca es superado
	double *vec_ener = malloc(sizeof(double)*50);
	
	// ================================
	// inicializo el vec_ener[50] a 0
	int i;
	for(i = 0; i < 50; i++)
	{
		vec_ener[i] = 0;
	}
	// ================================
	// re-inicializo i=0 como contador
	// para los loops del while
	i = 0;
	

	// ================================
	// Inicio el while hasta que se
	// acabe energia para ionizar
	while(E_r > 1)
	{
		E_r/=2;
		//printf("E_r = %lf\n", E_r);
		vec_ener[i] = E_r;
		i++;
	}
	return vec_ener;
}

int recursion(double E_r, double A, double E_loss, void * rand_beta)
{

	// ==============================================================
	// Hace la recursión y cuenta cuántos electrones son ionizados
	// en cascada
	// *
	// Para probarla a ver si cuenta bien, comentar la linea
	// Energia = evolucionar(E_r, A, rand_beta) y descomentar la
	// la linea
	// Energia = evolucionar_aux(E_r, A) y en el main darle E_r = 30.
	// El resultado debería ser 2**5 = 32, pero da 31 y eso es enough
	// ==============================================================
	int i = 0; 					// Inicializo la variable contador i
	int j = 0;					// Inicializo la variable contador auxiliar j
	double *Energia;			// Inicializo la variable
	
	Energia = evolucionar(E_r, A, E_loss, rand_beta);
	//Energia = evolucionar_aux(E_r, A);

	while(Energia[j] > 0.0){
		
		i++; // cuento la cantidad de electrones
		i += recursion(Energia[j], A, E_loss, rand_beta);
		j++; // aumento el contador j para finalizar el while

	}
	free(Energia);
	return i;
}
