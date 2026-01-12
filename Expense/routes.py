#from sqlalchemy.sql.functions import current_user
from Expense import app
from flask import render_template,redirect,url_for,flash,session,jsonify,request
from flask_login import login_user
from Expense.forms import IncomeForm,ExpenseForm,RegisterForm,LoginForm
from Expense.model import db,AddExpense,AddIncome,User
from flask_login import logout_user, login_required,current_user
@app.route('/income_page',methods=['GET','POST'])
def income_page():
    form=IncomeForm()
    if form.validate_on_submit():
        income = AddIncome(
        i_amount=form.i_amount.data,
        i_date=form.i_date.data,
        source=form.source.data,
        i_description=form.i_description.data,
        i_user_id=current_user.id
    )

        #i_user_id=current_user.id
        db.session.add(income)
        db.session.commit()
        return redirect(url_for('income_page'))
    return render_template("income.html",form=form)

@app.route('/expense_page',methods=['GET','POST'])
def expense_page():
    form=ExpenseForm()
    if form.validate_on_submit():
        expense=AddExpense(
            e_amount=form.e_amount.data,
            e_date=form.e_date.data,
            category=form.category.data,
            e_description=form.e_description.data,
            e_user_id=current_user.id)
       # e_user_id=current_user.id#need to build later e_user_id
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully","success")
        return redirect(url_for('expense_page'))
    return render_template("expense.html",form=form)

@app.route('/support_page')
def support_page():
    return render_template("support.html")
@app.route('/register_page', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            )
        user_to_create.password = form.password1.data
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('income_page'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f"There is an error with creating a new user:{err_msg}",category='danger')
    return render_template("register.html",form=form)
@app.route('/', methods=['GET', 'POST'])
@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f"Welcome {attempted_user.username}!", category='success')
            return redirect(url_for('expense_page'))
        else:
            flash("Email and password are not matched! Please try again",category='danger')
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
   # flash("You have been logged out", category="info")
    return redirect(url_for('login_page'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_page():
    import os
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')   # ensure non-GUI backend
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Query records
    incomes = AddIncome.query.filter_by(i_user_id=current_user.id).order_by(AddIncome.i_date.desc()).all()
    expenses = AddExpense.query.filter_by(e_user_id=current_user.id).order_by(AddExpense.e_date.desc()).all()

    # Build DataFrames with explicit columns (safe even if empty)
    df_income = pd.DataFrame(
        [{"date": i.i_date.strftime("%Y-%m"), "amount": i.i_amount, "type": "Income"} for i in incomes],
        columns=["date", "amount", "type"]
    )
    df_expense = pd.DataFrame(
        [{"date": e.e_date.strftime("%Y-%m"), "amount": e.e_amount, "type": "Expense"} for e in expenses],
        columns=["date", "amount", "type"]
    )
    df = pd.concat([df_income, df_expense], ignore_index=True)

    # Category breakdown
    df_cat = pd.DataFrame([{"category": e.category, "amount": e.e_amount} for e in expenses],
                          columns=["category", "amount"])

    # Theme
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.15)
    static_path = app.static_folder

    # Handle empty case (new user)
    if df.empty:
        # Generate placeholder charts
        for fname in ["income_expense.png", "expense_pie.png", "net_balance.png"]:
            plt.figure(figsize=(6,4))
            plt.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14)
            plt.axis("off")
            plt.savefig(os.path.join(static_path, fname))
            plt.close()

        total_income = 0
        total_expenses = 0
        net_balance = 0
        record_type = 'income'
        records = []
    else:
        # Net balance per month
        df_month = df.groupby(["date", "type"])["amount"].sum().unstack(fill_value=0)
        df_month["net"] = df_month.get("Income", 0) - df_month.get("Expense", 0)
        df_balance = df_month["net"]

        # 1) Income vs Expense chart
        plt.figure(figsize=(9,5))
        sns.barplot(data=df, x="date", y="amount", hue="type",
                    palette={"Income": "#4CAF50", "Expense": "#F44336"})
        plt.title("Income vs Expense (Monthly)", fontsize=16, fontweight="bold")
        plt.xlabel("Month"); plt.ylabel("Amount (₹)")
        plt.legend(title="Type"); plt.tight_layout()
        plt.savefig(os.path.join(static_path, "income_expense.png")); plt.close()

        # 2) Expense category pie
        plt.figure(figsize=(6.5,6.5))
        df_cat_grouped = df_cat.groupby("category", as_index=False)["amount"].sum()
        colors = sns.color_palette("pastel", n_colors=len(df_cat_grouped))
        plt.pie(df_cat_grouped["amount"], labels=df_cat_grouped["category"],
                autopct="%1.1f%%", colors=colors, textprops={"fontsize": 12})
        plt.title("Expense Breakdown by Category", fontsize=16, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(static_path, "expense_pie.png")); plt.close()

        # 3) Net balance line
        plt.figure(figsize=(9,5))
        sns.lineplot(x=df_balance.index, y=df_balance.values, marker="o", color="#2196F3")
        plt.title("Net Balance Over Time", fontsize=16, fontweight="bold")
        plt.xlabel("Month"); plt.ylabel("Net Balance (₹)")
        plt.tight_layout()
        plt.savefig(os.path.join(static_path, "net_balance.png")); plt.close()

        # Totals
        total_income = sum(i.i_amount for i in incomes)
        total_expenses = sum(e.e_amount for e in expenses)
        net_balance = total_income - total_expenses

        # Default: show last 5 incomes
        record_type = 'income'
        records = incomes[:5]

        if request.method == 'POST':
            record_type = request.form.get('record_type', 'income')
            records = expenses[:5] if record_type == 'expense' else incomes[:5]

    return render_template(
        'dashboard.html',
        incomes=incomes,
        expenses=expenses,
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        records=records,
        record_type=record_type
    )


@app.route('/delete/<int:record_id>/<string:record_type>',
           methods=['GET','POST'])
@login_required
def delete_record(record_type,record_id):
    if record_type=='expense':
        record=AddExpense.query.get_or_404(record_id)
    elif record_type=='income':
        record=AddIncome.query.get_or_404(record_id)
    else:
        return jsonify({"Success": False,"error":"Invalid record type"}),400
    db.session.delete(record)
    db.session.commit()
    flash(f"{record_type.capitalize()} deleted successfully!", "success")
    return redirect(url_for('dashboard_page'))