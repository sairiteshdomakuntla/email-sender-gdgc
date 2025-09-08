# GDGC Email Sender Setup Guide

## Prerequisites

1. Python 3.7 or higher
2. Gmail account
3. Google Sheets API access

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail" application
   - Copy the 16-character password

### 3. Google Sheets API Setup

#### Option A: Service Account (Recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing one
3. Enable Google Sheets API
4. Create Service Account:
   - IAM & Admin → Service Accounts → Create Service Account
   - Download JSON key file
   - Rename to `service-account.json` and place in project folder
5. Share your Google Sheet with the service account email

#### Option B: OAuth (Alternative)
1. Create OAuth credentials in Google Cloud Console
2. Download credentials.json file
3. First run will open browser for authentication

### 4. Update Configuration

Edit `gdgc_email_sender.py` and update these variables:

```python
SENDER_EMAIL = "your-email@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "your-app-password"  # 16-character app password from step 2
```

### 5. Sheet Format

Ensure your Google Sheet has email addresses in **Column A**:

```
A
sainiteshdomakuntla@gmail.com
domakuntlasairitesh@gmail.com
arbazahmed1729@gmail.com
```

## Usage

### Run the Script

```bash
python gdgc_email_sender.py
```

### Choose Option:

1. **Test Email** - Send to one email to verify setup
2. **Send All** - Send to all emails in the sheet

## Security Notes

- Never commit `service-account.json` or credentials to version control
- Use app passwords, not regular Gmail passwords
- Add these files to `.gitignore`:
  ```
  service-account.json
  credentials.json
  *.log
  ```

## Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Check app password is correct
   - Ensure 2FA is enabled on Gmail

2. **"Google Sheets access denied"**
   - Share sheet with service account email
   - Check sheet ID is correct

3. **"Rate limit exceeded"**
   - Script has 1-second delay between emails
   - Gmail limit: ~100 emails per day for new accounts

### Logs

Check console output for detailed error messages and progress updates.

## Features

- ✅ Reads emails from Google Sheets column A
- ✅ Professional HTML email template
- ✅ Error handling and logging
- ✅ Rate limiting to avoid Gmail limits
- ✅ Test email functionality
- ✅ Detailed success/failure reporting

## Email Content

The script sends a professionally formatted GDGC recruitment assignment email with:
- Job Portal Assignment details
- Core features requirements
- Bonus features (optional)
- Guidelines and deadline
- GDGC branding and styling