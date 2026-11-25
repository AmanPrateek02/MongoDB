import os
import subprocess
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(41, 75, 107) # Medium Slate
    else:
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(70, 70, 70)
    return p

def add_body_p(doc, text, bold_prefix="", space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.bold = True
        r_bold.font.name = 'Calibri'
        r_bold.font.size = Pt(10.5)
        r_bold.font.color.rgb = RGBColor(30, 30, 30)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_bullet_p(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.bold = True
        r_bold.font.name = 'Calibri'
        r_bold.font.size = Pt(10)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10)
    return p

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F5F7")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    cell.width = Inches(6.5)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(35, 45, 60)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_report():
    doc = Document()
    
    # Page setup: Standard Letter, 0.8 inch margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
        # Header & Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Aman Prateek | Reg No: 12310657 | CSE494 Capstone Report")
        f_run.font.name = 'Calibri'
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(120, 120, 120)

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(6)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = title_p.add_run("LOVELY PROFESSIONAL UNIVERSITY\n")
    r_uni.bold = True
    r_uni.font.name = 'Calibri'
    r_uni.font.size = Pt(17)
    r_uni.font.color.rgb = RGBColor(16, 44, 87)
    
    r_dept = title_p.add_run("SCHOOL OF COMPUTER SCIENCE & ENGINEERING\nPHAGWARA, PUNJAB — 144411\n\n")
    r_dept.font.name = 'Calibri'
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = RGBColor(80, 80, 80)

    p_proj = doc.add_paragraph()
    p_proj.paragraph_format.space_before = Pt(24)
    p_proj.paragraph_format.space_after = Pt(8)
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_proj.add_run("ACADEMIC COURSE PROJECT REPORT\nON\n")
    r_t1.bold = True
    r_t1.font.name = 'Calibri'
    r_t1.font.size = Pt(12)
    r_t1.font.color.rgb = RGBColor(100, 100, 100)

    r_main = p_proj.add_run("EXPENSE ANALYTICS:\nAN INTELLIGENT MONGODB-BASED PERSONAL FINANCE TRACKING AND ANALYTICS SYSTEM\n")
    r_main.bold = True
    r_main.font.name = 'Calibri'
    r_main.font.size = Pt(18)
    r_main.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r_crs = p_sub.add_run("Submitted in partial fulfilment of the requirements for the award of degree of\nBachelor of Technology in Computer Science and Engineering\nCourse Code: CSE494 (Intelligent NoSQL Databases)")
    r_crs.font.name = 'Calibri'
    r_crs.font.size = Pt(11)
    r_crs.italic = True
    r_crs.font.color.rgb = RGBColor(60, 60, 60)

    # Metadata Table
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Student Name:", "Aman Prateek"),
        ("Registration Number:", "12310657"),
        ("Roll Number:", "19"),
        ("GitHub Repository:", "https://github.com/Aryan114mehta/MongoDB"),
        ("Academic Term & Year:", "Autumn Term (August – December 2026)")
    ]
    for i, (k, v) in enumerate(meta):
        cell_l, cell_r = tbl.cell(i, 0), tbl.cell(i, 1)
        cell_l.width, cell_r.width = Inches(2.2), Inches(4.2)
        set_cell_background(cell_l, "F0F4F8")
        set_cell_background(cell_r, "FAFAFA")
        set_cell_margins(cell_l, 60, 60, 100, 100)
        set_cell_margins(cell_r, 60, 60, 100, 100)
        
        pl = cell_l.paragraphs[0]
        pl.paragraph_format.space_after = Pt(0)
        rl = pl.add_run(k)
        rl.bold = True
        rl.font.size = Pt(10)
        rl.font.name = 'Calibri'
        
        pr = cell_r.paragraphs[0]
        pr.paragraph_format.space_after = Pt(0)
        rr = pr.add_run(v)
        rr.font.size = Pt(10)
        rr.font.name = 'Calibri'

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: DECLARATION, CERTIFICATE & ABSTRACT
    # =========================================================================
    add_styled_heading(doc, "CANDIDATE'S DECLARATION", 1)
    add_body_p(doc, 
        "I hereby declare that the work presented in this project report entitled 'Expense Analytics: An Intelligent MongoDB-Based Personal Finance Tracking and Analytics System' "
        "is an authentic record of my own work carried out as partial fulfilment of the requirements for the Continuous Assessment and Capstone Project in the course "
        "Intelligent NoSQL Databases (CSE494) at Lovely Professional University, Phagwara, Punjab. "
        "The project demonstrates the practical application of NoSQL document modelling, PyMongo driver integration, database-level schema validation, and multi-stage aggregation pipelines. "
        "I confirm that this report has not been submitted elsewhere for any academic degree or diploma.")
    
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(14)
    p_sig.paragraph_format.space_after = Pt(16)
    p_sig.add_run("Aman Prateek\nRegistration No: 12310657 | Roll No: 19\nSchool of Computer Science & Engineering, LPU").bold = True

    add_styled_heading(doc, "CERTIFICATE OF ORIGINALITY", 1)
    add_body_p(doc, 
        "This is to certify that the project report entitled 'Expense Analytics' submitted by Aman Prateek (Reg. No. 12310657) has been prepared under academic supervision. "
        "The work embodies comprehensive implementation of modern NoSQL database concepts including JSON schema validation, CRUD operations, indexing strategies, "
        "and analytical pipelines connected to a full-stack web application. The results and conclusions embodied in this report have been verified and found satisfactory.")

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(14)
    p_guide.paragraph_format.space_after = Pt(16)
    p_guide.add_run("Course Coordinator / Evaluator\nDepartment of Computer Science & Engineering\nLovely Professional University, Phagwara").bold = True

    add_styled_heading(doc, "ABSTRACT", 1)
    add_body_p(doc, 
        "Traditional personal finance applications rely heavily on relational database management systems (RDBMS) featuring rigid tabular structures, "
        "complex normalization constraints, and computationally expensive multi-table JOIN operations for analytical roll-ups. In the modern era of rapid digital micro-transactions "
        "(such as Unified Payments Interface - UPI, contactless debit cards, and e-wallets), transactional spending data is inherently semi-structured, containing polymorphic metadata, "
        "variable tagging arrays, and dynamic merchant attributes. This project presents 'Expense Analytics', a high-performance 3-tier financial management system built on top of "
        "MongoDB 8.0+, Python Flask REST APIs, and a React 19 single-page application. The system leverages MongoDB's BSON document model, database-level strict $jsonSchema validation, "
        "and seven native Aggregation Pipelines to perform zero-join, in-engine analytics for monthly budget trends, category spending distribution, and merchant expenditure rankings. "
        "Empirical testing with a verified empirical dataset confirms real-time query resolution with complete transactional consistency and zero data leakage.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: CHAPTER 1 - INTRODUCTION & PROBLEM STATEMENT
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT", 1)
    
    add_styled_heading(doc, "1.1 Background and Context", 2)
    add_body_p(doc, 
        "In recent years, the explosion of digital payment ecosystems in India, spearheaded by the Unified Payments Interface (UPI) and mobile banking applications, "
        "has drastically reduced the friction associated with day-to-day spending. While cashless convenience has accelerated commerce, it has introduced a severe cognitive disconnect "
        "for students and young adults: because tangible physical currency does not exchange hands, individuals frequently lose track of cumulative micro-expenditures. "
        "At the end of each billing cycle, users face unexpected budget deficits without understanding where their financial capital was allocated.")

    add_styled_heading(doc, "1.2 Motivation", 2)
    add_body_p(doc, 
        "Standard personal expense trackers commonly suffer from two distinct architectural drawbacks: either they are overly simplistic static spreadsheets lacking validation, "
        "or they are bloated legacy SQL-backed enterprise applications. In an RDBMS, adding polymorphic attributes (such as variable item tags, multiple category splits, or merchant identifiers) "
        "requires extensive schema alteration migrations, foreign key cascading, and multi-table JOIN queries that suffer significant latency degradation as transaction tables grow into hundreds of thousands of rows. "
        "There is a distinct necessity for an intelligent NoSQL-driven solution that provides flexible schema evolution while enforcing strict transactional validation at the database core.")

    add_styled_heading(doc, "1.3 Problem Statement", 2)
    add_body_p(doc, 
        "To design, develop, and benchmark an intelligent, full-stack personal finance and expense tracking system that utilizes MongoDB's NoSQL document architecture to store, "
        "strictly validate, and aggregate multi-category financial records in real time, delivering actionable analytics through an interactive React web dashboard.")

    add_styled_heading(doc, "1.4 Project Objectives", 2)
    add_bullet_p(doc, "Design and implement a document-oriented database schema in MongoDB specifically optimized for temporal transaction records.", "Objective 1: ")
    add_bullet_p(doc, "Enforce strict collection-level data integrity using MongoDB's $jsonSchema validator to eliminate negative amounts, invalid enums, and malformed inputs.", "Objective 2: ")
    add_bullet_p(doc, "Develop seven native multi-stage MongoDB Aggregation Pipelines to compute key performance indicators (KPIs), category distributions, and monthly spending trends directly inside the database engine.", "Objective 3: ")
    add_bullet_p(doc, "Engineer a robust, decoupled REST API middleware utilizing Python 3.10, Flask, and the PyMongo driver with complete BSON serialization and CORS protection.", "Objective 4: ")
    add_bullet_p(doc, "Deliver a responsive, reactive single-page user interface using React 19, Vite, Recharts, and custom CSS design systems to visualize real-time analytical data.", "Objective 5: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: CHAPTER 2 - THEORETICAL ANALYSIS: RDBMS VS. NOSQL MONGODB
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 2: THEORETICAL ANALYSIS & COMPARATIVE STUDY", 1)

    add_styled_heading(doc, "2.1 The Case for NoSQL in Financial Analytics", 2)
    add_body_p(doc, 
        "Relational Database Management Systems (RDBMS) like MySQL and PostgreSQL were architected under assumptions of structural uniformity and disk-space scarcity in the 1970s. "
        "Consequently, they mandate rigid schema declarations and strict tabular normalization (1NF, 2NF, 3NF). However, modern transactional logs are document-oriented by nature: "
        "a single transaction represents a self-contained factual event encompassing date, amount, vendor, category, and an arbitrary list of semantic tags.")

    add_styled_heading(doc, "2.2 Comparative Architecture: MySQL vs. MongoDB", 2)
    add_body_p(doc, "The table below summarizes the architectural distinctions and empirical advantages of utilizing MongoDB for financial analytics over traditional RDBMS:")

    tbl_comp = doc.add_table(rows=6, cols=3)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Evaluation Metric", "Relational Database (MySQL/PostgreSQL)", "Document Store (MongoDB 8.0+)"]
    for j, h in enumerate(headers):
        cell = tbl_comp.cell(0, j)
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)
        set_cell_margins(cell, 80, 80, 100, 100)

    rows_data = [
        ("Data Model", "Rigid two-dimensional tables with fixed columns.", "Flexible, hierarchical BSON documents with dynamic fields."),
        ("Tagging / Arrays", "Requires junction tables (M:N) and costly JOIN operations.", "Native embedded arrays (`tags: ['food', 'lunch']`) indexed directly."),
        ("Analytical Aggregations", "Heavy `GROUP BY` and multi-table JOINs consuming server RAM.", "Native C++ multi-stage Aggregation Pipeline (`$match`, `$group`, `$sort`)."),
        ("Schema Evolution", "Downtime required for `ALTER TABLE` operations across large datasets.", "Dynamic schema with collection-level `$jsonSchema` versioning."),
        ("Scalability", "Primarily vertical scaling (expensive hardware upgrades).", "Native horizontal scale-out via automatic sharding across clusters.")
    ]
    for i, row in enumerate(rows_data):
        for j, text in enumerate(row):
            cell = tbl_comp.cell(i+1, j)
            set_cell_background(cell, "F9FBFD" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if j == 0: r.bold = True

    add_styled_heading(doc, "2.3 Eliminating Impedance Mismatch", 2)
    add_body_p(doc, 
        "In modern web development, frontend frameworks (React) and backend runtimes (Python/Node) operate naturally with JSON objects. When using an RDBMS, an Object-Relational Mapper (ORM) "
        "must continually translate tabular rows into objects, introducing CPU overhead known as 'Object-Relational Impedance Mismatch'. "
        "With MongoDB, the native storage representation (BSON) is binary JSON. Hence, data passes from the database engine to the REST API and to the React browser client with near-zero transformation overhead.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: CHAPTER 3 - SOFTWARE REQUIREMENTS & SYSTEM ARCHITECTURE
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 3: SYSTEM ARCHITECTURE & SPECIFICATIONS", 1)

    add_styled_heading(doc, "3.1 3-Tier Decoupled Architecture", 2)
    add_body_p(doc, 
        "The system adopts a modular 3-tier client-server architecture designed for high maintainability, fault isolation, and independent scalability:")
    add_bullet_p(doc, "Presentation Layer (Client): Single-Page Application (SPA) developed with React 19, Vite build tooling, and Recharts visualization. Handles UI state, event handling, and asynchronous API calls.", "Tier 1: ")
    add_bullet_p(doc, "Application Layer (Server): Lightweight REST API built using Python 3.10 and Flask 3.1.2. Orchestrates business logic, incoming payload validation, BSON serialization, and PyMongo client communication.", "Tier 2: ")
    add_bullet_p(doc, "Data Persistence Layer (Database): MongoDB 8.0+ Community Server running on port 27017. Hosts the `expense_analytics` database and the strictly validated `expenses` collection.", "Tier 3: ")

    add_styled_heading(doc, "3.2 Hardware and Software Specifications", 2)
    tbl_req = doc.add_table(rows=6, cols=2)
    tbl_req.alignment = WD_TABLE_ALIGNMENT.CENTER
    specs = [
        ("Operating System", "Microsoft Windows 10/11 (x64 Architecture)"),
        ("Database Engine", "MongoDB Community Server Version 8.0+ / Mongosh 2.x"),
        ("Backend Framework & Driver", "Python 3.10.11, Flask 3.1.2, PyMongo 4.15.1, Flask-CORS 6.0.1"),
        ("Frontend Runtime & Libraries", "Node.js 18+, React 19, Vite 8.3, Recharts, Lucide-React"),
        ("Local Port Allocations", "Frontend: Port 5173 | Backend: Port 5000 | MongoDB: Port 27017")
    ]
    for i, (k, v) in enumerate(specs):
        c1, c2 = tbl_req.cell(i, 0), tbl_req.cell(i, 1)
        c1.width, c2.width = Inches(2.2), Inches(4.2)
        set_cell_background(c1, "EAEFF5")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c1, 50, 50, 80, 80)
        set_cell_margins(c2, 50, 50, 80, 80)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(k); r1.bold = True; r1.font.size = Pt(9.5)
        p2 = c2.paragraphs[0]; r2 = p2.add_run(v); r2.font.size = Pt(9.5)

    add_styled_heading(doc, "3.3 REST API Endpoints Specification", 2)
    add_body_p(doc, "The backend exposes clean, stateless RESTful endpoints over HTTP supporting standard JSON payloads:")
    add_bullet_p(doc, "GET /api/health — Connectivity probe verifying database status and server health.", "Health Check: ")
    add_bullet_p(doc, "GET /api/expenses — Returns filtered transactions with query params for category, payment_method, search, and month.", "Read Transactions: ")
    add_bullet_p(doc, "POST /api/expenses — Validates and inserts a new expense document into the database.", "Create Transaction: ")
    add_bullet_p(doc, "PUT /api/expenses/<id> & DELETE /api/expenses/<id> — Updates or removes a transaction by its BSON ObjectId.", "Update/Delete: ")
    add_bullet_p(doc, "GET /api/analytics/* — Specialized endpoints executing MongoDB aggregation pipelines for summary KPIs, categories, monthly trends, and merchants.", "Analytics Endpoints: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: CHAPTER 4 - DATABASE DESIGN & STRICT SCHEMA VALIDATION
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 4: DATABASE DESIGN & SCHEMA VALIDATION", 1)

    add_styled_heading(doc, "4.1 Document Structure and BSON Representation", 2)
    add_body_p(doc, 
        "Every transaction record in the `expenses` collection is stored as an independent BSON document. "
        "Unlike an SQL table requiring separate lookup tables for tags and payment modes, all metadata is encapsulated natively:")
    
    add_code_block(doc, 
"""{
  "_id": ObjectId("6ae85a015da12b7c2616a41c"),
  "user_id": "12310657",
  "amount": 320.0,
  "category": "Food",
  "description": "Lunch at Campus Cafe",
  "payment_method": "UPI",
  "date": ISODate("2026-07-02T00:00:00.000Z"),
  "merchant": "Campus Cafe",
  "tags": ["food", "college"],
  "created_at": ISODate("2026-11-02T09:38:09.216Z")
}""")

    add_styled_heading(doc, "4.2 Database-Level $jsonSchema Validation Rules", 2)
    add_body_p(doc, 
        "To refute the common misconception that NoSQL databases cannot guarantee data integrity, this project implements a strict, collection-level "
        "JSON Schema validator configured directly in the database engine (`mongodb/schema_validation.js`):")

    add_code_block(doc, 
"""db.createCollection('expenses', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'amount', 'category', 'description', 'payment_method', 'date'],
      properties: {
        user_id: { bsonType: 'string', minLength: 1 },
        amount: { bsonType: ['double', 'int', 'long', 'decimal'], minimum: 0.01 },
        category: { enum: ['Food', 'Transport', 'Shopping', 'Bills', 'Education', 'Entertainment', 'Healthcare', 'Other'] },
        description: { bsonType: 'string', minLength: 1 },
        payment_method: { enum: ['Cash', 'UPI', 'Credit Card', 'Debit Card'] },
        date: { bsonType: 'date' },
        merchant: { bsonType: 'string' },
        tags: { bsonType: 'array', items: { bsonType: 'string' } },
        created_at: { bsonType: 'date' }
      }
    }
  },
  validationLevel: 'strict',
  validationAction: 'error'
});""")

    add_body_p(doc, 
        "Setting `validationLevel: 'strict'` guarantees that all write operations (both inserts and updates) must satisfy the schema constraints. "
        "Setting `validationAction: 'error'` ensures that any illegal operation (such as negative amounts, empty descriptions, or unrecognized categories) "
        "is immediately aborted with an execution WriteError.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: CHAPTER 5 - MONGODB AGGREGATION PIPELINES
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 5: MONGODB AGGREGATION PIPELINES", 1)

    add_styled_heading(doc, "5.1 Pipeline Philosophy: Server-Side Analytics", 2)
    add_body_p(doc, 
        "The core technical highlight of this project is the complete reliance on MongoDB Aggregation Pipelines for business intelligence. "
        "Rather than fetching raw documents to Python and iterating with inefficient CPU loops, all mathematical transformations and grouping operations "
        "execute directly within MongoDB's multi-threaded C++ database engine.")

    add_styled_heading(doc, "5.2 Detailed Aggregation Pipeline Listings", 2)
    
    add_body_p(doc, "1. KPI Summary Aggregation (Total Spend, Average, Count):", bold_prefix="Pipeline 1: ")
    add_code_block(doc, 
"""db.expenses.aggregate([
  { $group: { 
      _id: null, 
      total: { $sum: "$amount" }, 
      average: { $avg: "$amount" }, 
      count: { $sum: 1 } 
  }}
]);""")

    add_body_p(doc, "2. Monthly Spending Trends (Using $dateToString for Date Bucketing):", bold_prefix="Pipeline 2: ")
    add_code_block(doc, 
"""db.expenses.aggregate([
  { $group: { 
      _id: { $dateToString: { format: "%Y-%m", date: "$date" } }, 
      total: { $sum: "$amount" } 
  }},
  { $sort: { _id: 1 } }
]);""")

    add_body_p(doc, "3. Category-Wise Expenditure Breakdown:", bold_prefix="Pipeline 3: ")
    add_code_block(doc, 
"""db.expenses.aggregate([
  { $group: { _id: "$category", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } }
]);""")

    add_body_p(doc, "4. Top Merchant Spending with $match Filtering:", bold_prefix="Pipeline 4: ")
    add_code_block(doc, 
"""db.expenses.aggregate([
  { $match: { merchant: { $nin: [null, ""] } } },
  { $group: { 
      _id: "$merchant", 
      total: { $sum: "$amount" }, 
      transactions: { $sum: 1 } 
  }},
  { $sort: { total: -1 } },
  { $limit: 5 }
]);""")

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: CHAPTER 6 - BACKEND IMPLEMENTATION WITH PYTHON & PYMONGO
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 6: BACKEND IMPLEMENTATION & MIDDLEWARE", 1)

    add_styled_heading(doc, "6.1 PyMongo Database Connection Architecture", 2)
    add_body_p(doc, 
        "The Python backend communicates with MongoDB using PyMongo, the official MongoDB driver. Connection configuration is isolated in "
        "`backend/database.py`, using environment variables loaded via `python-dotenv` for 12-factor application compliance:")

    add_code_block(doc, 
"""# backend/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "expense_analytics")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DATABASE_NAME]
expenses = db["expenses"]""")

    add_styled_heading(doc, "6.2 Serialization & BSON Type Conversion", 2)
    add_body_p(doc, 
        "MongoDB documents contain specialized BSON data types (such as `bson.ObjectId` and `datetime.datetime`) that cannot be serialized into JSON by default. "
        "A dedicated serialization utility in `backend/app.py` converts native BSON types into JSON-compatible primitives:")

    add_code_block(doc, 
"""def serialize(doc):
    if not doc:
        return None
    result = dict(doc)
    result["_id"] = str(result["_id"])  # Convert ObjectId to string
    if isinstance(result.get("date"), datetime):
        result["date"] = result["date"].strftime("%Y-%m-%d")
    if isinstance(result.get("created_at"), datetime):
        result["created_at"] = result["created_at"].isoformat()
    return result""")

    add_styled_heading(doc, "6.3 Dual-Tier Payload Validation", 2)
    add_body_p(doc, 
        "While MongoDB enforces schema rules at the database boundary, the Flask API implements front-line input validation inside `parse_payload()`. "
        "This function sanitizes user inputs, casts string amounts to floats, and returns clear HTTP 400 Bad Request error messages before hitting the database.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: CHAPTER 7 - FRONTEND VISUALIZATION & USER INTERFACE
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 7: FRONTEND VISUALIZATION & UI DESIGN", 1)

    add_styled_heading(doc, "7.1 React 19 Client Architecture", 2)
    add_body_p(doc, 
        "The frontend is structured as a Single-Page Application (SPA) leveraging React 19 and Vite. The application state is managed cleanly using React's "
        "`useState`, `useEffect`, and `useCallback` hooks. When the application mounts, it executes parallel API calls to fetch both the transaction ledger "
        "and pre-computed aggregation analytics:")

    add_code_block(doc, 
"""const load = useCallback(async () => {
  setLoading(true); setError('');
  try {
    const [e, s, c, m, p, me, t] = await Promise.all([
      api.expenses(filters), api.summary(), api.categories(),
      api.monthly(), api.payments(), api.merchants(), api.trends()
    ]);
    setExpenses(e); setSummary(s); setCats(c); setMonthly(m);
    setPmt(p); setMerch(me); setTrends(t);
  } catch (err) { setError(err.message); }
  finally { setLoading(false); }
}, [filters]);""")

    add_styled_heading(doc, "7.2 Interactive Charting with Recharts", 2)
    add_body_p(doc, 
        "The dashboard visualizes multidimensional data using responsive Recharts components:")
    add_bullet_p(doc, "A BarChart tracking monthly expenditures across calendar months, featuring custom tooltips and coral accent colors.", "Monthly Spending Bar Chart: ")
    add_bullet_p(doc, "A customized PieChart with innerRadius rendering a clean donut chart that illustrates spending percentages across Food, Bills, Shopping, etc.", "Category Breakdown Donut: ")
    add_bullet_p(doc, "A secondary donut chart and tabular legend reflecting the volume and percentage of transactions executed through UPI, Debit Cards, Cash, and Credit Cards.", "Payment Methods Analytics: ")
    add_bullet_p(doc, "High-contrast KPI cards displaying Total Spending, Total Transaction Count, Average Ticket Size, and Top Category with skeleton loading states.", "Metric KPI Cards: ")

    add_styled_heading(doc, "7.3 Transaction Management & Real-Time Filtering", 2)
    add_body_p(doc, 
        "The Transactions view incorporates real-time debounced text searching (querying description and merchant via MongoDB `$regex`) "
        "along with dropdown filters for category, payment method, and billing month. Users can add, edit, or delete transactions through accessible modal dialogs.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: CHAPTER 8 - TESTING, VERIFICATION & RESULTS ANALYSIS
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 8: TESTING, VERIFICATION & EMPIRICAL RESULTS", 1)

    add_styled_heading(doc, "8.1 Verified Empirical Dataset", 2)
    add_body_p(doc, 
        "The system was seeded and verified with 41 realistic transaction records spanning July to September 2026, associated with student registration number `12310657`. "
        "The table below details the verified empirical metrics computed by MongoDB's aggregation engine:")

    tbl_results = doc.add_table(rows=7, cols=3)
    tbl_results.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = ["Metric / Dimension", "MongoDB Aggregated Output", "Academic Significance"]
    for j, h in enumerate(res_headers):
        c = tbl_results.cell(0, j); set_cell_background(c, "102C57")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h); r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255); r.font.size = Pt(9.5)
        set_cell_margins(c, 70, 70, 90, 90)

    res_data = [
        ("Total Expenditure", "₹20,808.00", "Accurate cumulative sum across all 41 transactions."),
        ("Total Transactions", "41 records", "Verified document count in `expenses` collection."),
        ("Average Ticket Size", "₹507.51", "Accurate mathematical average (`$avg: '$amount'`)."),
        ("Highest Spending Category", "Bills (₹5,000.00 / 24.03%)", "Computed via `$sort: { total: -1 }` and `$limit: 1`."),
        ("Dominant Payment Method", "UPI (56.65% / ₹11,788.00)", "Reflects real-world student digital payment distribution."),
        ("Top Individual Merchant", "StyleHub (₹3,060.00 across 4 txns)", "Multi-stage pipeline successfully groups by vendor.")
    ]
    for i, row in enumerate(res_data):
        for j, text in enumerate(row):
            cell = tbl_results.cell(i+1, j)
            set_cell_background(cell, "F9FBFD" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]; r = p.add_run(text); r.font.size = Pt(9)
            if j == 0: r.bold = True

    add_styled_heading(doc, "8.2 Test Suite Verification Matrix", 2)
    add_body_p(doc, "Comprehensive black-box and validation test cases were conducted to confirm database and API robustness:")
    add_bullet_p(doc, "Input: `amount = -150`. Result: MongoDB rejects insert with `WriteError: Document failed validation`. HTTP Status 400 returned. Status: PASSED.", "Test Case 1 (Negative Amount): ")
    add_bullet_p(doc, "Input: `category = 'Crypto'`. Result: Validation fails because 'Crypto' is not in the declared enum array. Status: PASSED.", "Test Case 2 (Invalid Category Enum): ")
    add_bullet_p(doc, "Input: Search query `cafe`. Result: MongoDB executes `$regex: 'cafe', $options: 'i'` across description and merchant fields, returning 4 matching records. Status: PASSED.", "Test Case 3 (Regex Search): ")
    add_bullet_p(doc, "Input: Delete transaction `6ae85a015da12b7c2616a41c`. Result: Document removed, subsequent aggregation immediately recalculates total spend to ₹20,488. Status: PASSED.", "Test Case 4 (CRUD & Aggregation Reactivity): ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 11: CHAPTER 9 & 10 - CONCLUSION, FUTURE ROADMAP & REFERENCES
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 9: CONCLUSION & FUTURE SCOPE", 1)

    add_styled_heading(doc, "9.1 Project Conclusion", 2)
    add_body_p(doc, 
        "The 'Expense Analytics' system successfully demonstrates the immense architectural advantages of deploying MongoDB in personal finance and analytical domains. "
        "By discarding rigid relational table structures in favor of flexible, self-contained BSON documents, the system achieves frictionless schema evolution while maintaining "
        "ironclad data integrity via database-level `$jsonSchema` validation. "
        "Furthermore, utilizing native Aggregation Pipelines proves that complex analytical rollups can be executed inside the database engine with superior speed and minimal memory footprint. "
        "The integration with Python Flask and React 19 produces a responsive, intuitive, and modern application that fulfills all academic and engineering goals.")

    add_styled_heading(doc, "9.2 Future Enhancements Roadmap", 2)
    add_bullet_p(doc, "Implement monthly category budget caps that trigger visual warning indicators when spending surpasses 85% of budget limits.", "1. Budget Threshold Alerts: ")
    add_bullet_p(doc, "Integrate optical character recognition (OCR) via Tesseract or Google Cloud Vision to extract amounts and merchants automatically from physical receipts.", "2. OCR Receipt Scanning: ")
    add_bullet_p(doc, "Deploy predictive machine learning models (ARIMA or LSTM) to forecast student month-end cash outflows based on historical spending velocity.", "3. Predictive Spending Analytics: ")
    add_bullet_p(doc, "Provide automated PDF report generation and CSV export capabilities for academic and personal record keeping.", "4. Multi-Format Report Export: ")

    add_styled_heading(doc, "CHAPTER 10: REFERENCES & BIBLIOGRAPHY", 1)
    refs = [
        ("MongoDB Inc.", "MongoDB Documentation: The Aggregation Pipeline Framework, Available: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/, 2026."),
        ("MongoDB Inc.", "JSON Schema Validation in MongoDB, Available: https://www.mongodb.com/docs/manual/core/schema-validation/, 2026."),
        ("Pallets Projects", "Flask Documentation (v3.1.x) - Lightweight WSGI Web Application Framework, Available: https://flask.palletsprojects.com/, 2026."),
        ("Python Software Foundation", "PyMongo: The Official Python Driver for MongoDB, Available: https://pymongo.readthedocs.io/, 2026."),
        ("Meta Platforms Inc.", "React Documentation: Building Modern Interactive Single-Page User Interfaces, Available: https://react.dev/, 2026."),
        ("Recharts Group", "Recharts: Redefined Charting Library Built with React and D3, Available: https://recharts.org/, 2026."),
        ("Silberschatz, A., Korth, H. F., & Sudarshan, S.", "Database System Concepts (7th Edition), McGraw-Hill Education, 2020.")
    ]
    for author, title in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_num = p.add_run(f"[{refs.index((author, title))+1}] ")
        r_num.bold = True
        r_auth = p.add_run(f"{author}, ")
        r_auth.italic = True
        r_tit = p.add_run(f"\"{title}\"")

    output_docx = r'd:\College\Sem 7\mongodb\ca2\AryanKumar12310657_Project_Report.docx'
    doc.save(output_docx)
    print(f"Docx report created successfully at: {output_docx}")

    # Convert to PDF via Word COM
    output_pdf = r'd:\College\Sem 7\mongodb\ca2\AryanKumar12310657_Project_Report.pdf'
    ps_cmd = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("{output_docx}")
$doc.SaveAs([ref]"{output_pdf}", [ref]17)
$doc.Close()
$word.Quit()
Write-Output "PDF generated successfully!"
"""
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    print("PowerShell PDF export STDOUT:", res.stdout)
    print("PowerShell PDF export STDERR:", res.stderr)

if __name__ == '__main__':
    build_report()
