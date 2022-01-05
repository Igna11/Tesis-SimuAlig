CC = gcc
CFLAGS = -Wall
BIN = SimuAlig
OBJECTS = SimuScatteringAlig.c auxiliares_Alig.c
ALL : $(BIN)
	@echo "Compilado"

$(BIN) : $(OBJECTS)
	$(CC) $(CFLAGS) -o $(BIN) $(OBJECTS) -lm -lgsl

clean:
	rm -f $(BIN)
	@echo "Borrado"