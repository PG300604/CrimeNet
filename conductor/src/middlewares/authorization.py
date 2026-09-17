"""
Authorize user if JWT is present
"""
from falcon import Request, Response
from ..auth_models import User
from ..auth_graph import auth_dataset
from ..helpers.auth_helpers import read_token


class AuthorizationComponent(object):
    """ Process authorization """

    auth_header_prefix = "Bearer "

    def process_request(self, request: Request, response: Response):
        """
        Check Authorization header and authorize user if token is valid

        :param request: falcon.Request
        :param response: falcon.Response
        """
        if request.auth:
            token = request.auth.replace(self.auth_header_prefix, "")
            claims = read_token(token, ["iat", "exp", "username"])
            user = User(auth_dataset).identify(claims["username"])
            request.context.user = user
        else:
            request.context.user = None
