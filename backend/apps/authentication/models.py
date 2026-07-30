"""
Models for the authentication app.

Authentication itself is stateless (JWT). The User model lives in
apps.users — this module intentionally has no models of its own.
Token blacklisting tables are provided by rest_framework_simplejwt's
'token_blacklist' app (add to INSTALLED_APPS + migrate).
"""
