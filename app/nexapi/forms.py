from flask_wtf import FlaskForm
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField

class NameForm(FlaskForm):
    name = StringField('名称', validators=[Required()])
    submit = SubmitField('Submit')

class ConfigForm(FlaskForm):
    name = StringField('配置', validators=[Required()])
    # submit = SubmitField('Submit')

class DescForm(FlaskForm):
    name = StringField('描述', validators=[Required()])
    submit = SubmitField('Submit')