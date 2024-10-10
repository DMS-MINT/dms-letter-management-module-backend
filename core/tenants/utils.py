from core.tenants.models import Domain


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(":")[0].lower()


def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)


def get_tenants_map():
    domains = Domain.objects.filter(is_primary=True).select_related("tenant")
    return {domain.domain: domain.tenant.database_name for domain in domains}
