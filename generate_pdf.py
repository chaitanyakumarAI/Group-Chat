import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_report():
    pdf_path = os.path.join(os.path.dirname(__file__), "Group_Chat_Architecture_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1e1b4b")      # Deep Indigo
    SECONDARY = colors.HexColor("#4f46e5")    # Vibrant Indigo
    ACCENT = colors.HexColor("#0284c7")       # Cyan/Blue Accent
    DARK_TEXT = colors.HexColor("#0f172a")    # Slate 900
    MUTED_TEXT = colors.HexColor("#475569")   # Slate 600
    BG_LIGHT = colors.HexColor("#f8fafc")     # Light Slate Background

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=MUTED_TEXT,
        spaceAfter=12
    )

    heading1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=BG_LIGHT,
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    highlight_box_style = ParagraphStyle(
        'Highlight_Custom',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0369a1")
    )

    story = []

    # Document Header
    story.append(Paragraph("Real-Time Group Chat Application", title_style))
    story.append(Paragraph("Computer System Design (CSD) — Assignment 4 | Technical & Deployment Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=12))

    # General Information Table
    info_data = [
        [Paragraph("<b>Course:</b> Computer System Design (CSD)", body_style), Paragraph("<b>Assignment:</b> Assignment 4", body_style)],
        [Paragraph("<b>Host SSH Machine:</b> student@10.1.75.51 (Port 2237)", body_style), Paragraph("<b>Internal Port:</b> 5000", body_style)],
        [Paragraph("<b>Official Testing Public URL:</b> <font color='#0284c7'><b>http://10.1.75.51:5237/</b></font>", highlight_box_style), Paragraph("<b>Tech Stack:</b> Flask, Flask-SocketIO, SQLite, AES-256-GCM, Ed25519", body_style)]
    ]
    t_info = Table(info_data, colWidths=[270, 260])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_info)
    story.append(Spacer(1, 10))

    # Section 1: Executive Summary & Network Routing
    story.append(Paragraph("1. Executive Summary & Lab Network Mapping", heading1_style))
    exec_summary_text = (
        "This project implements a multi-user, real-time Group Chat Application for <b>Computer System Design (CSD) Assignment 4</b>. "
        "Built using WebSockets (Flask-SocketIO) and SQLite persistence, it includes advanced security layers (AES-256-GCM confidentiality and Ed25519 digital signatures). "
        "The backend server runs on the allotted SSH laboratory machine (<code>student@10.1.75.51</code>).<br/><br/>"
        "<b>Lab Network & Port Forwarding Mapping:</b><br/>"
        "The Flask backend process binds internally to port <code>5000</code>. The laboratory network NAT router maps SSH port <code>2237</code> "
        "to external web port <code>5237</code>. Therefore, the official public URL for TA evaluation across all 4 student clients is: "
        "<font color='#0284c7'><b>http://10.1.75.51:5237/</b></font>."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 8))

    # Section 2: Laboratory Team Information & SSH Server Allocation
    story.append(Paragraph("2. Group Members & SSH Server Allotment", heading1_style))
    team_data = [
        ["Role / Designation", "Student Name", "Roll Number", "SSH Connection Server", "Access URL"],
        ["Group Head (Host)", "Ranga Chandra Naga Venkata Chaitanya Kumar", "12341740", "ssh -p 2237 student@10.1.75.51", "http://10.1.75.51:5237/"],
        ["Member 2", "Bhukya Raju", "12340520", "ssh -p 2238 student@10.1.75.51", "http://10.1.75.51:5237/"],
        ["Member 3", "V.G.N. Harshitha", "12342310", "ssh -p 2239 student@10.1.75.51", "http://10.1.75.51:5237/"],
        ["Member 4", "Maloth Madhu", "12341370", "ssh -p 2240 student@10.1.75.51", "http://10.1.75.51:5237/"]
    ]
    t_team = Table(team_data, colWidths=[90, 160, 65, 125, 90])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_team)
    story.append(Spacer(1, 10))

    # Section 3: Feature Verification Matrix
    story.append(Paragraph("3. Feature Coverage & Requirement Verification", heading1_style))
    req_data = [
        ["Requirement / Feature", "Implementation Mechanism", "Status"],
        ["Real-Time Message Broadcast", "Bi-directional WebSocket event broadcasting via Flask-SocketIO", "VERIFIED"],
        ["User Join/Leave Alerts", "Automatic broadcast of user arrival/departure pills to room", "VERIFIED"],
        ["User Identification", "Unique username validation & dynamic gradient avatar generation", "VERIFIED"],
        ["Client Disconnection Cleanup", "Server socket connection monitoring & cleanup on tab close", "VERIFIED"],
        ["SQLite Persistence", "All messages saved in chat.db; auto-loaded upon joining chat", "VERIFIED"],
        ["Confidentiality (AES-256-GCM)", "Payload encrypted with room key prior to database insertion", "VERIFIED"],
        ["Authenticity (Ed25519)", "Cryptographic digital signature per user stored & verified", "VERIFIED"],
        ["Public TA Access URL", "Mapped external port forwarded to http://10.1.75.51:5237/", "VERIFIED"]
    ]
    t_req = Table(req_data, colWidths=[140, 310, 80])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('TEXTCOLOR', (2,1), (2,-1), colors.HexColor("#16a34a")),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
        ('ALIGN', (2,0), (2,-1), 'CENTER')
    ]))
    story.append(t_req)
    story.append(Spacer(1, 10))

    # Section 4: System Architecture Workflow
    story.append(Paragraph("4. System Architecture Workflow", heading1_style))
    arch_box = (
        "<b>End-to-End System Flow:</b><br/>"
        "1. <b>Client Frontend:</b> Users connect via Socket.IO client interface over <code>http://10.1.75.51:5237/</code>.<br/>"
        "2. <b>Port Forwarding:</b> Public port <code>5237</code> routes connection to internal Flask port <code>5000</code>.<br/>"
        "3. <b>WebSocket Handler (Flask-SocketIO):</b> Event-driven handling of join, disconnect, typing, and message events.<br/>"
        "4. <b>Cryptographic Security:</b> AES-256-GCM encrypts plaintext; Ed25519 private key signs sender message.<br/>"
        "5. <b>SQLite Database Persistence:</b> Writes record into <code>chat.db</code> (tables: <code>messages</code>, <code>signing_keys</code>)."
    )
    story.append(Paragraph(arch_box, code_style))
    story.append(Spacer(1, 8))

    # Section 5: Database Schema & Query Guide
    story.append(Paragraph("5. Database Verification Commands (SSH Host)", heading1_style))
    db_text = (
        "<b>To inspect encrypted messages and signatures in SQLite:</b><br/>"
        "<code>sqlite3 ~/chat_app/chat.db \"SELECT id, sender, ciphertext, signature, timestamp FROM messages;\"</code><br/>"
        "<b>To verify public Ed25519 user signing keys:</b><br/>"
        "<code>sqlite3 ~/chat_app/chat.db \"SELECT username, public_key FROM signing_keys;\"</code>"
    )
    story.append(Paragraph(db_text, body_style))
    story.append(Spacer(1, 10))

    # Section 6: Submission Links
    story.append(Paragraph("6. Official Submission Details", heading1_style))
    links_text = (
        "• <b>GitHub Repository:</b> <font color='#0284c7'><u>https://github.com/chaitanyakumarAI/Group-Chat</u></font><br/>"
        "• <b>Live Application URL (For TA Testing):</b> <font color='#0284c7'><b>http://10.1.75.51:5237/</b></font><br/>"
        "• <b>Host SSH Server Command:</b> <code>ssh -p 2237 student@10.1.75.51</code><br/>"
        "• <b>Daemon Process Command:</b> <code>nohup python3 server.py &gt; server.log 2&gt;&amp;1 &amp;</code>"
    )
    story.append(Paragraph(links_text, body_style))

    doc.build(story)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    create_report()
