# BlueOak Investment Firm - Quick Setup Guide

## 🚀 Application Status: RUNNING

Your investment platform is now live and running on **http://localhost:5001**

## 📋 Quick Access

### Admin Access
- **URL**: http://localhost:5001/admin
- **Phone**: +919999999999
- **Login**: Use OTP sent to phone

### User Registration
- **URL**: http://localhost:5001/register
- Create new user accounts with referral codes

## 🎯 Key Features Ready to Use

### ✅ User Management
- User registration with referral system
- Secure login/logout
- User dashboard with statistics

### ✅ Investment Plans
- **Starter Plan**: ₹1,000 - ₹5,000 → 100% return in 10 days
- **Growth Plan**: ₹5,000 - ₹25,000 → 100% return in 7 days
- **Premium Plan**: ₹10,000 - ₹100,000 → 50% return in 3 days

### ✅ Payment System
- UPI deposit requests
- UPI withdrawal requests
- Admin approval system
- Transaction tracking

### ✅ Referral System
- Unique referral codes for each user
- ₹100 bonus for each successful referral
- Referral tracking and earnings

### ✅ Admin Panel
- Complete user management
- Transaction approval system
- Investment monitoring
- System statistics

## 🔧 How to Use

### For Testing Users:
1. Go to http://localhost:5001/register
2. Create a new account
3. Use admin panel to approve deposits
4. Make investments and track returns

### For Admins:
1. Login at http://localhost:5001/admin
2. Review pending transactions
3. Approve deposits/withdrawals
4. Monitor system activity

## 📊 Database Status
- ✅ SQLite database created: `instance/investment_platform.db`
- ✅ Sample investment plans loaded
- ✅ Admin user created
- ✅ All tables initialized

## 🛠️ Technical Details

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Authentication**: Flask-Login
- **Security**: Password hashing with bcrypt

### Frontend
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Responsive**: Mobile-friendly design

### File Structure
```
BlueOak/
├── app.py                 # Main application (436 lines)
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── templates/            # HTML templates (10 files)
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── register.html     # Registration
│   ├── login.html        # Login
│   ├── dashboard.html    # User dashboard
│   ├── invest.html       # Investment page
│   ├── deposit.html      # Deposit funds
│   ├── withdraw.html     # Withdraw funds
│   ├── referrals.html    # Referral management
│   └── admin.html        # Admin panel
└── static/               # Static assets
```

## 🎨 Design Features
- Modern, professional UI
- Gradient backgrounds and cards
- Responsive design for all devices
- Interactive elements with hover effects
- Professional color scheme (blue/white)

## 🔒 Security Features
- Password hashing
- Session management
- Input validation
- SQL injection protection
- CSRF protection

## 📱 Mobile Responsive
- Works perfectly on mobile devices
- Touch-friendly interface
- Optimized for all screen sizes

## 🚀 Ready for Production
The platform is ready for deployment with:
- Complete user management
- Payment processing system
- Admin controls
- Database persistence
- Security measures

## 📞 Support
For any issues or questions, refer to the main README.md file for detailed documentation.

---

**🎉 Your WealthMax Pro investment platform is now fully operational!** 