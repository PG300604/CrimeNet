"""
Define all routes
"""
from .. import api
from .resources.login import LoginResource
from .resources.users_collection import UsersCollectionResource
from .resources.roles_collection import RolesCollectionResource
from .resources.users import UsersResource
from .resources.files_collection import FilesCollectionResource
from .resources.files import FilesResource
from .resources.roles import RolesResource
from .resources.datasets_collection import DatasetsCollectionResource
from .resources.datasets import DatasetsResource
from .resources.tasks_collection import TasksCollectonResource
from .resources.tasks import TaskResource
from .resources.network_construction_tasks import NetworkConstructionTasksResource
from .resources.operations import OperationsResource

login_resource = LoginResource()
roles_collection_resource = RolesCollectionResource()
users_collection_resource = UsersCollectionResource()
users_resource = UsersResource()
files_collection_resource = FilesCollectionResource()
files_resource = FilesResource()
roles_resource = RolesResource()
datasets_collection_resource = DatasetsCollectionResource()
dataset_resource = DatasetsResource()
tasks_collection_resource = TasksCollectonResource()
task_resource = TaskResource()
operations_resource = OperationsResource()
network_construction_task = NetworkConstructionTasksResource()

api.add_route("/login", login_resource)
api.add_route("/users", users_collection_resource)
api.add_route("/users/{username}", users_resource)
api.add_route("/roles", roles_collection_resource)
api.add_route("/roles/{role_name}", roles_resource)
api.add_route("/files", files_collection_resource)
api.add_route("/files/{filename}", files_resource)
api.add_route("/datasets", datasets_collection_resource)
api.add_route("/datasets/{dataset_name}", dataset_resource)
api.add_route("/tasks", tasks_collection_resource)
api.add_route("/tasks/network_construction/{task_name}", network_construction_task)
api.add_route("/tasks/{task_name}", task_resource)
api.add_route("/operations/{operation_id}", operations_resource)
