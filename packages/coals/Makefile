
all:
	@echo Targets:
	@echo clean - clean
	@echo install - local install
	@echo dist - make debian package

clean:
	rm -f *~
	rm -rf build
	rm -rf dist
	rm -rf deb_dist
	rm -f MANIFEST
	rm -f *deb
	python3 setup.py clean

install:
	make clean
	sudo python3 setup.py install

dist:
	make clean
	python3 setup.py sdist
	(cd dist ; py2dsc-deb --with-python3=True --with-python2=False *.tar.gz )
	mv dist/deb_dist/*deb .
	echo "Now install", *deb