CFLAGS = -Wall -Wextra -Werror -std=gnu11

BIN = bin
SRC = src
INCLUDE = include

LIBRARIES =
EXECUTABLE  = main

.PHONY: all
all: $(BIN)/$(EXECUTABLE)

run: clean all
	./$(BIN)/$(EXECUTABLE) $(ARGS)

test: clean shared
	pytest 

clean:
	$(RM) -r $(BIN)/*

$(BIN)/$(EXECUTABLE): $(SRC)/*.c
	$(CC) $(CFLAGS) -I $(INCLUDE) $^ -o $@ $(LIBRARIES)

.PHONY: debug
debug: $(SRC)/*.c
	$(CC) $(CFLAGS) -I $(INCLUDE) -g $^ -o $(BIN)/$@ $(LIBRARIES)

shared: $(SRC)/C*.c $(SRC)/A*.c $(SRC)/O*.c $(SRC)/R*.c
	$(CC) $(FLAGS) -I $(INCLUDE) -shared  -o $(BIN)/test.so $^

