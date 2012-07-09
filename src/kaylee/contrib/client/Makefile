TARGETS = kaylee.js kldemo.js klconsole.js klworker.js

ifeq ($(origin KL_JSLIB_DIR), environment)
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif


all: $(TARGETS)

kaylee.js: kaylee.coffee
	coffee -j kaylee.js -c kaylee.coffee 

klworker.js: klworker.coffee
	coffee --bare -c klworker.coffee

kldemo.js: kldemo.coffee
	coffee -c kldemo.coffee 

klconsole.js: klconsole.coffee
	coffee -c klconsole.coffee 

remote:
	mkdir -p  $(KL_JSLIB_DIR)
	cp *.js $(KL_JSLIB_DIR)


clean: $(CLEAN_TARGETS)
	rm -f *.js

clean_remote:
	rm -rf $(KL_JSLIB_DIR)
