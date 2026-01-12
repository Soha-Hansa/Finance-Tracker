from Expense import db
from Expense import bcrypt
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    expenses = db.relationship('AddExpense', backref='user', lazy=True)
    incomes = db.relationship('AddIncome', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")  # ✅ safer

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class AddExpense(db.Model):
    __tablename__ = 'addExpense'
    id = db.Column(db.Integer, primary_key=True)
    e_amount = db.Column(db.Integer, nullable=False)
    e_date = db.Column(db.Date, nullable=False)
    e_description = db.Column(db.String(length=500), nullable=False)
    category = db.Column(db.String(50))
    e_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class AddIncome(db.Model):
    __tablename__ = 'addIncome'
    id = db.Column(db.Integer, primary_key=True)
    i_amount = db.Column(db.Integer, nullable=False)
    i_date = db.Column(db.Date, nullable=False)
    i_description = db.Column(db.String(length=500), nullable=False)
    source = db.Column(db.String(50))
    i_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
