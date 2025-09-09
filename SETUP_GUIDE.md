# GDGC Email Sender Setup Guide

## Prerequisites

1. **Python 3.7 or higher**
2. **Gmail account**
3. **Public Google Sheet** (no API required)

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

### 3. Google Sheets Setup (Simplified)

#### Make Your Sheet Public
1. Open your Google Sheet
2. Click **"Share"** button (top-right)
3. Click **"Change to anyone with the link"**
4. Set permission to **"Viewer"**
5. Copy the **Sheet ID** from URL

**Example URL:**
```
https://docs.google.com/spreadsheets/d/1Pf9ROUKO3gqoyB35TnPIM6I7EY8kR_qsaH5hCwZFvr8/edit
```
**Sheet ID:** `1Pf9ROUKO3gqoyB35TnPIM6I7EY8kR_qsaH5hCwZFvr8`

### 4. Update Configuration

Edit [`gdgc_email_sender.py`](gdgc_email_sender.py) and update these variables:

```python
SHEET_ID = "your-google-sheet-id-here"      # From step 3
SENDER_EMAIL = "your-email@gmail.com"       # Your Gmail address
SENDER_PASSWORD = "your-app-password-here"  # 16-character app password from step 2
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

- **No service account needed** - Uses public sheet CSV export
- Use app passwords, not regular Gmail passwords
- Keep your app password secure and don't commit it to version control
- Add sensitive files to `.gitignore`:
  ```
  *.log
  .env
  ```

## Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Check app password is correct (16 characters, no spaces)
   - Ensure 2FA is enabled on Gmail
   - Try generating a new app password

2. **"Error reading emails from sheet"**
   - Ensure sheet is set to "Anyone with the link can view"
   - Check sheet ID is correct (from the URL)
   - Make sure emails are in Column A

3. **"Rate limit exceeded"**
   - Script has 1-second delay between emails
   - Gmail limit: ~100 emails per day for new accounts
   - Wait 24 hours before sending more

4. **"No valid emails found"**
   - Check that Column A contains valid email addresses
   - Remove any headers or empty rows at the top
   - Ensure emails contain '@' symbol

### Logs

Check console output for detailed error messages and progress updates.

## Features

- ✅ **No API setup required** - Uses public sheet CSV export
- ✅ **Simple configuration** - Just Sheet ID and Gmail credentials
- ✅ Professional HTML email template with GDGC branding
- ✅ Assignment document link and submission form
- ✅ Contact information (phone numbers)
- ✅ Social media links (LinkedIn & Instagram)
- ✅ Error handling and logging
- ✅ Rate limiting to avoid Gmail limits
- ✅ Test email functionality
- ✅ Detailed success/failure reporting

## Email Content

The script sends a professionally formatted GDGC recruitment email with:

### 📋 **Assignment Section:**
- Link to assignment document
- Clear instructions to view requirements

### 📝 **Submission Section:** 
- Google Forms link for assignment submission
- Green button for easy identification

### 📞 **Contact Information:**
- Sai Ritesh: 8639154193
- Hasnika: 7981367685

### 🔗 **Social Media Links:**
- LinkedIn: https://www.linkedin.com/company/gdsc-vnrvjiet/
- Instagram: https://www.instagram.com/gdgc.vnrvjiet

## Quick Start

1. Make your Google Sheet public
2. Copy Sheet ID from URL  
3. Get Gmail app password
4. Update configuration in script
5. Run `python gdgc_email_sender.py`
6. Test with option 1 first!

**That's it! No complex API setup needed.** 🚀