"""
GDGC Web Development Volunteer Recruitment - Email Sender
Sends assignment emails to candidates from Google Sheets
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import csv
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GDGCEmailSender:
    def __init__(self, sheet_id, sender_email, sender_password):
        """
        Initialize the email sender
        
        Args:
            sheet_id (str): Google Sheets ID containing emails in column A
            sender_email (str): Gmail address to send from
            sender_password (str): Gmail app password (not regular password)
        """
        self.sheet_id = sheet_id
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def get_emails_from_sheet(self):
        """Get email addresses from column A of the public Google Sheet"""
        try:
            # Use CSV export URL for public sheets
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv&gid=0"
            
            logger.info(f"🔄 Fetching emails from public sheet...")
            logger.info(f"URL: {csv_url}")
            
            response = requests.get(csv_url)
            response.raise_for_status()
            
            # Parse CSV content
            content = response.content.decode('utf-8')
            csv_reader = csv.reader(content.splitlines())
            
            # Get first column (column A) from all rows
            emails_raw = []
            for row in csv_reader:
                if row and len(row) > 0:  # If row is not empty and has at least one column
                    emails_raw.append(row[0])  # First column (Column A)
            
            # Filter valid email addresses
            emails = [email.strip() for email in emails_raw if email and '@' in email and email.strip()]
            
            logger.info(f"Found {len(emails)} valid email addresses")
            logger.info(f"Emails: {emails}")
            return emails
            
        except Exception as e:
            logger.error(f"❌ Error reading emails from sheet: {e}")
            return []
    
    def create_assignment_email_html(self):
        """Create the HTML email content for the assignment"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            color: #2d3748; 
            margin: 0; 
            padding: 0; 
            background: #f7f7f7;
        }
        
        .email-wrapper {
            background: #f7f7f7;
            padding: 20px 0;
        }
        
        .container { 
            max-width: 680px; 
            margin: 0 auto; 
            background: #ffffff; 
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border: 1px solid #e2e2e2;
        }
        
        .header { 
            padding: 0;
            text-align: center; 
        }
        
        .banner-image {
            width: 100%;
            height: auto;
            display: block;
            max-height: 250px;
        }
        
        .content { 
            padding: 40px 35px; 
            background: #ffffff;
        }
        
        .greeting {
            font-size: 18px;
            margin-bottom: 20px;
            color: #2d3748;
            font-weight: 600;
        }
        
        .intro-text {
            font-size: 16px;
            margin-bottom: 30px;
            color: #4a5568;
            line-height: 1.7;
            font-weight: 400;
        }
        
        .assignment-doc-box {
            background: #f8f9fa;
            border: 2px solid #4299e1;
            border-radius: 8px;
            padding: 35px;
            margin: 30px 0;
            text-align: center;
        }
        
        .assignment-doc-box h3 {
            color: #2d3748;
            margin: 0 0 20px 0;
            font-size: 22px;
            font-weight: 700;
        }
        
        .assignment-doc-box p {
            color: #4a5568;
            font-weight: 400;
            margin-bottom: 25px;
            line-height: 1.6;
            font-size: 16px;
        }
        
        .doc-link-button {
            display: inline-block;
            background: #4299e1;
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
            margin: 0 10px 10px 0;
        }
        
        .doc-link-button:hover {
            background: #3182ce;
        }
        
        .submission-form-box {
            background: #f0fff4;
            border: 2px solid #48bb78;
            border-radius: 8px;
            padding: 35px;
            margin: 30px 0;
            text-align: center;
        }
        
        .submission-form-box h3 {
            color: #2d5016;
            margin: 0 0 20px 0;
            font-size: 22px;
            font-weight: 700;
        }
        
        .submission-form-box p {
            color: #38a169;
            font-weight: 500;
            margin-bottom: 25px;
            line-height: 1.6;
            font-size: 16px;
        }
        
        .deadline-box {
            background: #fff5f5;
            border: 2px solid #fc8181;
            border-radius: 8px;
            padding: 28px;
            margin: 25px 0;
            text-align: center;
        }
        
        .deadline-box h4 {
            color: #e53e3e;
            margin: 0 0 15px 0;
            font-size: 18px;
            font-weight: 600;
        }
        
        .deadline-box p {
            color: #4a5568;
            font-weight: 400;
            margin: 8px 0;
            line-height: 1.6;
        }
        
        .deadline-box strong {
            color: #e53e3e;
            font-weight: 600;
        }
        
        .closing-text {
            background: #f0fff4;
            padding: 28px;
            border-radius: 8px;
            border-left: 4px solid #48bb78;
            margin: 30px 0;
            color: #38a169;
            font-weight: 500;
            text-align: center;
            line-height: 1.6;
        }
        
        .contact-info {
            text-align: center;
            margin: 30px 0;
            padding: 24px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e2e2e2;
        }
        
        .contact-info p {
            color: #4a5568;
            font-weight: 400;
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .contact-info a {
            color: #4299e1;
            text-decoration: none;
            font-weight: 600;
        }
        
        .contact-info a:hover {
            text-decoration: underline;
        }
        
        .footer { 
            background: #2d3748;
            color: white;
            padding: 35px; 
            text-align: center; 
        }
        
        .footer p { 
            margin: 8px 0; 
            font-size: 14px; 
            font-weight: 400;
            color: #a0aec0;
        }
        
        .footer .team-name {
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
        }
        
        .social-section {
            margin: 20px 0 15px 0;
            text-align: center;
        }
        
        .social-text {
            color: #cbd5e1;
            font-size: 14px;
            margin-bottom: 15px;
            font-weight: 400;
        }
        
        .social-icons {
            display: inline-block;
            text-align: center;
        }
        
        .social-icon {
            display: inline-block;
            margin: 0 15px;
            text-decoration: none;
            color: #cbd5e1;
        }
        
        .social-icon img {
            width: 24px;
            height: 24px;
            vertical-align: middle;
        }
        
        .social-icon:hover {
            color: #ffffff;
        }
        
        .divider {
            height: 1px;
            background: #e2e2e2;
            margin: 30px 0;
        }
        
        /* Mobile responsive - simplified */
        @media only screen and (max-width: 600px) {
            .email-wrapper {
                padding: 10px;
            }
            
            .container { 
                margin: 0;
                border-radius: 6px;
            }
            
            .content { 
                padding: 25px 20px; 
            }
            
            .assignment-doc-box,
            .submission-form-box {
                padding: 25px 20px;
                margin: 20px 0;
            }
            
            .doc-link-button {
                padding: 12px 24px;
                font-size: 14px;
                display: block;
                margin: 10px 0;
            }
            
            .deadline-box {
                padding: 20px;
                margin: 20px 0;
            }
            
            .footer {
                padding: 25px 20px;
            }
            
            .social-icon {
                margin: 0 12px;
            }
        }
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="container">
            <div class="header">
                <img src="https://drive.google.com/uc?export=view&id=1N7dunWTAFT5h8eVxK0K1sTR30ky_YWFg" alt="GDGC Banner" class="banner-image">
            </div>
            
            <div class="content">
                <p class="greeting">Dear Candidate,</p>
                <p class="intro-text">Thank you for showing interest in volunteering with GDGC. As part of the first round of the selection process, we have designed a hands-on assignment to assess your technical skills and creativity.</p>
                
                <div class="divider"></div>
                
                <div class="assignment-doc-box">
                    <h3>📋 Assignment Details</h3>
                    <p>Please check the document below for complete assignment details, requirements, and submission guidelines.</p>
                    <a href="https://docs.google.com/document/d/1srQpzDvOO6T3-FQ-BzSpTbs-72H-5MvK5SwQ8TSXySI/edit?tab=t.0" class="doc-link-button">
                        📄 View Assignment Document
                    </a>
                </div>
                
                <div class="submission-form-box">
                    <h3>📝 Assignment Submission</h3>
                    <p>Once you complete the assignment, submit your project using the form below:</p>
                    <a href="https://docs.google.com/forms/d/e/1FAIpQLSe-V4n86_n-AM2JGU8T0x3QJ1pm7Di6DVNZ-mMJYgLtd3ceMA/viewform" class="doc-link-button" style="background: #48bb78;">
                        📤 Submit Assignment
                    </a>
                </div>
                
                <div class="deadline-box">
                    <h4>📅 Important Note</h4>
                    <p>Please refer to the assignment document for <strong>submission deadline</strong> and other important details.</p>
                    <p>Candidates whose submissions meet the requirements will be shortlisted for the <strong>second round (technical interview)</strong>.</p>
                </div>
                
                <div class="closing-text">
                    <p><strong>We're excited to see your innovative ideas and technical approach. Best of luck with your submission! 🚀</strong></p>
                </div>
                
                <div class="contact-info">
                    <p><strong>📞 For any queries or clarifications, contact:</strong></p>
                    <p>Sai Ritesh: <a href="tel:+918639154193">8639154193</a></p>
                    <p>Hasnika: <a href="tel:+917981367685">7981367685</a></p>
                </div>
            </div>
            
            <div class="footer">
                <p class="team-name">GDGC Team</p>
                <p><strong>Google Developer Groups on Campus - VNRVJIET</strong></p>
                
                <div class="social-section">
                    <p class="social-text">Follow us on social media</p>
                    <div class="social-icons">
                        <a href="https://www.linkedin.com/company/gdsc-vnrvjiet/" class="social-icon" target="_blank">
                            LinkedIn
                        </a>
                        <a href="https://www.instagram.com/gdgc.vnrvjiet" class="social-icon" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width:24px;height:24px;vertical-align:middle;">
                        </a>
                    </div>
                </div>
                
                <p><em>This is an automated email. Please keep this for your records.</em></p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def send_email(self, recipient_email, subject, html_body):
        """Send an email to a single recipient"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Attach HTML content
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email to {recipient_email}: {e}")
            return False
    
    def send_assignment_emails(self):
        """Send assignment emails to all candidates in the sheet"""
        logger.info("🚀 Starting GDGC assignment email sending process...")
        
        # Get emails from sheet (no authentication needed for public sheets)
        emails = self.get_emails_from_sheet()
        if not emails:
            return {"success": False, "error": "No valid emails found in sheet"}
        
        # Prepare email content
        subject = "GDGC Web Development Volunteer Recruitment – First Round Assignment"
        html_body = self.create_assignment_email_html()
        
        # Send emails
        success_count = 0
        failure_count = 0
        results = []
        
        for i, email in enumerate(emails, 1):
            logger.info(f"📧 Sending email {i}/{len(emails)} to: {email}")
            
            success = self.send_email(email, subject, html_body)
            
            if success:
                success_count += 1
                results.append({"email": email, "status": "success"})
                logger.info(f"✅ Email sent successfully to: {email}")
            else:
                failure_count += 1
                results.append({"email": email, "status": "failed"})
            
            # Add delay to avoid rate limits
            if i < len(emails):  # Don't delay after the last email
                time.sleep(1)  # 1 second delay between emails
        
        # Summary
        logger.info(f"\n📊 Email sending completed:")
        logger.info(f"✅ Success: {success_count}")
        logger.info(f"❌ Failed: {failure_count}")
        logger.info(f"📧 Total: {len(emails)}")
        
        return {
            "success": True,
            "total_emails": len(emails),
            "success_count": success_count,
            "failure_count": failure_count,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def send_test_email(self, test_email):
        """Send a test email to verify the setup"""
        logger.info(f"🧪 Sending test email to: {test_email}")
        
        subject = "GDGC Web Development Volunteer Recruitment – First Round Assignment (TEST)"
        html_body = self.create_assignment_email_html()
        
        success = self.send_email(test_email, subject, html_body)
        
        if success:
            logger.info(f"✅ Test email sent successfully to: {test_email}")
            return {"success": True, "message": f"Test email sent to {test_email}"}
        else:
            return {"success": False, "message": f"Failed to send test email to {test_email}"}


def main():
    """Main function to run the email sender"""
    
    # Configuration - UPDATE THESE VALUES
    SHEET_ID = "1Pf9ROUKO3gqoyB35TnPIM6I7EY8kR_qsaH5hCwZFvr8"  # ✅ Already correct
    SENDER_EMAIL = "laksita2004@gmail.com"  # ✅ Updated with your email
    SENDER_PASSWORD = "ndwn xfcs xwqg zfkq"  # ❌ You need to replace this

    # Create email sender instance
    sender = GDGCEmailSender(SHEET_ID, SENDER_EMAIL, SENDER_PASSWORD)
    
    # Option 1: Send test email first
    print("Choose an option:")
    print("1. Send test email")
    print("2. Send to all emails in sheet")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        test_email = input("Enter test email address: ").strip()
        result = sender.send_test_email(test_email)
        print(f"Result: {result}")
        
    elif choice == "2":
        confirm = input("Are you sure you want to send emails to ALL addresses in the sheet? (yes/no): ").strip().lower()
        if confirm == "yes":
            result = sender.send_assignment_emails()
            print(f"Final Result: {result}")
        else:
            print("❌ Email sending cancelled")
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()