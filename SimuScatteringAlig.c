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
	double energia, A;
	int k, trials, electrones;


//=============================================================================
	
	// Argumentos iniciales
	if(argc > 1){

		sscanf(argv[1], "%lf", &energia);
		sscanf(argv[2], "%lf", &A);
		sscanf(argv[3], "%i", &trials);

	}

	else{

		energia = 677;
		trials = 2000;
		A = 5.2;
	}
	

//=============================================================================

	//===============================================
	// Inicializo la variable para guardar el archivo
	FILE* fp;
	fp = fopen("datos_simulacion_alig.txt", "w");
	fprintf(fp, "electrones\n");

//=============================================================================

	for(k = 0; k < trials; k++)
	{
		//double * vec_ener;
		electrones = recursion(energia, A, rand_beta);
		printf("%i: electrones ionizados = %i\n", k, electrones);
		//free(vec_ener);
		fprintf(fp, "%i\n", electrones);
	}

	//===============================================
	// Cierro el archivo
	fclose(fp);
	
	return 0;
}