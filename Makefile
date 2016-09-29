all:

include supermake/python-sandbox.mk

build-graph:
	$(SANDBOX) python docker-net-graph.py

