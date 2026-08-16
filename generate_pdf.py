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
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=MUTED_TEXT,
        spaceAfter=15
    )

    heading1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=SECONDARY,
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT,
        spaceAfter=8
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
        spaceBefore=6,
        spaceAfter=8
    )

    highlight_box_style = ParagraphStyle(
        'Highlight_Custom',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0369a1")
    )

    story = []

    # Document Header
    story.append(Paragraph("Real-Time Group Chat Application", title_style))
    story.append(Paragraph("System Architecture, Security Design & Lab Deployment Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=15))

    # General Information Table
    info_data = [
        [Paragraph("<b>Course Assignment:</b> Real-Time Group Chat", body_style), Paragraph("<b>Target Environment:</b> Laboratory SSH Server", body_style)],
        [Paragraph("<b>Host Machine:</b> student@10.1.75.51 (Port 2237)", body_style), Paragraph("<b>Internal Server Port:</b> 5000", body_style)],
        [Paragraph("<b>External Public URL:</b> <font color='#0284c7'><b>http://10.1.75.51:5237/</b></font>", highlight_box_style), Paragraph("<b>Tech Stack:</b> Flask, Flask-SocketIO, SQLite, AES-256-GCM, Ed25519", body_style)]
    ]
    t_info = Table(info_data, colWidths=[260, 270])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_info)
    story.append(Spacer(1, 14))

    # Section 1: Executive Summary & URL Mapping
    story.append(Paragraph("1. Executive Summary & Lab Network Mapping", heading1_style))
    exec_summary_text = (
        "This project implements a multi-user, real-time Group Chat Application using WebSockets (Flask-SocketIO) "
        "and SQLite persistence with end-to-end security enhancements (AES-256-GCM confidentiality and Ed25519 digital signatures). "
        "The application backend runs on the assigned SSH laboratory host (<code>student@10.1.75.51</code>). "
        "<br/><br/>"
        "<b>Important Port Mapping Note for Evaluation:</b><br/>"
        "While the Flask backend process binds internally to port <code>5000</code>, the laboratory NAT router maps SSH port <code>2237</code> "
        "to external web port <code>5237</code>. Therefore, the official testing URL accessible to all lab clients and TAs is: "
        "<font color='#0284c7'><b>http://10.1.75.51:5237/</b></font>."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 10))

    # Section 2: Laboratory Team & Server Allotment
    story.append(Paragraph("2. Group Members & SSH Machine Allocation", heading1_style))
    team_data = [
        ["Role", "Student Member", "SSH Server Connection", "Mapped Public Web Port"],
        ["Group Head / Host", "Member 1 (Host Server)", "ssh -p 2237 student@10.1.75.51", "http://10.1.75.51:5237/"],
        ["Client Member 2", "Member 2", "ssh -p 2238 student@10.1.75.51", "Accesses http://10.1.75.51:5237/"],
        ["Client Member 3", "Member 3", "ssh -p 2239 student@10.1.75.51", "Accesses http://10.1.75.51:5237/"],
        ["Client Member 4", "Member 4", "ssh -p 2240 student@10.1.75.51", "Accesses http://10.1.75.51:5237/"]
    ]
    t_team = Table(team_data, colWidths=[110, 120, 180, 120])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT')
    ]))
    story.append(t_team)
    story.append(Spacer(1, 12))

    # Section 3: Key Features & Verification Matrix
    story.append(Paragraph("3. Feature Coverage & Verification Matrix", heading1_style))
    req_data = [
        ["Requirement / Feature", "Implementation Details", "Verification Result"],
        ["Real-Time Messaging", "Bi-directional WebSocket event broadcasting via Flask-SocketIO", "PASSED"],
        ["Join/Leave Notifications", "Automatic broadcast of user arrival/departure pills to room", "PASSED"],
        ["User Identification", "Unique username enforcement & dynamic avatar generation", "PASSED"],
        ["Graceful Disconnections", "Server socket cleanup & broadcast on browser tab close", "PASSED"],
        ["SQLite Message Persistence", "Stored in chat.db; auto-loaded upon room entry/reconnect", "PASSED"],
        ["Confidentiality (AES-256-GCM)", "Payloads encrypted with room key before database insertion", "PASSED"],
        ["Authenticity (Ed25519)", "Cryptographic digital signature per user stored & verified", "PASSED"],
        ["Public Access URL", "External port forwarding mapped to http://10.1.75.51:5237/", "PASSED"]
    ]
    t_req = Table(req_data, colWidths=[150, 280, 100])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('TEXTCOLOR', (2,1), (2,-1), colors.HexColor("#16a34a")),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold')
    ]))
    story.append(t_req)
    story.append(Spacer(1, 14))

    # Section 4: System Architecture Diagram (Textual Representation)
    story.append(Paragraph("4. System Architecture Overview", heading1_style))
    arch_box = (
        "<b>Architectural Workflow:</b><br/>"
        "1. <b>Client Frontend:</b> Browser connects via Socket.IO client over <code>http://10.1.75.51:5237/</code>.<br/>"
        "2. <b>Port Forwarding:</b> External port <code>5237</code> routes incoming traffic to internal Flask port <code>5000</code>.<br/>"
        "3. <b>WebSocket Handler (Flask-SocketIO):</b> Manages connection lifecycle (join, leave, message, typing).<br/>"
        "4. <b>Security Subsystem:</b> Encrypts message body using AES-256-GCM and signs plaintext using sender's Ed25519 key.<br/>"
        "5. <b>Persistence Layer (SQLite):</b> Writes record to <code>chat.db</code> (tables: <code>messages</code>, <code>signing_keys</code>)."
    )
    story.append(Paragraph(arch_box, code_style))
    story.append(Spacer(1, 10))

    # Section 5: Database Schema & Inspection
    story.append(Paragraph("5. Database Schema & SQLite Inspection Guide", heading1_style))
    db_text = (
        "Messages are persisted in <code>chat.db</code> under the following schema:<br/>"
        "<code>CREATE TABLE messages (id INTEGER PRIMARY KEY, room_id TEXT, sender TEXT, ciphertext TEXT, nonce TEXT, signature TEXT, timestamp TEXT);</code><br/><br/>"
        "<b>To inspect stored messages and signatures via SSH:</b><br/>"
        "<code>sqlite3 ~/chat_app/chat.db \"SELECT id, sender, ciphertext, signature, timestamp FROM messages;\"</code>"
    )
    story.append(Paragraph(db_text, body_style))
    story.append(Spacer(1, 14))

    # Section 6: GitHub & Deployment Links
    story.append(Paragraph("6. Submission Links & Verification Summary", heading1_style))
    links_text = (
        "• <b>GitHub Source Code Repository:</b> <font color='#0284c7'><u>https://github.com/chaitanyakumarAI/Group-Chat</u></font><br/>"
        "• <b>Live Application URL (For TA Testing):</b> <font color='#0284c7'><b>http://10.1.75.51:5237/</b></font><br/>"
        "• <b>SSH Server Host Command:</b> <code>ssh -p 2237 student@10.1.75.51</code><br/>"
        "• <b>Background Daemon Command:</b> <code>nohup python3 server.py &gt; server.log 2&gt;&amp;1 &amp;</code>"
    )
    story.append(Paragraph(links_text, body_style))

    doc.build(story)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    create_report()
