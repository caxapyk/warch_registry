from flask import render_template, redirect, request, url_for

from warch_registry.app import db, auth, bp_inventory_type
from warch_registry.models import RegistryModel, InventoryTypeModel
from warch_registry.forms import InventoryTypeForm


@bp_inventory_type.route('/')
@auth.login_required
def index():
    objects_list = InventoryTypeModel.query.all()
    return render_template('inventory-type/index.html', objects_list=objects_list)


@bp_inventory_type.route('/create', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def create():
    form = InventoryTypeForm(request.form)

    if request.method == 'POST' and form.validate():
        inventory = InventoryTypeModel()
        form.populate_obj(inventory)

        db.session.add(inventory)
        db.session.commit()

        return redirect(url_for("inventory_type.index"))

    return render_template('inventory-type/create.html', form=form)


@bp_inventory_type.route('/update/<int:id>', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def update(id):
    inventory = InventoryTypeModel.query.get(id)
    form = InventoryTypeForm(request.form, obj=inventory)

    if request.method == 'POST' and form.validate():
        form.populate_obj(inventory)

        db.session.add(inventory)
        db.session.commit()

        return redirect(url_for("inventory_type.index"))

    return render_template('inventory-type/update.html', form=form)

@bp_inventory_type.route('/remove', methods=['POST'])
@bp_inventory_type.route('/remove/<int:id>', methods=['GET'])
@auth.login_required(role='manager')
def remove(id=None):
    if request.method == 'GET':
        InventoryTypeModel.query.filter_by(id=id).delete()
        db.session.commit()
    elif request.method == 'POST':
        selected = request.form.getlist('selected')
        if len(selected) > 0:
            for pk in selected:
                InventoryTypeModel.query.filter_by(id=pk).delete()
                db.session.commit()

    return redirect(url_for("inventory_type.index"))
