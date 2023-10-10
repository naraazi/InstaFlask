from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    caption = StringField('Caption')
    images = HiddenField('images', validators=[DataRequired('You must upload at least one image')])
    submit = SubmitField('Add Post')
