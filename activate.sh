if [ -s ./.venv ] ; then 
	. ./.venv/bin/activate ;
else
	echo 'No venv defined, creating...' ;
	python3 -m venv .venv ;
	. ./.venv/bin/activate ;
fi;

