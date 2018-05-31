all:
	@echo "targets:"
	@echo
	@echo "implicit - copy the resources based on derived constraints into resources"
	@echo "explicit - copy the resources with explicit constraints into resources"
	@echo
	@echo "demo - demo the resources - requires 'coals' to be installed"
	@echo
	
implicit:
	rm -rf resources/*
	cp resources_implicit/* resources/

explicit:
	rm -rf resources/*
	cp resources_explicit/* resources/

demo:
	coals
