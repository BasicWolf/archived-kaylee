KC = kayleejs/src
KJ = kayleejs/static/js/kaylee

KJSOURCES = $(KC)/*.coffee
JSOBJECTS = $(KJSOURCES:.coffee=.js)

$(KJ): $(JSOBJECTS)
	mkdir -p $(KJ)
	cp $(KC)/*.js $(KJ)

$(JSOBJECTS): $(KJSOURCES)
	coffee -c $? 

clean:
	rm -f $(KJ)/*.js
	rm -f $(KC)/*.js


# Cheatsheet
# http://www.cprogramming.com/tutorial/makefiles_continued.html
# The $? macro stores the list of dependents more recent than the target
