TARGETS = kaylee.js kldemo.js klconsole.js klworker.js

all: $(TARGETS)

kaylee.js: kaylee.coffee
	coffee -j kaylee.js -c kaylee.coffee 

klworker.js: klworker.coffee
	coffee --bare -c klworker.coffee

kldemo.js: kldemo.coffee
	coffee -c kldemo.coffee 

klconsole.js: klconsole.coffee
	coffee -c klconsole.coffee 

clean:
	rm -f *.js
