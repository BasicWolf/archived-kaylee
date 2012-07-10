# Define the names of the projects here
PROJECTS = monte_carlo_pi hash_cracker

# Create project directories' paths
PJ_DIRS = $(addprefix projects/, $(PROJECTS) )

# Define build directory and export variables for recursive make purpose
export KL_BUILD_DIR = $(CURDIR)/_build
export PJ_RES_DIR = $(KL_BUILD_DIR)/static/js/projects

DEMO_DIR = kaylee/contrib/client/demo

all : $(PJ_DIRS)

$(PJ_DIRS): 
	$(MAKE) $(MAKECMDGOALS) -C $@

demo:
	$(MAKE) $(MAKECMDGOALS) -C $(DEMO_DIR)/src

clean: subdirs
	rm -rf $(KL_BUILD_DIR)

.PHONY: $(SUBDIRS) clean subdirs
