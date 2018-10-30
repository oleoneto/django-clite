from rest_framework_httpsignature.authentication import SignatureAuthentication


class APISignatureAuthentication(SignatureAuthentication):
    """
        The HTTP header used to pass the consumer key ID.
        Defaults to 'X-Api-Key'.
    """
    API_KEY_HEADER = 'X-Api-Key'

    """
        A method to fetch (user instance, user_secret_string) from the
        consumer key ID, or None in case it is not found.
    """
    def fetch_user_data(self, api_key):
        try:
            user = User.objects.get(api_key=api_key)
            return user, user.secret
        except User.DoesNotExist:
            return None
