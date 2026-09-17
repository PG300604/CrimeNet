"""
Collection to manage all of roles
"""
from falcon import Request, Response, before, HTTP_200, HTTP_201
from ..hooks.secure_resource import Secure
from ..auth_graph import auth_dataset
from ..auth_models import Role
from ..helpers.validate_schema import validate_schema
from ..schemas.roles_collection_schemas import create_schema, list_roles_schema
from ..helpers.log_helpers import log_event


@before(Secure("Admin"))
class RolesCollectionResource(object):
    """
    summary: Roles Collection Resource
    description: Allows administrator to add new role or list all roles
    """

    @validate_schema(output_schema=list_roles_schema)
    def on_get_v1_0(self, req: Request, resp: Response):
        """
        summary: List Roles
        externalDocs:
            description: Example of listing roles
            url: /docs/api_examples.html#list_roles
        responses:
            200:
                description: Role list
                content:
                    application/json:
                        schema: RoleListSchema
                        examples: RoleCollectionGetListExample
                    application/msgpack:
                        schema: RoleListSchema
                        examples: RoleCollectionGetListExample
        security:
            - jwt:
                - Admin
        errors:
            - name: AuthRecordNotFoundError
              message: No Roles found!
              target: Role
        examples:
            - ex_name: RoleCollectionGetListExample
              roles:
                - name: User
                  rank: 0
                - name: Admin
                  rank: 1
        """
        roles = [
            {"name": r.get_name(), "rank": r.get_rank()}
            for r in Role.get_all(auth_dataset)
        ]
        resp.media = {"roles": roles}
        resp.status = HTTP_200
        log_event(req.context.request_id, "Roles listed")

    @validate_schema(create_schema)
    def on_post_v1_0(self, req: Request, resp: Response):
        """
        summary: Create Role
        externalDocs:
            description: Example of creating a role
            url: /docs/api_examples.html#create_role
        requestBody:
            content:
                application/json:
                    schema: RoleRequestSchema
                    examples: RoleCollectionPostRequestExample
                application/msgpack:
                    schema: RoleRequestSchema
                    examples: RoleCollectionPostRequestExample
        responses:
            201:
                description: Role successfuly created
                headers:
                    Location:
                        description: Relative path to the created role
                        schema:
                            type: string
        security:
            - jwt:
                - Admin
        errors:
            - name: AlreadyExistsError
              message: Role already exists
              target: role name
        examples:
            - ex_name: RoleCollectionPostRequestExample
              name: CIA
              rank: 2
        """
        role = Role(auth_dataset).add_role(req.media["name"], req.media["rank"])
        resp.status = HTTP_201
        resp.set_header("Location", "/v1.0/roles/" + role.get_name())
        log_event(req.context.request_id, "New role added", role=req.media["name"])
