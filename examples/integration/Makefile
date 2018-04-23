all:
	@echo "targets:"
	@echo
	@echo "implicit - copy the resources based on derived constraints into resources"
	@echo "explict - copy the resources with explicit constraints into resources"
	@echo
	@echo "demo - demo the resources - requires als_core to be installed"
	@echo
	
implict:
	rm -rf resources/*
	cp resources_implicit/* resources/

explict:
	rm -rf resources/*
	cp resources_explicit/* resources/

demo:
	als.py
