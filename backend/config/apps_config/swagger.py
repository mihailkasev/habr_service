SWAGGER_SETTINGS = {
    "LOGIN_URL": "/admin/login/",
    "LOGOUT_URL": "/admin/logout/",
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
