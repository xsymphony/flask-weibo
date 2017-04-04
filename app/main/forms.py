#coding=utf-8
from flask_wtf import Form
from flask_pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class NameForm(Form):
    name = StringField(u'快来和大家分享你的新鲜事吧~', validators=[Required()])
    submit = SubmitField(u'确认')

class EditProfileForm(Form):
	name = StringField(u'姓名', validators=[Length(0,64)])
	location = StringField(u'所在地', validators=[Length(0,64)])
	about_me = TextAreaField(u'个人简介')
	submit = SubmitField(u'确认')

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册.')

class PostForm(Form):
	body = PageDownField(u"快来和大家分享你的新鲜事吧~", validators=[Required()])
	submit = SubmitField(u'确认')

class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField(u'回复')