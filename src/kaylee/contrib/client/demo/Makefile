TARGETS = src/klconsole.js src/kldemo.js

ifeq ($(origin KL_BUILD_DIR), environment)
KL_JS_DIR = $(KL_BUILD_DIR)/static/js/kaylee
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif

all: $(TARGETS)

src/klconsole.js: src/klconsole.coffee
	coffee -j src/klconsole.js -c src/klconsole.coffee

src/kldemo.js: src/kldemo.coffee
	coffee -j src/kldemo.js -c src/kldemo.coffee

remote:
	mkdir -p  $(KL_JS_DIR)
	cp src/*.js $(KL_JS_DIR)
	cp -r static $(KL_BUILD_DIR)
	cp -r templates $(KL_BUILD_DIR)

clean: $(CLEAN_TARGETS)
	rm -f src/*.js

clean_remote:
	rm -rf $(KL_JS_DIR)
	rm -rf $(KL_BUILD_DIR)/static
	rm -rf $(KL_BUILD_DIR)/templates
