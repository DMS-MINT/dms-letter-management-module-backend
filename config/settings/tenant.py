from config.env import env

TENANT_MODEL = "organizations.Organization"

TENANT_DOMAIN_MODEL = "organizations.Domain"

TENANT_USERS_DOMAIN = env.str("APP_DOMAIN", default="localhost")
