TARGETS = klconsole.js kldemo.js

all: $(TARGETS)

klconsole.js: klconsole.coffee
	coffee -j klconsole.js -c klconsole.coffee

kldemo.js: kldemo.coffee
	coffee -j kldemo.js -c kldemo.coffee

clean: 
	rm -f *.js
