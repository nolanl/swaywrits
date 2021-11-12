all: sdist

sdist:
	python3 -m build --sdist

wheel:
	python -m build --wheel

clean:
	@rm -rf dist build swaywrits.egg-info

check:
	@flake8 swaywrits

.PHONY: all sdist clean
