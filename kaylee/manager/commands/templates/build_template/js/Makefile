TARGETS = kldebug.js

all: $(TARGETS)

kldebug.js: kldebug.coffee klconsole.coffee
	coffee -j kldebug.js -c kldebug.coffee klconsole.coffee

clean: 
	rm -f kldebug.js
