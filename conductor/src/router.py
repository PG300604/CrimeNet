"""
Custom routing logic, including verioning
"""
from re import compile
from decimal import Decimal
from falcon.routing import CompiledRouter
from .config import config


class VersionedRouter(CompiledRouter):
    """ Router implementation, that takes into account versioning """

    def __init__(self, *params, **kwargs):
        self._route_mappings = []
        super().__init__(*params, **kwargs)

    matcher = compile(r"^on_((get)|(post)|(put)|(patch)|(delete)|(head)|(connect)|(options)|(trace))_v(?P<major>\d+)_(?P<minor>\d+)$")

    def add_route(self, uri_template, resource, **kwargs):
        """ Add route with version number, using the suffix after the method """
        router = super()
        resource_versions = set()
        config_versions = sorted(config["versions"])
        resource_methods = [m for m in dir(resource) if callable(getattr(resource, m))]
        for m in resource_methods:
            match = self.matcher.match(m)
            if not match:
                continue
            version_major = int(match.group("major"))
            version_minor = int(match.group("minor"))
            resource_versions.add(Decimal(f"{version_major}.{version_minor}"))
        resource_versions = sorted(resource_versions)
        for v in config_versions:
            for rv in resource_versions:
                if rv > v:
                    break
                mv = rv
            mv = mv.as_tuple()
            major_suffix = ''.join(str(n) for n in mv.digits[:mv.exponent])
            minor_suffix = ''.join(str(n) for n in mv.digits[mv.exponent:])
            suffix = f"v{major_suffix}_{minor_suffix}"
            path = f"/v{v}{uri_template}"
            self._route_mappings.append({
                "path": path,
                "resource": resource,
                "suffix": suffix
            })
            router.add_route(path, resource, suffix=suffix)
