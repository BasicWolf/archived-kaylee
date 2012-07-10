# Define the names of the projects here
PROJECTS = monte_carlo_pi hash_cracker

# Create project directories' paths
PJ_DIRS = $(addprefix projects/, $(PROJECTS) )

# Define build directory and export variables for recursive make purpose
export KL_BUILD_DIR = $(CURDIR)/_build
export PJ_RES_DIR = $(KL_BUILD_DIR)/static/js/projects

CLIENT_DIR = kaylee/contrib/client
DEMO_DIR = kaylee/contrib/client/demo

all : $(PJ_DIRS) client demo

$(PJ_DIRS): 
	$(MAKE) $(MAKECMDGOALS) -C $@

demo: client
	$(MAKE) $(MAKECMDGOALS) -C $(DEMO_DIR)

client:
	$(MAKE) $(MAKECMDGOALS) -C $(CLIENT_DIR)

clean: $(PJ_DIRS) demo client
	rm -rf $(KL_BUILD_DIR)

.PHONY: clean demo projects $(PJ_DIRS)
