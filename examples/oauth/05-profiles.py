from mollie.api.error import Error


def main(client):
    try:

        # https://docs.mollie.com/reference/v2/profiles-api/create-profile

        body = "<h1>Create profile</h1>"
        data = {
            "name": "My website name",
            "website": "https://www.mywebsite.com",
            "email": "info@mywebsite.com",
            "phone": "+31208202070",
            "categoryCode": "5399",
            "mode": "live",
        }
        response = client.profiles.create(data)
        body += str(response)

        profile_id = response.id

        # https://docs.mollie.com/reference/v2/profiles-api/get-profile

        body += "<h1>Get profile</h1>"
        response = client.profiles.get(profile_id)
        body += str(response)

        # https://docs.mollie.com/reference/v2/profiles-api/update-profile

        body += "<h1>Update profile</h1>"
        data.update(
            {
                "name": "My website name updated",
                "email": "updated-profile@example.org",
            }
        )
        response = client.profiles.update(profile_id, data)
        body += str(response)

        # https://docs.mollie.com/reference/v2/profiles-api/enable-method

        body += "<h1>Enable payment method</h1>"
        profile = client.profiles.get(profile_id)
        response = client.profile_methods.on(profile, "bancontact").create()
        body += str(response)

        # https://docs.mollie.com/reference/v2/profiles-api/disable-method

        body += "<h1>Disable payment method</h1>"
        response = client.profile_methods.on(profile, "bancontact").delete()
        body += str(response)

        # https://docs.mollie.com/reference/v2/profiles-api/list-profiles

        body += "<h1>List profiles</h1>"
        response = client.profiles.list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/profiles-api/delete-profile

        body += "<h1>Delete profile</h1>"
        response = client.profiles.delete(profile_id)
        body += str(response)

        return body

    except Error as err:
        return f"API call failed: {err}"
