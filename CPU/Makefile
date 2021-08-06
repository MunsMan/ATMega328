CFLAGS = -Wall -Wextra -Werror -std=gnu11
LFLAGS =

INCLUDES = include
SRC = src
BIN = bin

EXECUTABLE = main

clean:
	$(RM) -r $(BIN)/*

$(EXECUTABLE): $(SRC)/*.c $(SRC)/**/*.c
	$(CC) $(CFLAGS) -I $(INCLUDES) -o $(BIN)/$@ $^ 

debug: $(SRC)/*.c $(SRC)/**/*.c
	$(CC) $(CFLAGS) -I $(INCLUDES) -g $^ -o $(BIN)/$@

shared: $(SRC)/*.c $(SRC)/**/*.c
	$(CC) $(FLAGS) -I $(INCLUDES) -shared -o $(BIN)/test.so $^

test: shared
	pytest