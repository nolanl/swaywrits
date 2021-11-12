all: sdist

sdist:
	python3 -m build --sdist

clean:
	@rm -rf dist swaywrits.egg-info

check:
	@flake8 swaywrits

.PHONY: all sdist clean
