# coding=utf-8

from __future__ import print_function

from mollie.api.error import Error


def main(client):
    try:

        # https://docs.mollie.com/reference/v2/onboarding-api/get-onboarding-status

        body = '<h1>Get onboarding status</h1>'
        onboarding = client.onboarding.get('me')

        print(onboarding)

        body += 'Status: <b>{onboarding.status}</b>'.format(onboarding=onboarding)

        # https://docs.mollie.com/reference/v2/onboarding-api/submit-onboarding-data

        body += '<h1>Submit onboarding data</h1>'
        data = {
            'profile': {
                'categoryCode': '6012'
            }
        }
        onboarding = client.onboarding.create(resource_id='me', data=data)
        print(onboarding)
        body += str(onboarding)

        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)
