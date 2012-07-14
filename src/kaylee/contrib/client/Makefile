TARGETS = kaylee.js klworker.js

ifeq ($(origin KL_BUILD_DIR), environment)
KL_JS_DIR = $(KL_BUILD_DIR)/static/js/kaylee
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif


all: $(TARGETS)

kaylee.js: kaylee.coffee
	coffee -j kaylee.js -c kaylee.coffee klajax.coffee

klworker.js: klworker.coffee
	coffee --bare -c klworker.coffee

remote:
	mkdir -p $(KL_JS_DIR)
	cp *.js $(KL_JS_DIR)


clean: $(CLEAN_TARGETS)
	rm -f *.js

clean_remote:
	rm -rf $(KL_JS_DIR)
