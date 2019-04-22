CRYPTO_SOURCES = sources/crypto/crypto.h \
				 sources/crypto/crypto.c \

KERBEROS_SOURCES = sources/kerberos/as_server.c \
				   sources/kerberos/tgs_server.c \
				   sources/kerberos/server.c \
				   sources/kerberos/kdc.h \

SOURCES = $(CRYPTO_SOURCES) \
		  $(KERBEROS_SOURCES) \
		  sources/main.c \

EXECUTABLE_DIR = bin
EXECUTABLE = $(EXECUTABLE_DIR)/auth

build: $(SOURCES)
	@mkdir -p $(EXECUTABLE_DIR)
	@gcc -std=gnu99 $(SOURCES) -o $(EXECUTABLE)

run: build
	@./$(EXECUTABLE)
