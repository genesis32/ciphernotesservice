CC=gcc
CFLAGS=-Wno-deprecated-declarations 
LIBS=-lssl -lcrypto 

encrypt: cncrypto.c
	$(CC) -c cncrypto.c $(CFLAGS) 
	ld -macosx_version_min 10.7 -bundle -flat_namespace -undefined suppress -o libcncrypto.so cncrypto.o $(LIBS) 

clean:
	rm -f *.pyc *.so *.o;
