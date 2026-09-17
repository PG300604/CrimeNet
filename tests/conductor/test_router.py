"""
Tests for VersionedRouter
"""
import pytest
from unittest.mock import patch
from conductor.src.router import VersionedRouter


class ResourceExample(object):

    def on_get_v1_0(self, req, resp):
        pass

    def on_post_v1_0(self, req, resp):
        pass

    def on_put_v1_0(self, req, resp):
        pass

    def on_patch_v1_0(self, req, resp):
        pass

    def on_delete_v1_0(self, req, resp):
        pass

    def on_head_v1_0(self, req, resp):
        pass

    def on_connect_v1_0(self, req, resp):
        pass

    def on_options_v1_0(self, req, resp):
        pass

    def on_trace_v1_0(self, req, resp):
        pass

    def on_get_v1_1(self, req, resp):
        pass

    def on_post_v1_1(self, req, resp):
        pass

    def on_put_v2_0(self, req, resp):
        pass

    def on_patch_v2_0(self, req, resp):
        pass


@patch("conductor.src.router.config")
def test_add_route_should_add_route_handlers_with_v1_0_suffix(config_mock):
    """ add_route should add routes with sufix v1_0 """
    config = {"versions": [1.0, 1.1, 2.0, 2.2]}
    methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]
    config_mock.__getitem__.side_effect = config.__getitem__
    router = VersionedRouter()
    resource = ResourceExample()
    router.add_route("/example", resource)
    found = router.find("/v1.0/example")
    assert found[0] == resource
    assert all(hasattr(resource, h.__name__) and "v1_0" in h.__name__ for k, h in found[1].items() if k in methods)


@patch("conductor.src.router.config")
def test_add_route_should_add_route_handlers_with_v1_1_suffix(config_mock):
    """ add_route should add routes with sufix v1_1 """
    config = {"versions": [1.0, 1.1, 2.0, 2.2]}
    methods = ["GET", "POST"]
    config_mock.__getitem__.side_effect = config.__getitem__
    router = VersionedRouter()
    resource = ResourceExample()
    router.add_route("/example", resource)
    found = router.find("/v1.1/example")
    assert found[0] == resource
    assert all(hasattr(resource, h.__name__) and "v1_1" in h.__name__ for k, h in found[1].items() if k in methods)


@patch("conductor.src.router.config")
def test_add_route_should_add_route_handlers_with_v2_0_suffix(config_mock):
    """ add_route should add routes with sufix v1_1 """
    config = {"versions": [1.0, 1.1, 2.0]}
    methods = ["PUT", "PATCH"]
    config_mock.__getitem__.side_effect = config.__getitem__
    router = VersionedRouter()
    resource = ResourceExample()
    router.add_route("/example", resource)
    found = router.find("/v2.0/example")
    assert found[0] == resource
    assert all(hasattr(resource, h.__name__) and "v2_0" in h.__name__ for k, h in found[1].items() if k in methods)
