PROJECT_NAME = monte_carlo_pi
LIB = $(PROJECT_NAME).js
LIBDIR = res/js

TARGETS = $(LIBDIR)/$(LIB)
CLEAN_TARGETS = 

ifeq ($(origin PJ_JSLIB_DIR), environment)
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif

all: $(TARGETS)

$(LIBDIR)/$(LIB): $(LIBDIR)/$(PROJECT_NAME).coffee
	coffee -c $(LIBDIR)/$(PROJECT_NAME).coffee

remote:
	mkdir -p  $(PJ_JSLIB_DIR)/$(PROJECT_NAME)
	cp $(LIBDIR)/$(PROJECT_NAME).js $(PJ_JSLIB_DIR)/$(PROJECT_NAME)

clean: $(CLEAN_TARGETS)
	rm -f $(LIBDIR)/$(PROJECT_NAME).js 

clean_remote:
	rm -f $(PJ_JSLIB_DIR)/$(PROJECT_NAME)/$(PROJECT_NAME).js
