MODULE := dbspan

demo:
	@python -m $(MODULE) dbspan

test:
	@pytest
