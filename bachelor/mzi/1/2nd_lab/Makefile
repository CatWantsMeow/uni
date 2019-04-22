TEST_COUNT = 40
TEST_LENGTH = 1000000
TESTGEN_SORUCES = sources/testgen/testgen.c

KEY = '1234567812345ab8'
INPUT = 'sample/text'
ENCRYPTED_OUTPUT = 'sample/encrypted'
DECRYPTED_OUTPUT = 'sample/decrypted'

SOURCES = sources/tea/tea.c \
		  sources/tea/tea.h \
		  sources/maa/maa.h \
		  sources/maa/maa.c \
		  sources/main.c

build: $(SOURCES) $(TESTGEN_SORUCES)
	@gcc -std=c99 -o testgen $(TESTGEN_SORUCES)
	@gcc -std=c99 -o tea $(SOURCES)

run: build
	@./tea encrypt $(KEY) $(INPUT) $(ENCRYPTED_OUTPUT)
	@./tea decrypt $(KEY) $(ENCRYPTED_OUTPUT) $(DECRYPTED_OUTPUT)
	@cmp -l $(INPUT) $(DECRYPTED_OUTPUT)

genkey: build
	@./tea generate_key

gentests: build
	@mkdir -p tests
	@./testgen $(TEST_COUNT) $(TEST_LENGTH)

test: build gentests test.sh
	@./test.sh

clean:
	@rm -rf $(ENCRYPTED_OUTPUT) $(DECRYPTED_OUTPUT)
	@rm -rf tea testgen a.out
	@rm -rf tests/*.test
