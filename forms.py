from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(FlaskForm):
    name = StringField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )

    demographic_sex = StringField(
        'Sex', validators=[DataRequired(), Length(min=1, max=10)]
    )

    demographic_age = StringField(
        'Age range', validators=[DataRequired(), Length(min=1, max=10)]
    )


    # Age range 0-2, 3-6, 7-10, 11-15, 16-21, 22-30, 31-40, 41-50, 51-70, 70+

    # Sex: F / M / Other

    # Ethnicity:


    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(FlaskForm):
    name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
