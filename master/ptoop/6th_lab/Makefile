build-plugins:
	@javac -Xlint:none --class-path ./src -d ./plugins/out ./plugins/src/plugins/*.java
	@mkdir -p ./out/plugins/
	@cp ./plugins/out/plugins/*.class ./out/plugins/

build:
	@javac -Xlint:none --class-path ./src -d ./out ./src/**/*.java

run: build
	@cd out/ && java main.Main main

clean:
	@rm -rf ./out
	@rm -rf ./plugins/out
