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

test: develop
	pipenv run pytest

clean:
	pipenv --rm
