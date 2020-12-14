from warch_registry.app import db


class RegistryModel(db.Model):
    __tablename__ = 'ri_registry'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class InventoryTypeModel(db.Model):
    __tablename__ = 'ri_inventory-type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)

class InventoryModel(db.Model):
    __tablename__ = 'ri_inventory'

    id = db.Column(db.Integer, primary_key=True)
    regid = db.Column(db.Integer, db.ForeignKey('ri_registry.id'))
    number = db.Column(db.String(20), nullable=False)
    fund_num = db.Column(db.String(50), nullable=False)
    inventory_num = db.Column(db.Integer, nullable=False)
    #inventory_type = db.Column(db.Integer, db.ForeignKey('ri_inventory-type.id'), nullable=True)
    inventory_name = db.Column(db.String(100), nullable=True)
    valuable = db.Column(db.Boolean, nullable=False)
    record_total = db.Column(db.Integer, nullable=False)
    record_private = db.Column(db.Integer, nullable=True)
    dates = db.Column(db.String(100), nullable=True)
    copies = db.Column(db.Integer, nullable=False)
    digital_copy = db.Column(db.Boolean, nullable=False)
    annotation = db.Column(db.String(255), nullable=True)
    in_year = db.Column(db.Integer, nullable=True)
    out_year = db.Column(db.Integer, nullable=True)

    registry = db.relationship("RegistryModel")
    #inventory_type = db.relationship("InventoryTypeModel")
