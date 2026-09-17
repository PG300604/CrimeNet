"""
Process multipart/form-data requests
"""
import cgi
from falcon import Request, Response


class FormComponent(object):
    """ If multipart/form-data header found, parse request body """

    def process_request(self, request: Request, response: Response):
        """
        Process multipart request and set FieldStorage in request.context.

        :param request: falcon.Request
        :param response: falcon.Response
        """
        if "multipart/form-data" not in request.content_type:
            return
        request.env.setdefault("QUERY_STRING", "")
        stream = (request.stream.stream if hasattr(request.stream, "stream") else request.stream)
        form = cgi.FieldStorage(fp=stream, environ=request.env, keep_blank_values=1)
        request.context.form = form
