#! /bin/bash

if [[ "$1" == "clean" ]]; then
    echo "Running make clean"
    make clean

    echo "Removing Emacs backups"
    find -name *.backups -exec rm -r {} \;

    echo "Removing compiled Python files"
    find -name *.pyc -exec rm -r {} \;
else   
    export PATH=../kaylee/bin:$PATH
    export PYTHONPATH=../:$PYTHONPATH
    make $@ LOCALBUILD=TRUE
fi
