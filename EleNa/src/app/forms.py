from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange


class FieldsRequiredForm(FlaskForm):
    """Require all fields to have content. This works around the bug that WTForms radio
    fields don't honor the `DataRequired` or `InputRequired` validators.
    """

    class Meta:
        def render_field(self, field, render_kw):
            render_kw.setdefault('required', True)
            return super().render_field(field, render_kw)


class SearchForm(FieldsRequiredForm):
    source = StringField('Source', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    percent = IntegerField('x %', validators=[NumberRange(min=100, max=200, message="Choose a value in [100%, 200%]")])
    maxmin = RadioField('Objective', choices=[('max', 'Max'), ('min', 'Min')], validators=[DataRequired()])
    submit = SubmitField('Get Route')

