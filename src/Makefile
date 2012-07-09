# Define the names of the projects here
PROJECTS = monte_carlo_pi hash_cracker

# Create project directories' paths
PJ_DIRS = $(addprefix projects/, $(PROJECTS) )

# Define build directory and export variables for recursive make purpose
export KL_BUILD_DIR = $(CURDIR)/_build
export PJ_RES_DIR = $(KL_BUILD_DIR)/static/js/projects

SUBDIRS = $(PJ_DIRS)

all : subdirs

subdirs: $(SUBDIRS)

$(SUBDIRS): 
	$(MAKE) $(MAKECMDGOALS) -C $@

clean: subdirs
	rm -rf $(KL_BUILD_DIR)

.PHONY: $(SUBDIRS) clean subdirs
