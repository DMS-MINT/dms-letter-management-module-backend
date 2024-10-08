from config.env import env

CSRF_COOKIE_DOMAIN = f".{env.str("CSRF_COOKIE_DOMAIN", default="localhost")}"

SESSION_COOKIE_DOMAIN = f".{env.str("SESSION_COOKIE_DOMAIN", default="localhost")}"

CSRF_TRUSTED_ORIGINS = [
    f"http://{env.str("APP_DOMAIN", default="localhost")}:{env.str("APP_PORT", default="8000")}",
    f"http://*.{env.str("APP_DOMAIN", default="localhost")}:{env.str("APP_PORT", default="8000")}",
]
