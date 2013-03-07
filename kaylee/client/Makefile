TARGETS = kaylee.js klworker.js
KL_COFFEE = klshared.coffee klutil.coffee klajax.coffee klbenchmark.coffee \
			kaylee.coffee 
KL_WORKER_COFFEE = klshared.coffee klutil.coffee klajax.coffee klworker.coffee

COFFEE = coffee

all: $(TARGETS)

kaylee.js: $(KL_COFFEE)
	$(COFFEE) -j kaylee.js -c $(KL_COFFEE)

klworker.js: $(KL_WORKER_COFFEE)
	$(COFFEE) -j klworker.js --bare -c $(KL_WORKER_COFFEE)

clean: 
	rm -f *.js
