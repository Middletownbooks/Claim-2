CFLAGS = -O3 -march=native -funroll-loops -Wall -Wextra -std=gnu11
all: zsearch zrefute
zsearch: search.c cog.c cog.h
	$(CC) $(CFLAGS) -o zsearch search.c cog.c
zrefute: refute.c
	$(CC) $(CFLAGS) -o zrefute refute.c -lm
clean:
	rm -f zsearch zrefute
