CFLAGS = -Wall -Wextra -Werror -std=gnu11
LFLAGS =

INCLUDES = include
SRC = src
BIN = bin

EXECUTABLE = main

$(BIN)/$(EXECUTABLE): $(SRC)/*.c $(SRC)/**/*.c
	$(CC) $(CFLAGS) -I $(INCLUDES) -o $@ $^ 