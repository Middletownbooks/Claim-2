CFLAGS = -O3 -march=native -funroll-loops -Wall -Wextra -std=gnu11
LDLIBS = -lpthread
all: zsearch zrefute zsearch6c ptcheck
zsearch: search.c cog.c cog.h
	$(CC) $(CFLAGS) -o zsearch search.c cog.c $(LDLIBS)
zrefute: refute.c
	$(CC) $(CFLAGS) -o zrefute refute.c -lm
zsearch6c: search6c.c pt.c pt.h cog.c cog.h
	$(CC) $(CFLAGS) -o zsearch6c search6c.c pt.c cog.c $(LDLIBS)
ptcheck: ptcheck.c pt.c pt.h cog.c cog.h
	$(CC) $(CFLAGS) -o ptcheck ptcheck.c pt.c cog.c
clean:
	rm -f zsearch zrefute zsearch6c ptcheck
