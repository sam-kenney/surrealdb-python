start_db:
	surreal start \
	--log debug \
	--user $(SURREALDB_USERNAME) \
	--pass $(SURREALDB_PASSWORD) \
	file://$(PWD)/.db_store

build-lib:
	@echo "Building lib..."
	python setup.py sdist bdist_wheel
	twine check dist/*

deploy:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy-live:
	twine upload dist/*
