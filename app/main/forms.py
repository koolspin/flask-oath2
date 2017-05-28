from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField

class FormCsDelete(Form):
    cs_id = HiddenField()
    name = StringField('System Name')
    submit = SubmitField('Delete')

