from flask import render_template, redirect, request, url_for
from sqlalchemy import and_

from warch_registry.app import db, auth, bp_inventory
from warch_registry.models import RegistryModel, InventoryModel, InventoryTypeModel
from warch_registry.forms import InventoryForm, FilterForm

@bp_inventory.route('/<int:regid>')
@bp_inventory.route('/<int:regid>/page/<int:page>')
@auth.login_required
def index(regid, page=1):
    registry_object = RegistryModel.query.get(regid)
    no_years_count = RegistryModel.query.filter(
        and_(InventoryModel.regid == regid, InventoryModel.in_year == None, InventoryModel.out_year == None)).count()

    fform = FilterForm(request.values)

    filter = list()
    filter.append(InventoryModel.regid == regid)

    if request.method == 'GET' and request.args and fform.validate():
        if request.args.get('fund_num'):
            filter.append(InventoryModel.fund_num ==
                            request.args.get('fund_num'))

        if request.args.get('inventory_num'):
            filter.append(InventoryModel.inventory_num.like("%{}%".format(request.args.get('inventory_num'))))

        if request.args.get('year'):
            filter.append(InventoryModel.in_year ==
                          request.args.get('year'))
        
        if request.args.get('lowcopy'):
            filter.append(InventoryModel.copies < 3)

        if request.args.get('no_years'):
            filter.append(and_(InventoryModel.in_year == None, InventoryModel.out_year == None))

    objects_list = InventoryModel.query.filter(*filter).paginate(page, 20, error_out=False)

    return render_template('inventory/index.html', registry_object=registry_object, objects_list=objects_list, fform=fform, no_years_count=no_years_count)

@bp_inventory.route('/<int:regid>/create', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def create(regid):
    registry_object = RegistryModel.query.get(regid)
    inventory_type_list = InventoryTypeModel.query.all()

    form = InventoryForm(request.form)
    form.regid.data = regid
    form.inventory_type.choices = [("", u"-- Без типа --")] + \
        [(it.id, it.short_name) for it in inventory_type_list]

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

    inventory_type_list = InventoryTypeModel.query.all()

    form = InventoryForm(request.form, obj=inventory)
    form.inventory_type.choices = [("",u"-- Без типа --")] + \
        [(it.id, it.short_name) for it in inventory_type_list]

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
