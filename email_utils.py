"""
Email utilities for sending notifications
"""

import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import COMPANY_NAME
from reports import generate_inspection_report

def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, 
               subject, body_html, body_text, attachment_data=None, attachment_name=None):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body
        part1 = MIMEText(body_text, 'plain')
        part2 = MIMEText(body_html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Add attachment if provided
        if attachment_data and attachment_name:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {attachment_name}')
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def generate_customer_warning_email(customer_id, risk_level, theft_probability):
    """Generate HTML email for customer warning (Medium risk, no theft)"""
    html_content = f"""
    <html>
      <body style="font-family: 'DM Sans', Arial, sans-serif; line-height: 1.6; color: #332F3A; background-color: #F4F1FA; margin: 0; padding: 24px;">
        <div style="max-width: 600px; margin: 0 auto; padding: 32px; background-color: #ffffff; border-radius: 32px; box-shadow: 16px 16px 32px rgba(160,150,180,0.20), -10px -10px 24px rgba(255,255,255,0.9);">
          <h2 style="font-family: 'Nunito', Arial, sans-serif; color: #7C3AED; margin-top: 0;">⚠️ Electricity Consumption Warning</h2>

          <p>Dear Customer,</p>

          <p>This is an automated notification regarding your electricity consumption pattern for <strong>Customer ID: {customer_id}</strong>.</p>

          <div style="background-color: #FFFBEB; border-left: 6px solid #F59E0B; border-radius: 20px; padding: 18px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #B45309; font-family: 'Nunito', Arial, sans-serif;">Notice</h3>
            <p style="margin-bottom: 0;">
              Our monitoring system has detected <strong>{risk_level} risk</strong> patterns in your electricity consumption.
              Theft probability is at <strong>{theft_probability}</strong>.
            </p>
          </div>
          
          <p><strong>What this means:</strong></p>
          <ul>
            <li>Your consumption pattern shows some anomalies</li>
            <li>This may indicate irregularities in your electricity usage</li>
            <li>Please ensure your meter and electrical connections are in proper condition</li>
          </ul>
          
          <p><strong>Recommended Actions:</strong></p>
          <ul>
            <li>Review your electricity usage patterns</li>
            <li>Ensure all electrical connections are legal and properly maintained</li>
            <li>Contact our customer service if you have any concerns</li>
          </ul>
          
          <p style="margin-top: 30px;">
            Best regards,<br>
            <strong>{COMPANY_NAME}</strong><br>
            Automated Monitoring System
          </p>
          
          <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
          <p style="font-size: 12px; color: #666;">
            This is an automated email. Please do not reply to this message.<br>
            Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
          </p>
        </div>
      </body>
    </html>
    """
    
    text_content = f"""
ELECTRICITY CONSUMPTION WARNING

Dear Customer,

This is an automated notification regarding your electricity consumption pattern for Customer ID: {customer_id}.

NOTICE:
Our monitoring system has detected {risk_level} risk patterns in your electricity consumption.
Theft probability is at {theft_probability}.

What this means:
- Your consumption pattern shows some anomalies
- This may indicate irregularities in your electricity usage
- Please ensure your meter and electrical connections are in proper condition

Recommended Actions:
- Review your electricity usage patterns
- Ensure all electrical connections are legal and properly maintained
- Contact our customer service if you have any concerns

Best regards,
{COMPANY_NAME}
Automated Monitoring System

Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return html_content, text_content

def generate_inspection_team_email(customer_id, result_series, data_series):
    """Generate HTML email for inspection team (High/Medium risk with theft detected)"""
    html_content = f"""
    <html>
      <body style="font-family: 'DM Sans', Arial, sans-serif; line-height: 1.6; color: #332F3A; background-color: #F4F1FA; margin: 0; padding: 24px;">
        <div style="max-width: 700px; margin: 0 auto; padding: 32px; background-color: #ffffff; border-radius: 32px; box-shadow: 16px 16px 32px rgba(160,150,180,0.20), -10px -10px 24px rgba(255,255,255,0.9);">
          <h2 style="font-family: 'Nunito', Arial, sans-serif; color: #EF4444; margin-top: 0;">🚨 URGENT: Theft Detection Alert</h2>

          <div style="background-color: #FEF2F2; border-left: 6px solid #EF4444; border-radius: 20px; padding: 18px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #B91C1C; font-family: 'Nunito', Arial, sans-serif;">Action Required</h3>
            <p style="margin-bottom: 0;">
              <strong>Customer ID:</strong> {customer_id}<br>
              <strong>Risk Level:</strong> {result_series['Risk_Level']}<br>
              <strong>Theft Probability:</strong> {result_series['Theft_Probability']}<br>
              <strong>Risk Score:</strong> {result_series.get('Risk_Score', 'N/A')}
            </p>
          </div>
          
          <h3 style="font-family: 'Nunito', Arial, sans-serif; color: #332F3A;">Detection Summary</h3>
          <table style="width: 100%; border-collapse: collapse; margin: 15px 0; border-radius: 20px; overflow: hidden;">
            <tr style="background-color: #F4F1FA;">
              <th style="padding: 12px; text-align: left; border: 1px solid #EFEBF5; color: #7C3AED; font-family: 'Nunito', Arial, sans-serif;">Metric</th>
              <th style="padding: 12px; text-align: left; border: 1px solid #EFEBF5; color: #7C3AED; font-family: 'Nunito', Arial, sans-serif;">Value</th>
            </tr>
            <tr>
              <td style="padding: 12px; border: 1px solid #EFEBF5;"><strong>Prediction Result</strong></td>
              <td style="padding: 12px; border: 1px solid #EFEBF5;">{result_series['Prediction']} (Theft Detected)</td>
            </tr>
            <tr>
              <td style="padding: 12px; border: 1px solid #EFEBF5;"><strong>Risk Level</strong></td>
              <td style="padding: 12px; border: 1px solid #EFEBF5;">{result_series['Risk_Level']}</td>
            </tr>
            <tr>
              <td style="padding: 12px; border: 1px solid #EFEBF5;"><strong>Theft Description</strong></td>
              <td style="padding: 12px; border: 1px solid #EFEBF5;">{result_series['Theft_Description']}</td>
            </tr>
            <tr>
              <td style="padding: 12px; border: 1px solid #EFEBF5;"><strong>Recommended Action</strong></td>
              <td style="padding: 12px; border: 1px solid #EFEBF5;">{result_series['Next_Action']}</td>
            </tr>
          </table>

          <h3 style="font-family: 'Nunito', Arial, sans-serif; color: #332F3A;">Key Anomalous Features</h3>
          <ul>
            <li>Zero Consumption Days: {data_series.get('zero_consumption_days', 'N/A')}</li>
            <li>Std Dev of Consumption: {data_series.get('std_consumption', 'N/A')}</li>
            <li>Max to Mean Ratio: {data_series.get('max_to_mean_ratio', 'N/A')}</li>
            <li>Avg Consumption: {data_series.get('avg_consumption', 'N/A')}</li>
          </ul>
          
          <div style="background-color: #FFFBEB; border-left: 6px solid #F59E0B; border-radius: 20px; padding: 18px; margin: 20px 0;">
            <h3 style="margin-top: 0; font-family: 'Nunito', Arial, sans-serif; color: #B45309;">Inspection Instructions</h3>
            <ol>
              <li>Conduct immediate on-site inspection of the premises</li>
              <li>Check meter physical condition and wiring integrity</li>
              <li>Document all findings with photographs</li>
              <li>Take legal action if theft is confirmed</li>
            </ol>
          </div>
          
          <p style="margin-top: 30px;">
            A detailed report is attached to this email.<br><br>
            Best regards,<br>
            <strong>{COMPANY_NAME} Automated Detection System</strong><br>
            Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
          </p>
        </div>
      </body>
    </html>
    """
    
    report_text = generate_inspection_report(customer_id, result_series, data_series)
    return html_content, report_text

