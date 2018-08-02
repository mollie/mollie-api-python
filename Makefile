mollie/api/cacert.pem: certdata.txt
	mv ca-bundle.crt $@
	rm certdata.txt

mk-ca-bundle.pl:
	curl -q https://raw.githubusercontent.com/curl/curl/master/lib/mk-ca-bundle.pl --output $@
	chmod +x $@

certdata.txt: mk-ca-bundle.pl
	./mk-ca-bundle.pl

.PHONY: develop
develop:
	pipenv sync --dev

.PHONY: test
test: develop
	pipenv run pytest
	pipenv run pyflakes .
	pipenv run pycodestyle
	pipenv run isort --recursive --check-only
	pipenv check

.PHONY: clean
clean:
	pipenv --rm
