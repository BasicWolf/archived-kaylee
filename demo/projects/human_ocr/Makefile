PROJECT_NAME = human_ocr
LIB = $(PROJECT_NAME).js
LIBDIR = res/js
CSSDIR = res/css

TARGETS = $(LIBDIR)/$(LIB)
CLEAN_TARGETS = 

ifeq ($(origin PJ_RES_DIR), environment)
PJ_JS_DIR = $(PJ_RES_DIR)/$(PROJECT_NAME)/js
PJ_CSS_DIR = $(PJ_RES_DIR)/$(PROJECT_NAME)/css
TARGETS += remote
CLEAN_TARGETS += clean_remote
endif

all: $(TARGETS)

$(LIBDIR)/$(LIB): $(LIBDIR)/$(PROJECT_NAME).coffee
	coffee --bare -c $(LIBDIR)/$(PROJECT_NAME).coffee

remote:
	mkdir -p  $(PJ_JS_DIR)/$(PROJECT_NAME)
	cp $(LIBDIR)/*.js $(PJ_JS_DIR)
	cp $(CSSDIR)/*.css $(PJ_CSS_DIR)

clean: $(CLEAN_TARGETS)
	rm -f $(LIBDIR)/$(PROJECT_NAME).js 

clean_remote:
	rm -rf $(PJ_JS_DIR)/$(PROJECT_NAME)
