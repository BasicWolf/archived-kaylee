TARGETS = kaylee.js klworker.js
KL_COFFEE = klshared.coffee klutil.coffee klajax.coffee klbenchmark.coffee \
			kaylee.coffee 
KL_WORKER_COFFEE = klshared.coffee klutil.coffee klajax.coffee klworker.coffee

ifeq ($(origin KL_BUILD_DIR), environment)
KL_JS_DIR = $(KL_BUILD_DIR)/static/js/kaylee
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif


all: $(TARGETS)

kaylee.js: $(KL_COFFEE)
	coffee -j kaylee.js -c $(KL_COFFEE)

klworker.js: $(KL_WORKER_COFFEE)
	coffee -j klworker.js --bare -c $(KL_WORKER_COFFEE)

remote:
	mkdir -p $(KL_JS_DIR)
	cp *.js $(KL_JS_DIR)

clean: $(CLEAN_TARGETS)
	rm -f *.js

clean_remote:
	rm -rf $(KL_JS_DIR)
