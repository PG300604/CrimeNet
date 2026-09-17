"""
Analysis algorithms collection resource
"""
from falcon import Request, Response, before, HTTP_200
from ..hooks.secure_resource import Secure
from ..helpers.validate_schema import validate_schema
from ..schemas.tasks_collection_schemas import list_algorithms_schema
from analyzer import request_taker
from ..helpers.log_helpers import log_event


@before(Secure("User"))
class TasksCollectonResource(object):
    """
    summary: Tasks Collection Resource
    description: Allows listing of analysis algorithms
    """

    @validate_schema(output_schema=list_algorithms_schema)
    def on_get_v1_0(self, req: Request, resp: Response):
        """
        summary: List Avalible Algorithms
        externalDocs:
            description: Example of listing the algorithms
            url: /docs/api_examples.html#list_algorithms
        responses:
            200:
                description: List of all avalible algorithms with their parameters
                content:
                    application/json:
                        schema: ListAlgorithmsSchema
                        examples: TaskGetRequestExample
                    application/msgpack:
                        schema: ListAlgorithmsSchema
                        examples: TaskGetRequestExample
        security:
            - jwt:
                - User
        examples:
            - ex_name: TaskGetRequestExample
              tasks:
                - name: community_detection
                  methods:
                    - name: k_cliques
                      description: K-clique
                      parameter:
                        - K:
                            description: Size of smallest clique
                            options:
                                Integer:
                                    - 3
                                    - 4
                                    - 5
                                    - 6
                                    - 7
        """
        algorithm_info = request_taker.get_info()
        response = {
            "tasks": []
        }
        for a in algorithm_info:
            temp_algorithm = {
                "name": a,
                "methods": []
            }
            for m in algorithm_info[a]["methods"]:
                temp_algorithm["methods"].append({
                    "name": m,
                    "description": algorithm_info[a]["methods"][m]["name"],
                    "parameter": algorithm_info[a]["methods"][m]["parameter"]
                })
            response["tasks"].append(temp_algorithm)
        resp.media = response
        resp.status = HTTP_200
        log_event(req.context.request_id, "Avalible algorithms listed")
