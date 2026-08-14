"""
Generate Submission PDF Report for Group Chat Lab Tutorial (With exact SSH Server credentials)
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def build_pdf():
    pdf_filename = "E:\\CSD\\chat_app\\Group_Chat_Architecture_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E1B4B'),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4F46E5'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    bold_body_style = ParagraphStyle(
        'BoldBody_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("LABORATORY TUTORIAL: REAL-TIME GROUP CHAT", title_style))
    story.append(Paragraph("Multi-User WebSocket Architecture & SSH Server Deployment Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#6366F1'), spaceAfter=10))

    # Summary Box
    summary_data = [
        [Paragraph("<b>Target Audience / TA Review:</b>", body_style), Paragraph("Multi-User Laboratory WebSocket Testing", body_style)],
        [Paragraph("<b>Group SSH Servers:</b>", body_style), Paragraph("Host (P1): <code>ssh -p 2237 student@10.1.75.51</code><br/>Clients: P2 (2238), P3 (2239), P4 (2240)", body_style)],
        [Paragraph("<b>Group Head Submission:</b>", body_style), Paragraph("4 Students Group Submission", body_style)],
        [Paragraph("<b>Group Registration Link:</b>", body_style), Paragraph("<font color='#4F46E5'><u>https://forms.gle/VHHzfSLmPhZQZ9rLA</u></font>", body_style)],
        [Paragraph("<b>Backend Tech Stack:</b>", body_style), Paragraph("Python 3, Flask, Flask-SocketIO (WebSockets / Engine.IO)", body_style)],
        [Paragraph("<b>TA Client Testing URL:</b>", bold_body_style), Paragraph("<font color='#059669'><b>http://10.1.75.51:5000</b></font>", bold_body_style)],
    ]
    t_summary = Table(summary_data, colWidths=[150, 390])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 8))

    # 1. System Architecture Diagram
    story.append(Paragraph("1. SSH Cluster System Architecture", h1_style))
    diagram_text = """
                       +-----------------------------------+
                       |    Student 1 SSH Server (Host)    |
                       |    (ssh -p 2237 student@10.1.75.51)|
                       |  (Flask + Flask-SocketIO Core)   |
                       |         Public IP / Port:         |
                       |      http://10.1.75.51:5000      |
                       +-----------------+-----------------+
                                         |
             +---------------------------+---------------------------+
             |                           |                           |
             v                           v                           v
  +--------------------+      +--------------------+      +--------------------+
  |   Student 2 SSH    |      |   Student 3 SSH    |      |   Student 4 SSH    |
  | (-p 2238 Client)   |      | (-p 2239 Client)   |      | (-p 2240 Client)   |
  | (Browser Session)  |      | (Browser Session)  |      | (Browser Session)  |
  +--------------------+      +--------------------+      +--------------------+
"""
    code_style_light = ParagraphStyle('CodeLight', parent=code_style, textColor=colors.HexColor('#38BDF8'))
    t_diagram = Table([[Preformatted(diagram_text, code_style_light)]], colWidths=[540])
    t_diagram.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#334155')),
    ]))
    story.append(t_diagram)
    story.append(Spacer(1, 6))

    # 2. Requirements Matrix
    story.append(Paragraph("2. Requirements Verification Matrix", h1_style))
    req_headers = [Paragraph("<b>Requirement</b>", bold_body_style), Paragraph("<b>Implementation Details</b>", bold_body_style), Paragraph("<b>Status</b>", bold_body_style)]
    req_rows = [
        req_headers,
        [Paragraph("Real-time message broadcasting", body_style), Paragraph("Handled via socketio.emit('message', data, to='general'). Instant relay.", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("User join/leave notifications", body_style), Paragraph("Server emits user_joined and user_left events to all clients.", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("Usernames for participants", body_style), Paragraph("Enforces non-empty & unique usernames per active connection.", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("Graceful disconnection handling", body_style), Paragraph("@socketio.on('disconnect') removes sid and notifies remaining users.", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("4 Client Support", body_style), Paragraph("Verified across 4 SSH student clients (ports 2237-2240).", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
    ]
    t_req = Table(req_rows, colWidths=[150, 310, 80])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_req)
    story.append(Spacer(1, 8))

    # 3. SSH Commands Guide
    story.append(Paragraph("3. Deployment Commands for Host SSH (Port 2237)", h1_style))
    ssh_guide_text = """
1. Upload Source Code from local machine to Student 1 SSH host:
   scp -P 2237 -r E:\\CSD\\chat_app student@10.1.75.51:~/chat_app

2. SSH into Host Machine & Start Flask-SocketIO Server:
   ssh -p 2237 student@10.1.75.51
   cd ~/chat_app
   pip install -r requirements.txt
   nohup python3 server.py > server.log 2>&1 &

3. Testing URL for TAs and all 4 Students:
   http://10.1.75.51:5000
"""
    t_ssh = Table([[Preformatted(ssh_guide_text, code_style)]], colWidths=[540])
    t_ssh.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ssh)

    doc.build(story)
    print("PDF build successful:", pdf_filename)

if __name__ == "__main__":
    build_pdf()
