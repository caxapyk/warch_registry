from flask import current_app
from warch_registry.models import RegistryModel


@current_app.context_processor
def registries_list():
    objects_list = RegistryModel.query.order_by(RegistryModel.name).all()
    return dict(registries_list=objects_list)
