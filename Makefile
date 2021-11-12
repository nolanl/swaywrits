all: sdist

sdist:
	python3 -m build --sdist

clean:
	rm -rf dist swaywrits.egg-info

.PHONY: all sdist clean
