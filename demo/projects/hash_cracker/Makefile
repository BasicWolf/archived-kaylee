PROJECT_NAME = hash_cracker
LIB = $(PROJECT_NAME).js
LIBDIR = res/js


TARGETS = $(LIBDIR)/$(LIB)
CLEAN_TARGETS = 

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
	rm -rf $(PJ_JS_DIR)/$(PROJECT_NAME)
