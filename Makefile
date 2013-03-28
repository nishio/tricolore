arena:
	-rm -rf arena
	mkdir arena
	cd arena; \
		git clone https://github.com/shuyo/misc.git shuyo; \
		cp shuyo/tricolour/tricolore.py .; \
		git clone git@github.com:nishio/tricolore.git nishio;
