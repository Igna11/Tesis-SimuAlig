//=============================================================================
// 02/06/2021 V1 funcional: No sé bien como funcionara el free(vec_ener) pero
// 							no debería romper nada. 
//
//						=======================================================
//						=======================================================
//						//  OJO! 20000 trials equivalen a 1.6gb de memoria!! //
//						//  (veinte mil trials equivalena 1.6gb de memoria!!)//
//						=======================================================
//						=======================================================					
//		
/* gcc -Wall -o SimuAlig SimuScatteringAlig.c auxiliares_Alig.c -lm -lgsl*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <gsl/gsl_randist.h>

#include "auxiliares_Alig.h"

int main(int argc, char *argv[]){

//=============================================================================

	//===============================================
	// Semilla para randoms uniformes
	srand(time(0));
	//===============================================
	// Inicialización para la beta
	gsl_rng * rand_beta = gsl_rng_alloc (gsl_rng_taus);

	// Semilla para la random beta
	gsl_rng_set(rand_beta, time(0));

	//===============================================
	// Declaro variables
	double energia, A, E_loss;
	int trials, atraviesa, electrones, print_progreso;


//=============================================================================
	
	// Argumentos iniciales
	if(argc > 1){

		sscanf(argv[1], "%lf", &energia);
		sscanf(argv[2], "%lf", &A);
		sscanf(argv[3], "%lf", &E_loss);
		sscanf(argv[4], "%i", &trials);
		sscanf(argv[5], "%i", &atraviesa);
		sscanf(argv[6], "%i", &print_progreso);

	}

	else{

		energia = 677;
		A = 5.2;
		E_loss = 0.0;
		trials = 2000;
		atraviesa = 0;
		print_progreso = 1;
	}
	

//=============================================================================

	//===============================================
	// Inicializo la variable para guardar el archivo
	FILE* fp;
	fp = fopen("datos_simulacion_alig.txt", "w");
	fprintf(fp, "electrones\n");

//=============================================================================
	// Variables para ver el progreso
	int prog_count = 0;
	double prog;

	for(int k = 0; k <= trials; k++)
	{
		electrones = recursion(energia, A, E_loss, atraviesa, rand_beta);
		//printf("%i: electrones ionizados = %i\n", k, electrones);
		fprintf(fp, "%i\n", electrones);

		// Algunas cuentas para ver el progreso de la simulación
		if(print_progreso == 1)
		{
			prog = prog_count*100/(double)trials;
			printf("\rProgreso: %.2lf%% Terminado", prog);
			prog_count++;
			fflush(stdout);
			printf(" ");
		}

	}
	//printf("atraviesa mode: = %i\n", atraviesa);
	//===============================================
	// Cierro el archivo
	fclose(fp);
	
	return 0;
}