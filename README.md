# BlueOak Investment Firm - Investment Platform

A professional investment platform built with Flask, featuring user registration, investment plans, UPI integration, referral system, and admin panel.

## Features

### 🚀 Core Features
- **User Registration & Authentication**: Secure user accounts with referral system
- **Investment Plans**: Multiple investment options with high returns
- **UPI Integration**: Deposit and withdrawal via UPI payments
- **Dashboard**: Real-time investment tracking and statistics
- **Referral System**: Earn ₹100 for each successful referral
- **Admin Panel**: Complete user and transaction management

### 💰 Investment Plans
- **Starter Plan**: ₹1,000 - ₹5,000 → 100% return in 10 days
- **Growth Plan**: ₹5,000 - ₹25,000 → 100% return in 7 days  
- **Premium Plan**: ₹10,000 - ₹100,000 → 50% return in 3 days

### 🔧 Technical Features
- **Flask Backend**: Python-based web framework
- **SQLite Database**: Lightweight database for data storage
- **Bootstrap UI**: Modern, responsive design
- **Security**: Password hashing, session management
- **Real-time Updates**: Live transaction and investment tracking

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BlueOak
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5001`
   - Admin login: Use phone number +919999999999

## Project Structure

```
BlueOak/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── dashboard.html    # User dashboard
│   ├── invest.html       # Investment page
│   ├── deposit.html      # Deposit funds
│   ├── withdraw.html     # Withdraw funds
│   ├── referrals.html    # Referral management
│   └── admin.html        # Admin panel
└── static/               # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

## Database Models

### User
- Basic user information (username, email, phone)
- Balance and investment tracking
- Referral code and earnings
- Admin privileges

### InvestmentPlan
- Plan details (name, min/max amounts, duration, returns)
- Active/inactive status

### Investment
- User investments with plan details
- Start/end dates and expected returns
- Status tracking (active/completed/cancelled)

### Transaction
- All financial transactions (deposits, withdrawals, investments, returns)
- UPI integration details
- Status tracking (pending/completed/failed)

### Referral
- Referral relationships and commissions
- Payment status tracking

## Usage

### For Users
1. **Register**: Create an account with or without referral code
2. **Deposit**: Add funds via UPI payment
3. **Invest**: Choose from available investment plans
4. **Track**: Monitor investments and earnings in dashboard
5. **Refer**: Share referral code to earn bonuses
6. **Withdraw**: Request withdrawals via UPI

### For Admins
1. **Login**: Access admin panel with admin credentials
2. **Manage Users**: View and manage user accounts
3. **Process Transactions**: Approve deposits and withdrawals
4. **Monitor Investments**: Track all active investments
5. **Process Returns**: Automatically credit completed investments

## Security Features

- **Password Hashing**: Secure password storage using bcrypt
- **Session Management**: Flask-Login for user sessions
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: SQLAlchemy ORM
- **CSRF Protection**: Built-in Flask security

## Payment Integration

### UPI Support
- Google Pay
- PhonePe
- Paytm
- Amazon Pay
- BHIM UPI

### Transaction Flow
1. User submits deposit/withdrawal request
2. Admin reviews and approves transaction
3. Manual UPI transfer processing
4. Status updated in system

## Referral System

### How it Works
1. User gets unique referral code upon registration
2. Friends register using the referral code
3. Referrer earns ₹100 bonus instantly
4. Bonus credited to account balance

### Benefits
- Instant bonus credits
- No minimum requirements
- Unlimited referrals
- Track referral earnings

## Admin Panel Features

### Dashboard Overview
- Total users, transactions, and investments
- System statistics and metrics
- Quick action buttons

### User Management
- View all user accounts
- Monitor balances and earnings
- Track user activity

### Transaction Management
- Review pending deposits/withdrawals
- Approve or reject transactions
- Process investment returns

### Investment Monitoring
- Track all active investments
- Monitor completion dates
- Process automatic returns

## Development

### Adding New Features
1. Update database models in `app.py`
2. Create new routes and logic
3. Add corresponding HTML templates
4. Test functionality thoroughly

### Customization
- Modify investment plans in `init_db()` function
- Update UI styling in `base.html`
- Add new payment methods
- Customize referral bonuses

## Deployment

### Production Setup
1. Use production WSGI server (Gunicorn)
2. Set up proper database (PostgreSQL/MySQL)
3. Configure environment variables
4. Set up SSL certificates
5. Use reverse proxy (Nginx)

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
DEBUG=False
```

## Support

For technical support or questions:
- Email: support@wealthmaxpro.com
- Phone: +91 98765 43210

## License

This project is for educational and demonstration purposes only.

## Disclaimer

This is a demonstration platform. Please ensure compliance with local financial regulations before using in production. 