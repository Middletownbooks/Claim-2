CFLAGS = -O3 -march=native -funroll-loops -Wall -Wextra -std=c11
all: zsearch
zsearch: search.c cog.c cog.h
	$(CC) $(CFLAGS) -o zsearch search.c cog.c
clean:
	rm -f zsearch
