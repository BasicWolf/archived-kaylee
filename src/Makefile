PROJECTS = monte_carlo_pi hash_cracker

KL_SRC_DIR = kayleejs/src
KL_JSLIB_DIR = kayleejs/static/js/kaylee
export PJ_JSLIB_DIR = $(CURDIR)/kayleejs/static/js/projects
PJ_DIRS = $(addprefix projects/, $(PROJECTS) )


SUBDIRS = $(KL_SRC_DIR) $(PJ_DIRS)

all : subdirs $(KL_JSLIB_DIR)

subdirs: $(SUBDIRS)

$(PJ_DIRS):
	$(MAKE) $(MAKECMDGOALS) -C $@

$(KL_JSLIB_DIR): 
	cp $(KL_SRC_DIR)/*.js $(KL_JSLIB_DIR)

$(KL_SRC_DIR):
	$(MAKE) $(MAKECMDGOALS) -C $(KL_SRC_DIR)

clean: subdirs

.PHONY: $(SUBDIRS) $(KL_JSLIB_DIR) clean subdirs
