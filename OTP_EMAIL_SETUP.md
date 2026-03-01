# OTP Email Setup Guide

## How OTP Email Delivery Works

OTP verification emails are sent via a **Google Apps Script Web App API**. No SMTP credentials or email provider account is required.

### How It Works

1. When a user registers, the app calls the Google Apps Script endpoint via `POST` request.
2. The Apps Script sends the OTP email to the user's address.
3. The user enters the OTP on the `/verify-otp` page to complete registration.

### Apps Script Web App URL

The endpoint used internally:

```
https://script.google.com/macros/s/AKfycbxoStF25frOY88NGrFemsiDqIoTgOD3sQzUYF6kwp4rTXHlmH3AlZRR9caNMTwDzIrl/exec
```

No additional configuration is needed — the URL is hardcoded in `app/utils.py`.

### Environment Variables

No mail-server variables are required. The only OTP-related env vars are:

| Variable | Default | Description |
|---|---|---|
| `DISABLE_EMAIL_OTP` | `false` | Set to `true` to skip OTP verification (auto-verify on register). **Do not use in production.** |
| `OTP_DEV_MODE` | `false` | Set to `true` to print OTP to console instead of sending via Apps Script. **Never enable in production.** |

### Important Notes

- **OTP Expiry**: OTP expires after 10 minutes
- **Resend Limit**: Users can resend OTP max 3 times per minute
- **No sender config needed**: All email delivery is handled by the Apps Script
- **Fallback logging**: If the API call fails, the error is logged under `[OTP][GAS]`

### Security Features

✅ OTP stored in database
✅ OTP expiry time tracked
✅ Rate limiting on OTP requests
✅ CSRF protection on all forms
