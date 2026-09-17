"""
Middleware for logging requests
"""
from uuid import uuid4
from falcon import Request, Response
from ..helpers.log_helpers import log_event


class LoggingComponent(object):
    """ Log all incoming and outgoing requests """

    def process_request(self, req: Request, resp: Response):
        """ Log incoming request and give it an ID """
        req.context.request_id = str(uuid4())
        log_event(
            req.context.request_id,
            "Request recieved",
            method=req.method,
            url=req.url,
            content_type=req.content_type,
            accept=req.accept,
            content_length=req.content_length
        )

    def process_response(self, req: Request, resp: Response, resource, req_succeeded):
        """ Log outgoing requests """
        log_event(
            req.context.request_id,
            "Response dispatched",
            status=resp.status,
            is_successful=req_succeeded
        )
