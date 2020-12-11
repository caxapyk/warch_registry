from flask import redirect, request, render_template, url_for

from warch_registry.app import db, auth, bp_registry
from warch_registry.models import RegistryModel
from warch_registry.forms import RegistryForm


@bp_registry.route('/')
@auth.login_required
def index():
    objects_list = RegistryModel.query.all()
    return render_template('registry/index.html', objects_list=objects_list)

@bp_registry.route('/create', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def create():
    form = RegistryForm(request.form)
    if request.method == 'POST' and form.validate():
        registry = RegistryModel()
        form.populate_obj(registry)

        db.session.add(registry)
        db.session.commit()

        return redirect(url_for("registry.index"))

    return render_template('registry/create.html', form=form)

@bp_registry.route('/update/<int:id>', methods=['GET', 'POST'])
@auth.login_required(role='manager')
def update(id):
    registry = RegistryModel.query.get(id)
    form = RegistryForm(request.form, obj=registry)

    if request.method == 'POST' and form.validate():
        form.populate_obj(registry)

        db.session.add(registry)
        db.session.commit()

        return redirect(url_for("registry.index"))

    return render_template('registry/update.html', form=form)

@bp_registry.route('/remove', methods=['POST'])
@bp_registry.route('/remove/<int:id>', methods=['GET'])
@auth.login_required(role='manager')
def remove(id=None):
    RegistryModel.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for("registry.index"))
