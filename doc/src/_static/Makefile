PROJECT_NAME = monte_carlo_pi
LIB = $(PROJECT_NAME).js
# location of coffee file and to-be-compiled js files.
LIBDIR = js

# js target
TARGETS = $(LIBDIR)/$(LIB)
CLEAN_TARGETS =

# if make has been called recursively, add remote targets
ifeq ($(origin PJ_RES_DIR), environment)
PJ_JS_DIR = $(PJ_RES_DIR)/$(PROJECT_NAME)/js
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif

all: $(TARGETS)

$(LIBDIR)/$(LIB): $(LIBDIR)/$(PROJECT_NAME).coffee
	coffee --bare -c $(LIBDIR)/$(PROJECT_NAME).coffee

remote:
	mkdir -p  $(PJ_JS_DIR)
	cp $(LIBDIR)/*.js $(PJ_JS_DIR)

clean: $(CLEAN_TARGETS)
	rm -f $(LIBDIR)/$(PROJECT_NAME).js

clean_remote:
	rm -rf $(PJ_RES_DIR)/$(PROJECT_NAME)
