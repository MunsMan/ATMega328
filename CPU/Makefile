CFLAGS = -Wall -Wextra -Werror -std=gnu11
LFLAGS =

INCLUDES = include
SRC = src
BIN = bin

EXECUTABLE = main

$(EXECUTABLE): $(SRC)/*.c $(SRC)/**/*.c
	$(CC) $(CFLAGS) -I $(INCLUDES) -o $(BIN)/$@ $^ 

debug: $(SRC)/*.c $(SRC)/**/*.c
	$(CC) $(CFLAGS) -I $(INCLUDES) -g $^ -o $(BIN)/$@