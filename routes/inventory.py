from flask import render_template, redirect, request, url_for

from warch_registry import db, auth, bp_inventory
from warch_registry.models import RegistryModel, InventoryModel
from warch_registry.forms import InventoryForm


@bp_inventory.route('/<int:regid>')
@auth.login_required
def index(regid):
    registry_object = RegistryModel.query.get(regid)
    objects_list = InventoryModel.query.filter_by(regid=regid).all()

    return render_template('inventory/index.html', registry_object=registry_object, objects_list=objects_list)

@bp_inventory.route('/<int:regid>/create', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def create(regid):
    registry_object = RegistryModel.query.get(regid)

    form = InventoryForm(request.form)

    if request.method == 'POST' and form.validate():
        inventory = InventoryModel()
        form.populate_obj(inventory)

        db.session.add(inventory)
        db.session.commit()

        return redirect(url_for("inventory.index", regid=regid))

    return render_template('inventory/create.html', registry_object=registry_object, form=form)

@bp_inventory.route('/<int:regid>/inventory/update/<int:id>', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def update(regid, id):
    registry_object = RegistryModel.query.get(regid)
    inventory = InventoryModel.query.get(id)

    form = InventoryForm(request.form, obj=inventory)

    if request.method == 'POST' and form.validate():
        form.populate_obj(inventory)

        db.session.add(inventory)
        db.session.commit()

        return redirect(url_for("inventory.index", regid=regid))

    return render_template('inventory/update.html', registry_object=registry_object, form=form)

@bp_inventory.route('/<int:regid>/inventory/remove', methods=['POST'])
@bp_inventory.route('/<int:regid>/inventory/<int:id>', methods=['GET'])
@auth.login_required(role='manager')
def remove(regid, id=None):
    if request.method == 'GET':
        InventoryModel.query.filter_by(id=id).delete()
        db.session.commit()
    elif request.method == 'POST':
        selected = request.form.getlist('selected')
        if len(selected) > 0:
            for pk in selected:
                InventoryModel.query.filter_by(id=pk).delete()
                db.session.commit()

    return redirect(url_for("inventory.index", regid=regid))