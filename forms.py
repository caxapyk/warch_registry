from datetime import date
from wtforms.form import Form
from wtforms.fields import BooleanField, FieldList, FormField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import CheckboxInput, TextInput, TextArea, Select, SubmitInput
from wtforms.widgets.html5 import DateInput, NumberInput


class BaseForm(Form):
    class Meta:
        locales = ['ru_RU', 'ru']


class CustomCheckboxInput(CheckboxInput):
    """Custom checkbox input with Bootstrap validation from WTForms CheckboxInput"""

    def __init__(self, error_class=u"is-invalid"):
        super(CustomCheckboxInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop(
            "class", "") or kwargs.pop("class_", "")
        kwargs["class"] = u"form-control custom-control-input %s" % c

        if field.errors:
            kwargs["class"] += self.error_class
            kwargs["aria-describedby"] = u"%sValidationFeedback" % field.id

        return super(CustomCheckboxInput, self).__call__(field, **kwargs)

class CustomNumberInput(NumberInput):
    """Custom number input with Bootstrap validation from WTForms NumberInput"""

    def __init__(self, error_class=u"is-invalid", step=None, min=None, max=None):
        super(CustomNumberInput, self).__init__(step, min, max)
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop(
            "class", "") or kwargs.pop("class_", "")
        kwargs["class"] = u"form-control form-control-sm %s" % c

        if field.errors:
            kwargs["class"] += self.error_class
            kwargs["aria-describedby"] = u"%sValidationFeedback" % field.id

        return super(CustomNumberInput, self).__call__(field, **kwargs)

class CustomTextInput(TextInput):
    """Custom input with Bootstrap validation from WTForms TextInput"""

    def __init__(self, error_class=u"is-invalid"):
        super(CustomTextInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop(
            "class", "") or kwargs.pop("class_", "")
        kwargs["class"] = u"form-control form-control-sm %s" % c

        if field.errors:
            kwargs["class"] += self.error_class
            kwargs["aria-describedby"] = u"%sValidationFeedback" % field.id

        return super(CustomTextInput, self).__call__(field, **kwargs)

class CustomSelect(Select):
    """Custom select with Bootstrap validation from WTForms Select"""

    def __init__(self, error_class=u"is-invalid"):
        super(CustomSelect, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop(
            "class", "") or kwargs.pop("class_", "")
        kwargs["class"] = u"form-control form-control-sm custom-select custom-select-sm %s" % c

        if field.errors:
            kwargs["class"] += self.error_class
            kwargs["aria-describedby"] = u"%sValidationFeedback" % field.id

        return super(CustomSelect, self).__call__(field, **kwargs)

class CustomSubmitInput(SubmitInput):
    """Custom submit input with Bootstrap validation from WTForms SubmitInput"""

    def __init__(self, error_class=u"is-invalid"):
        super(CustomSubmitInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop(
            "class", "") or kwargs.pop("class_", "")
        kwargs["class"] = u"btn btn-primary %s" % c

        return super(CustomSubmitInput, self).__call__(field, **kwargs)


class RegistryForm(BaseForm):
    name = StringField("Название*:", validators=[
                       DataRequired(), Length(min=2, max=100)], widget=CustomTextInput())
    submit = SubmitField("Сохранить", widget=CustomSubmitInput())


class InventoryForm(BaseForm):
    regid = HiddenField()
    fund_number = StringField("Номер фонда*:", validators=[
        DataRequired(), Length(max=50)], widget=CustomTextInput())
    number = IntegerField("Номер описи:", validators=[
        DataRequired(), NumberRange(min=1, max=999)], widget=CustomNumberInput(min=1, max=999))
    title = StringField("Название описи:", validators=[
        Optional(), Length(max=100)], widget=CustomTextInput())
    valuable = BooleanField("Особо ценное", validators=[
        Optional()], widget=CustomCheckboxInput())
    record_total = IntegerField("Всего ед. хр.:", validators=[
        DataRequired(), NumberRange(min=1, max=9999)], widget=CustomNumberInput(min=1, max=9999))
    record_private = IntegerField("В т.ч. по л.с.:", validators=[
        Optional(), NumberRange(min=1, max=9999)], widget=CustomNumberInput(min=1, max=9999))
    dates = StringField("Крайние даты:", validators=[
        Optional(), Length(max=100)], widget=CustomTextInput())
    copies = IntegerField("Кол-во экз.:", validators=[
        DataRequired(), NumberRange(min=1, max=9)], widget=CustomNumberInput(min=1, max=9))
    digital_copy = BooleanField("В т.ч. оцифровано", validators=[
        Optional()], widget=CustomCheckboxInput())
    in_year = SelectField("Год приема:", validators=[
        Optional()], filters=[lambda x: x or None], widget=CustomSelect(), choices=[y for y in range(1990, date.today().year)])
    out_year = SelectField("Год приема:", validators=[
        Optional()], filters=[lambda x: x or None], widget=CustomSelect(), choices=[y for y in range(1990, date.today().year)])

    submit = SubmitField("Сохранить", widget=CustomSubmitInput())
