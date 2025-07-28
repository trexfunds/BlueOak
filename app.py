from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///investment_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    referral_code = db.Column(db.String(10), unique=True, nullable=False)
    referred_by = db.Column(db.String(10), nullable=True)
    balance = db.Column(db.Float, default=0.0)
    total_invested = db.Column(db.Float, default=0.0)
    total_earned = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class InvestmentPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_amount = db.Column(db.Float, nullable=False)
    max_amount = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    return_percentage = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('investment_plan.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expected_return = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdrawal, investment, return, referral
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    reference_id = db.Column(db.String(50), unique=True, nullable=False)
    upi_id = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commission_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending, paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_referral_code():
    return str(uuid.uuid4())[:8].upper()

def generate_reference_id():
    return f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8].upper()}"

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_sms(phone, otp):
    # In a real implementation, integrate with SMS gateway like Twilio, MSG91, etc.
    # For now, we'll just print the OTP to console
    print(f"OTP for {phone}: {otp}")
    return True

# Routes
@app.route('/')
def index():
    plans = InvestmentPlan.query.filter_by(is_active=True).all()
    return render_template('index.html', plans=plans)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        referral_code = request.form.get('referral_code', '')

        # Validate phone number (Indian format)
        if not phone.startswith('+91') and len(phone) == 10:
            phone = '+91' + phone
        elif not phone.startswith('+91'):
            flash('Please enter a valid Indian phone number!', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(phone=phone).first():
            flash('Phone number already registered!', 'error')
            return redirect(url_for('register'))

        # Generate OTP
        otp = generate_otp()
        otp_expiry = datetime.utcnow() + timedelta(minutes=10)

        # Create user with OTP
        user = User(
            name=name,
            phone=phone,
            otp=otp,
            otp_expiry=otp_expiry,
            referral_code=generate_referral_code(),
            referred_by=referral_code if referral_code else None
        )

        db.session.add(user)
        db.session.commit()

        # Send OTP via SMS
        if send_otp_sms(phone, otp):
            flash('OTP sent to your phone number! Please verify to complete registration.', 'success')
            return redirect(url_for('verify_otp', phone=phone))
        else:
            flash('Failed to send OTP. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/verify_otp/<phone>', methods=['GET', 'POST'])
def verify_otp(phone):
    if request.method == 'POST':
        otp = request.form['otp']
        
        user = User.query.filter_by(phone=phone).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('register'))
        
        if user.otp != otp:
            flash('Invalid OTP!', 'error')
            return redirect(url_for('verify_otp', phone=phone))
        
        if user.otp_expiry < datetime.utcnow():
            flash('OTP expired! Please register again.', 'error')
            return redirect(url_for('register'))
        
        # Verify OTP and complete registration
        user.otp = None
        user.otp_expiry = None
        
        # Handle referral commission
        if user.referred_by:
            referrer = User.query.filter_by(referral_code=user.referred_by).first()
            if referrer:
                commission = 100  # ₹100 commission for referral
                referrer.balance += commission
                referrer.total_earned += commission
                
                referral = Referral(
                    referrer_id=referrer.id,
                    referred_id=user.id,
                    commission_amount=commission,
                    status='paid'
                )
                db.session.add(referral)
        
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('verify_otp.html', phone=phone)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        
        # Validate phone number (Indian format)
        if not phone.startswith('+91') and len(phone) == 10:
            phone = '+91' + phone
        elif not phone.startswith('+91'):
            flash('Please enter a valid Indian phone number!', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(phone=phone).first()
        if not user:
            flash('Phone number not registered!', 'error')
            return redirect(url_for('login'))
        
        # Generate and send OTP
        otp = generate_otp()
        otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        
        user.otp = otp
        user.otp_expiry = otp_expiry
        db.session.commit()
        
        if send_otp_sms(phone, otp):
            flash('OTP sent to your phone number!', 'success')
            return redirect(url_for('verify_login_otp', phone=phone))
        else:
            flash('Failed to send OTP. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/verify_login_otp/<phone>', methods=['GET', 'POST'])
def verify_login_otp(phone):
    if request.method == 'POST':
        otp = request.form['otp']
        
        user = User.query.filter_by(phone=phone).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('login'))
        
        if user.otp != otp:
            flash('Invalid OTP!', 'error')
            return redirect(url_for('verify_login_otp', phone=phone))
        
        if user.otp_expiry < datetime.utcnow():
            flash('OTP expired! Please try again.', 'error')
            return redirect(url_for('login'))
        
        # Clear OTP and login user
        user.otp = None
        user.otp_expiry = None
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('verify_login_otp.html', phone=phone)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_investments = Investment.query.filter_by(user_id=current_user.id, status='active').all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(10).all()
    referrals = Referral.query.filter_by(referrer_id=current_user.id).all()
    
    # Calculate total referral earnings
    total_referral_earnings = sum(ref.commission_amount for ref in referrals if ref.status == 'paid')
    
    return render_template('dashboard.html', 
                         investments=user_investments, 
                         transactions=transactions,
                         referrals=referrals,
                         total_referral_earnings=total_referral_earnings)

@app.route('/invest', methods=['GET', 'POST'])
@login_required
def invest():
    if request.method == 'POST':
        plan_id = request.form['plan_id']
        amount = float(request.form['amount'])
        
        plan = InvestmentPlan.query.get(plan_id)
        if not plan or not plan.is_active:
            flash('Invalid investment plan!', 'error')
            return redirect(url_for('invest'))
        
        if amount < plan.min_amount or amount > plan.max_amount:
            flash(f'Amount must be between ₹{plan.min_amount} and ₹{plan.max_amount}!', 'error')
            return redirect(url_for('invest'))
        
        if current_user.balance < amount:
            flash('Insufficient balance! Please deposit funds first.', 'error')
            return redirect(url_for('invest'))
        
        # Calculate expected return
        expected_return = amount * (1 + plan.return_percentage / 100)
        end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
        
        # Create investment
        investment = Investment(
            user_id=current_user.id,
            plan_id=plan_id,
            amount=amount,
            expected_return=expected_return,
            end_date=end_date
        )
        
        # Deduct amount from balance
        current_user.balance -= amount
        current_user.total_invested += amount
        
        # Create transaction record
        transaction = Transaction(
            user_id=current_user.id,
            transaction_type='investment',
            amount=amount,
            status='completed',
            reference_id=generate_reference_id()
        )
        
        db.session.add(investment)
        db.session.add(transaction)
        db.session.commit()
        
        flash('Investment created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    plans = InvestmentPlan.query.filter_by(is_active=True).all()
    return render_template('invest.html', plans=plans)

@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        upi_id = request.form['upi_id']
        
        if amount < 100:
            flash('Minimum deposit amount is ₹100!', 'error')
            return redirect(url_for('deposit'))
        
        # Create pending transaction
        transaction = Transaction(
            user_id=current_user.id,
            transaction_type='deposit',
            amount=amount,
            status='pending',
            reference_id=generate_reference_id(),
            upi_id=upi_id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('Deposit request submitted! Our team will process it within 24 hours.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        upi_id = request.form['upi_id']
        
        if amount < 100:
            flash('Minimum withdrawal amount is ₹100!', 'error')
            return redirect(url_for('withdraw'))
        
        if current_user.balance < amount:
            flash('Insufficient balance!', 'error')
            return redirect(url_for('withdraw'))
        
        # Create withdrawal transaction
        transaction = Transaction(
            user_id=current_user.id,
            transaction_type='withdrawal',
            amount=amount,
            status='pending',
            reference_id=generate_reference_id(),
            upi_id=upi_id
        )
        
        # Deduct from balance
        current_user.balance -= amount
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('Withdrawal request submitted! Our team will process it within 24 hours.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('withdraw.html')

@app.route('/referrals')
@login_required
def referrals():
    user_referrals = Referral.query.filter_by(referrer_id=current_user.id).all()
    referral_users = []
    for ref in user_referrals:
        user = User.query.get(ref.referred_id)
        referral_users.append({
            'user': user,
            'referral': ref
        })
    
    return render_template('referrals.html', referrals=referral_users)

# Admin Routes
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied!', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(50).all()
    investments = Investment.query.all()
    
    return render_template('admin.html', users=users, transactions=transactions, investments=investments)

@app.route('/admin/approve_transaction/<transaction_id>')
@login_required
def approve_transaction(transaction_id):
    if not current_user.is_admin:
        flash('Access denied!', 'error')
        return redirect(url_for('dashboard'))
    
    transaction = Transaction.query.get(transaction_id)
    if transaction and transaction.status == 'pending':
        if transaction.transaction_type == 'deposit':
            user = User.query.get(transaction.user_id)
            user.balance += transaction.amount
            transaction.status = 'completed'
        elif transaction.transaction_type == 'withdrawal':
            transaction.status = 'completed'
        
        db.session.commit()
        flash('Transaction approved successfully!', 'success')
    
    return redirect(url_for('admin'))

@app.route('/admin/process_returns')
@login_required
def process_returns():
    if not current_user.is_admin:
        flash('Access denied!', 'error')
        return redirect(url_for('dashboard'))
    
    # Process completed investments
    completed_investments = Investment.query.filter(
        Investment.status == 'active',
        Investment.end_date <= datetime.utcnow()
    ).all()
    
    for investment in completed_investments:
        user = User.query.get(investment.user_id)
        user.balance += investment.expected_return
        user.total_earned += (investment.expected_return - investment.amount)
        investment.status = 'completed'
        
        # Create return transaction
        transaction = Transaction(
            user_id=user.id,
            transaction_type='return',
            amount=investment.expected_return,
            status='completed',
            reference_id=generate_reference_id()
        )
        db.session.add(transaction)
    
    db.session.commit()
    flash(f'Processed {len(completed_investments)} investment returns!', 'success')
    return redirect(url_for('admin'))

# Initialize database and create sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create sample investment plans if they don't exist
        if not InvestmentPlan.query.first():
            plans = [
                InvestmentPlan(
                    name='Foundation Portfolio',
                    min_amount=1000,
                    max_amount=5000,
                    duration_days=10,
                    return_percentage=100,  # 100% return
                    description='Entry-level arbitrage strategy portfolio. Initial capital ₹1,000 generates ₹2,000 through multi-market opportunities.'
                ),
                InvestmentPlan(
                    name='Accelerated Growth Portfolio',
                    min_amount=5000,
                    max_amount=25000,
                    duration_days=7,
                    return_percentage=100,  # 100% return
                    description='Enhanced arbitrage execution with advanced risk management. Capital ₹5,000 yields ₹10,000 through optimized trading algorithms.'
                ),
                InvestmentPlan(
                    name='Premium Arbitrage Portfolio',
                    min_amount=10000,
                    max_amount=100000,
                    duration_days=3,
                    return_percentage=50,  # 50% return
                    description='Institutional-grade arbitrage strategy with maximum leverage. Investment ₹10,000 generates ₹15,000 through high-frequency trading systems.'
                )
            ]
            
            for plan in plans:
                db.session.add(plan)
            
            # Create admin user
            admin_user = User(
                name='Admin',
                phone='+919999999999',
                referral_code='ADMIN001',
                is_admin=True
            )
            db.session.add(admin_user)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001) 