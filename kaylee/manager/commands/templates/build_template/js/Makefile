TARGETS = kldemo.js

all: $(TARGETS)

kldemo.js: kldemo.coffee
	coffee -j kldemo.js -c kldemo.coffee klconsole.coffee

clean: 
	rm -f *.js
