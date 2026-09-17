"""
Route to manage user's file folder
"""
from os import listdir
from falcon import Request, Response, before, HTTP_200, HTTP_201
from werkzeug.utils import secure_filename
from ..hooks.secure_resource import Secure
from ..helpers.file_helpers import save_file
from ..helpers.validate_schema import validate_schema
from ..exceptions import FormValidationError, ValidationError
from ..schemas.files_collection_schemas import files_list
from ..helpers.log_helpers import log_event


@before(Secure("User"))
class FilesCollectionResource(object):
    """
    summary: Files Collection Resource
    description: Allows listing user files and uploading new files
    """

    @validate_schema(output_schema=files_list)
    def on_get_v1_0(self, req: Request, resp: Response):
        """
        summary: List all files
        externalDocs:
            description: Example of listing files
            url: /docs/api_examples.html#file_list
        responses:
            200:
                description: List of files in user folder
                content:
                    application/json:
                        schema: FileList
                        examples: FileCollectionGetListExample
                    application/msgpack:
                        schema: FileList
                        examples: FileCollectionGetListExample
        security:
            - jwt:
                - User
        examples:
            - ex_name: FileCollectionGetListExample
              files:
                - tempfile1.json
        """
        resp.media = {"files": listdir(req.context.user.get_folder_path())}
        resp.status = HTTP_200
        log_event(
            req.context.request_id,
            "Files listed in user folder")

    def on_post_v1_0(self, req: Request, resp: Response):
        """
        summary: Upload new file
        externalDocs:
            description: Example of uploading file
            url: /docs/api_examples.html#upload_file_body
        requestBody:
            description: File form contents
            content:
                multipart/form-data:
                    schema:
                        type: object
                        properties:
                            file:
                                type: string
                                format: binary
                    encoding:
                        file:
                            contentType: application/json
                    examples: FileCollectionPostUploadExample
        responses:
            201:
                description: File was successfuly uploaded
                headers:
                    Location:
                        description: Relative path to uploaded file
                        schema:
                            type: string
        security:
            - jwt:
                - User
        errors:
            - name: ValidationError
              message: File form not found
              target: request body
            - name: FormValidationError
              message: Field 'file' not found
              target: form
            - name: FileExistsError
              message: File already exists!
              target: filename
        examples:
            - ex_name: FileCollectionPostUploadExample
              file: {}
        """
        if not hasattr(req.context, "form"):
            raise ValidationError("File form not found", "request body")
        file = None
        try:
            file = req.context.form["file"]
        except KeyError:
            raise FormValidationError("Field 'file' not found", "form")
        filename = secure_filename(file.filename)
        filepath = req.context.user.get_folder_path() / filename
        save_file(file.file, filepath)
        resp.set_header("Location", "/v1.0/files/" + filename)
        resp.status = HTTP_201
        log_event(
            req.context.request_id,
            "File uploaded",
            file=filename)
