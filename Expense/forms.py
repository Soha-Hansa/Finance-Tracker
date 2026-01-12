from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField,DateField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from Expense.model import User
class ExpenseForm(FlaskForm):
    e_amount = IntegerField("Amount:", validators=[DataRequired()])
    e_date = DateField("Date:", format='%Y-%m-%d', validators=[DataRequired()])
    e_description = TextAreaField("Description", validators=[DataRequired()])
    category = SelectField("Category", choices=[
        ("Grocessory","Grocessory"),
        ("Medicine","Medicine"),
        ("Electronics","Electronics"),
        ("Transportation","Transportation"),
        ("Insurance","Insurance"),
        ("Other","Other")
    ], validators=[DataRequired()])
    submit = SubmitField("Add Expense")


class IncomeForm(FlaskForm):
    i_amount = IntegerField("Amount:", validators=[DataRequired()])
    i_date = DateField("Date:", format='%Y-%m-%d', validators=[DataRequired()])
    i_description = TextAreaField("Description", validators=[DataRequired()])
    source = SelectField("Category", choices=[
        ("Salary", "Salary"),
        ("Freelance", "Freelance"),
        ("Gift", "Gift"),
        ("Other", "Other")
    ], validators=[DataRequired()])
    submit = SubmitField("Add Income")


class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exsists, please try with a different one")

    def validate_email(self,email_to_check):
        email=User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already exsists, please try with a different one")

    username=StringField(label=" Enter your Username:",validators=[Length(min=2,max=30),DataRequired()])
    email=StringField(label="Email: ",validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Enter Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    remember_me = BooleanField("Confirm above details")
    submit = SubmitField(label='Sign In')

class LoginForm(FlaskForm):
    email = StringField(label="Email:", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


