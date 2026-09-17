"""
Add roule authorization to the recource
"""
from falcon import Request, Response, HTTP_401, HTTP_403
from ..auth_graph import auth_dataset
from ..auth_models import Role
from ..exceptions import AuthenticationError, ErrorDetail


class NotAuthorizedError(AuthenticationError):
    """ Error authorizing user """
    code = "NotAuthorizedError"
    response_code = HTTP_401


class NotEnoughPrivileges(AuthenticationError):
    """ User does not have enough privileges to access the recource """
    code = "NotEnoughPrivileges"
    response_code = HTTP_403


class Secure(object):
    """ Authoroze user and check proper role if given """

    def __init__(self, role=None):
        self.role_name = role

    def __call__(self, request: Request, response: Response, resource, params):
        """
        Check user auhorization in request

        :param request: falcon.Request
        :param response: falcon.Response
        :param resource: Resource class
        :param params: url params
        """
        if not request.context.user:
            raise NotAuthorizedError("Authorization required to access the recourse", "Authentication header")
        if not self.role_name:
            return
        user_role = request.context.user.get_role()
        role = Role(auth_dataset).get_role_vertex(self.role_name)
        if user_role.get_rank() < role.get_rank():
            description = ErrorDetail("RequiredRole", "role", role.get_name())
            raise NotEnoughPrivileges("Not enough privileges to access the recourse", "User role", [description])
