"""
Resource to authenticate user
"""
from falcon import Request, Response, HTTP_200
from ..helpers.validate_schema import validate_schema
from ..helpers.auth_helpers import create_token
from ..schemas.login_schemas import login_request, login_response
from ..auth_models import User
from ..auth_graph import auth_dataset
from ..helpers.log_helpers import log_event


class LoginResource(object):
    """
    summary: Login Resource
    description: Provides login into account
    """

    @validate_schema(login_request, login_response)
    def on_post_v1_0(self, req: Request, resp: Response):
        """
        summary: Log In
        externalDocs:
            description: Example of logging in
            url: /docs/api_examples.html#login
        requestBody:
            description: User's credentials
            content:
                application/json:
                    schema: LoginRequest
                    examples: LoginRequestExample
                application/msgpack:
                    schema: LoginRequest
                    examples: LoginRequestExample
        responses:
            200:
                description: After successfull login access token will be provided
                content:
                    application/json:
                        schema: LoginResponse
                    application/msgpack:
                        schema: LoginResponse
        errors:
            - name: AuthRecordNotFoundError
              message: User by username ... not found!
              target: username
            - name: WrongPasswordError
              message: Wrong password!
              target: User
        examples:
            - ex_name: LoginRequestExample
              username: admin
              password: Pass1234
        """
        user = User(auth_dataset).authenticate(req.media["username"], req.media["password"])
        access_token = create_token({"username": user.get_username()})
        resp.media = {"accessToken": access_token}
        resp.status = HTTP_200
        log_event(
            req.context.request_id,
            "Successfull login",
            username=req.media["username"])
