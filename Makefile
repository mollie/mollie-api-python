Mollie/Api/cacert.pem: certdata.txt
	mv ca-bundle.crt Mollie/Api/cacert.pem
	rm certdata.txt

mk-ca-bundle.pl:
	curl -q https://raw.githubusercontent.com/curl/curl/master/lib/mk-ca-bundle.pl --output mk-ca-bundle.pl
	chmod +x mk-ca-bundle.pl

certdata.txt: mk-ca-bundle.pl
	./mk-ca-bundle.pl

.PHONY: develop
develop:
	pipenv sync --dev

test: develop
	pipenv run pytest

clean:
	pipenv --rm