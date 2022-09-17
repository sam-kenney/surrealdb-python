start_db:
	surreal start \
	--log debug \
	--user "root" \
	--pass "root" \
	memory

build-lib:
	@echo "Building lib..."
	python setup.py sdist bdist_wheel
	twine check dist/*

deploy:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy-live:
	twine upload dist/*
