TARGETS = kaylee.js kldemo.js klconsole.js

all: $(TARGETS)

kaylee.js: kaylee.coffee
	coffee -c kaylee.coffee 

kldemo.js: kldemo.coffee
	coffee -c kldemo.coffee 

klconsole.js: klconsole.coffee
	coffee -c klconsole.coffee 

clean:
	rm -f *.js
