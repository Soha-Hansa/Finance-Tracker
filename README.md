# Finance Tracker 💰📊
Take control of your finances with a modern, intuitive Flask‑based Expense Tracker. This project is designed to help users record, visualize, and analyze their income and expenses with ease.

## 👨‍💻 Dev's Corner
Hi, I’m Soha — a second‑year BCA student. This project reflects my recent learning journey with **Flask**.
It helps you track your daily income and expenses, giving insights into your spending habits. Since I’m still new to this web framework, I’ve kept the design minimalistic and beginner‑friendly.
I hope you enjoy exploring it!
## 🚀 Features - 
**User Authentication**: Register, login, and manage accounts securely with Flask-Login and Bcrypt. 
**Expense Management**: Add, edit, and delete expenses .
**Dashboard Visualization**: Interactive charts using Matplotlib & Seaborn for balance trends.  
**Database Support**: SQLAlchemy is used easily
**Responsive UI**: Bootstrap-powered templates for clean and mobile-friendly design.

## Project Workthrough 
 1. Login page opened as soon as enter the page.
 2.If you didn't have account register first.
 3. Income section helps you add your income.
 4. Expense section helps you add your expense.
 5. Dashboard show your total income, expense and net balance 
    It generates chart like income vs expense, expense pie chart
    that helps you better handling of money
 6. In support page there is chatbot **Elie** who resolve all your doubts (temporary),
    Developer support for all possible medium to contact with me.
 7. At last login, logout session.

 ## 📊 Project Screenshot !
 [Dashboard Screenshot](screenshots/dashboard.png)
 [Expense Screenshot](screenshots/expense.png)
 
## 🛠️ Tech Stack -
 Backend: Flask, Flask-SQLAlchemy, Flask-Migrate - 
 Frontend: Bootstrap, Jinja2 templates - 
 Visualization: Matplotlib, Seaborn, Pandas - 
 Authentication: Flask-Login, Flask-Bcrypt

## 📂 Project Structure
Finance-Tracker/
│
├── Expense/              # Main app package (routes, models, forms)
├── instance/             # Database files (SQLAlchemy)
├── venv/                 # Virtual environment (ignored in deployment)
├── run.py                                # Entry point for Flask app
├── requirements.txt      # Dependencies
├── runtime.txt           # Python version for deployment
├── Procfile              # Deployment start command
├── README.md                          # Documentation
└── templates/, static/   # HTML templates and static assets


## Badges
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Jinja](https://img.shields.io/badge/Jinja-Templating-orange.svg)](https://jinja.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)


## 🤝 Contribution Request
I am very begineer so if you have any suggestion, please feel free fork, suggest changes, or open issues. 
Even small tips or explanations will help me grow as a developer. Thank you for supporting my learning journey 🙏

# Contact Details:
gmail: compsoha1024@gmail.com 
Instagram: soha.calculative
## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Soha-Hansa/Finance-Tracker.git
cd Finance-Tracker

### Install Dependecy 
pip install -r requirements.txt

