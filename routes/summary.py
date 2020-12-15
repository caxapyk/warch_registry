from flask import render_template, request

from warch_registry.app import auth, bp_summary
from warch_registry.models import RegistryModel, InventoryModel, InventoryTypeModel
from warch_registry.forms import SummaryForm


@bp_summary.route("/")
@auth.login_required
def index():
    registries_list = RegistryModel.query.all()

    form = SummaryForm(request.values)
    form.registry_id.choices = [
        (reg.id, reg.name + (u" (ОЦ)" if reg.valuable else u"")) for reg in registries_list]

    if request.method == 'GET' and request.args.get('registry_id') and form.validate():
        filter = list()
        filter.append(InventoryModel.regid ==
                      request.args.get('registry_id'))

        total_ = InventoryModel.query.filter(*filter).count()

        in_filter = filter
        if request.args.get('year'):
            in_filter.append(InventoryModel.in_year ==
                         request.args.get('year'))
        in_ = InventoryModel.query.filter(*in_filter).count()

        in_complect_ = InventoryModel.query.filter(
            *in_filter + [InventoryModel.copies == 3]).count()

        in_by_type_ = []
        inventory_types_list = InventoryTypeModel.query.all()
        for inv_type in inventory_types_list:
            in_by_type_.append((inv_type.name, InventoryModel.query.filter(
                *in_filter + [InventoryModel.inventory_type == inv_type.id]).count()))
        in_by_type_.append((u"Тип не указан", InventoryModel.query.filter(
            *in_filter + [InventoryModel.inventory_type == None]).count()))

        out_filter = filter
        if request.args.get('year'):
            out_filter.append(InventoryModel.out_year ==
                          request.args.get('year'))
        else:
            out_filter.append(InventoryModel.out_year.isnot(None))
        out_ = InventoryModel.query.filter(*out_filter).count()

        return render_template('summary/index.html', form=form, total_=total_, in_=in_, in_complect_=in_complect_, in_by_type_=in_by_type_, out_=out_)

    return render_template('summary/index.html', form=form)
