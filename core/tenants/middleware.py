import contextvars

from .utils import tenant_db_from_request

current_db_var = contextvars.ContextVar("current_db")


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db = tenant_db_from_request(request)
        mock = "tenant"
        # After you implemented the database generator replace the 'mock' with 'db'
        set_db_for_router(mock)

        return self.get_response(request)


def get_current_db_name():
    return current_db_var.get(None)


def set_db_for_router(db):
    current_db_var.set(db)
