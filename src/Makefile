# Define the names of the projects here
PROJECTS = monte_carlo_pi hash_cracker

# Create project directories' paths
PJ_DIRS = $(addprefix projects/, $(PROJECTS) )

# Define build directory and export variables for recursive make purpose
export KL_BUILD_DIR = $(CURDIR)/build
export PJ_RES_DIR = $(KL_BUILD_DIR)/static/js/projects

CLIENT_DIR = kaylee/client
DEMO_DIR = kaylee/contrib/demo

all : client projects demo

client:
	$(MAKE) $(MAKECMDGOALS) -C $(CLIENT_DIR)

projects: $(PJ_DIRS)

$(PJ_DIRS): 
	$(MAKE) $(MAKECMDGOALS) -C $@

demo: 
	@echo 'Building Kaylee demo'
	$(MAKE) $(MAKECMDGOALS) -C $(DEMO_DIR)

clean : clean $(PJ_DIRS) demo client
	rm -rf $(KL_BUILD_DIR)

.PHONY: clean demo projects $(PJ_DIRS)
