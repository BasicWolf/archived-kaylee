# Define the names of the projects here
PROJECTS = hash_cracker human_ocr

# Create project directories' paths
PJ_DIRS = $(addprefix projects/, $(PROJECTS) )

# Define build directory and export variables for recursive make purpose
export KL_BUILD_DIR = $(CURDIR)/build
export PJ_RES_DIR = $(KL_BUILD_DIR)/static/js/projects
KL_CLIENT_DIR = $(KL_BUILD_DIR)/static/js/kaylee

ifdef LOCALBUILD
	CLIENT_FLAGS = -b
else
	CLIENT_FLAGS = 
endif

all: demo

demo: static client demo_js $(PJ_DIRS) 

static:
	mkdir -p $(KL_BUILD_DIR)
	mkdir -p $(KL_CLIENT_DIR)
	cp -r static $(KL_BUILD_DIR)
	cp -r templates $(KL_BUILD_DIR)

client:
	kaylee-copy-client.py $(CLIENT_FLAGS) $(KL_CLIENT_DIR)

$(PJ_DIRS):
	$(MAKE) $(MAKECMDGOALS) -C $@

demo_js: src/klconsole.js src/kldemo.js

src/klconsole.js: src/klconsole.coffee
	coffee -j src/klconsole.js -c src/klconsole.coffee
	cp src/klconsole.js	 $(KL_CLIENT_DIR)

src/kldemo.js: src/kldemo.coffee
	coffee -j src/kldemo.js -c src/kldemo.coffee
	cp src/kldemo.js $(KL_CLIENT_DIR)

clean : $(PJ_DIRS)
	rm -r $(KL_BUILD_DIR)
	rm -f src/*.js

.PHONY: clean demo projects $(PJ_DIRS) static
