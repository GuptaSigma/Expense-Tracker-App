# OTP Email Setup Guide

## How to Setup Email for OTP Verification

Your app now has OTP email verification for new registrations. Follow these steps to enable it:

### Step 1: Gmail Setup (Recommended)

1. Go to [Google Account](https://myaccount.google.com)
2. Click "Security" in the left menu
3. Enable "2-Step Verification" if not already enabled
4. Go back to Security and look for "App passwords"
   - Select "Mail" and "Windows Computer" (or your device type)
   - Google will generate a 16-character password
5. Copy this password

### Step 2: Update .env File

Edit your `.env` file and add the following with your Gmail credentials:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-16-chars
MAIL_DEFAULT_SENDER=noreply@expensetracker.com
```

### Step 3: Restart Your App

The OTP email feature will now be active. When users register:
1. They fill in registration form
2. OTP is generated and sent to their email
3. User verifies OTP on `/verify-otp` page
4. Only after verification, email is marked as verified

### Important Notes

- **OTP Expiry**: OTP expires after 10 minutes
- **Resend Limit**: Users can resend OTP max 3 times per minute
- **Development**: If email is not configured, OTP will print to console for testing
- **Alternative Providers**: You can also use SendGrid, Mailgun, or other SMTP services

### Security Features

✅ OTP stored in database (hashed in production)
✅ OTP expiry time tracked
✅ Rate limiting on OTP requests
✅ CSRF protection on all forms
✅ Secure email transmission (TLS)

### Testing Without Email

During development, if you don't configure email, the OTP will be printed to your console logs. You can then use that OTP in the verification form.

```
Example console output:
Email not configured. OTP for test@example.com: 123456
```
