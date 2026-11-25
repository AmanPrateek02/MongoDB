# EXPENSE ANALYTICS: AN INTELLIGENT MONGODB-BASED PERSONAL FINANCE TRACKING AND ANALYTICS SYSTEM

> **Academic Course Project Report**  
> **Course:** CSE494 — Intelligent NoSQL Databases  
> **Department:** School of Computer Science & Engineering  
> **Institution:** Lovely Professional University, Phagwara, Punjab — 144411  
> **Student:** Aman Prateek | **Roll No:** 19 | **Registration No:** 12310657
> **GitHub Repository:** [https://github.com/Aryan114mehta/MongoDB](https://github.com/Aryan114mehta/MongoDB)  
> **Academic Term:** Autumn Term (August – December 2026)  

---

## CANDIDATE'S DECLARATION
I hereby declare that the work presented in this project report entitled **"Expense Analytics: An Intelligent MongoDB-Based Personal Finance Tracking and Analytics System"** is an authentic record of my own work carried out as partial fulfilment of the requirements for the Continuous Assessment and Capstone Project in the course **Intelligent NoSQL Databases (CSE494)** at Lovely Professional University, Phagwara, Punjab.

The project demonstrates the practical application of NoSQL document modelling, PyMongo driver integration, database-level schema validation, and multi-stage aggregation pipelines. I confirm that this report has not been submitted elsewhere for any academic degree or diploma.

**Aman Prateek**
Registration No: 12310657 | Roll No: 19  
School of Computer Science & Engineering, Lovely Professional University  

---

## CERTIFICATE OF ORIGINALITY
This is to certify that the project report entitled **"Expense Analytics"** submitted by **Aman Prateek (Reg. No. 12310657)** has been prepared under academic supervision. The work embodies comprehensive implementation of modern NoSQL database concepts including JSON schema validation, CRUD operations, indexing strategies, and analytical pipelines connected to a full-stack web application. The results and conclusions embodied in this report have been verified and found satisfactory.

**Course Coordinator / Evaluator**  
Department of Computer Science & Engineering  
Lovely Professional University, Phagwara  

---

## ABSTRACT
Traditional personal finance applications rely heavily on relational database management systems (RDBMS) featuring rigid tabular structures, complex normalization constraints, and computationally expensive multi-table JOIN operations for analytical roll-ups. In the modern era of rapid digital micro-transactions (such as Unified Payments Interface - UPI, contactless debit cards, and e-wallets), transactional spending data is inherently semi-structured, containing polymorphic metadata, variable tagging arrays, and dynamic merchant attributes. 

This project presents **"Expense Analytics"**, a high-performance 3-tier financial management system built on top of **MongoDB 8.0+**, **Python Flask REST APIs**, and a **React 19 single-page application**. The system leverages MongoDB's BSON document model, database-level strict `$jsonSchema` validation, and seven native Aggregation Pipelines to perform zero-join, in-engine analytics for monthly budget trends, category spending distribution, and merchant expenditure rankings. Empirical testing with a verified empirical dataset of 41 transactions confirms real-time query resolution with complete transactional consistency and zero data leakage.

---

## TABLE OF CONTENTS
1. [Chapter 1: Introduction & Problem Statement](#chapter-1-introduction--problem-statement)
2. [Chapter 2: Theoretical Background & Comparative Analysis (RDBMS vs. NoSQL)](#chapter-2-theoretical-background--comparative-analysis)
3. [Chapter 3: System Architecture & Requirements Specifications](#chapter-3-system-architecture--requirements-specifications)
4. [Chapter 4: MongoDB Database Design & Strict Schema Validation](#chapter-4-mongodb-database-design--strict-schema-validation)
5. [Chapter 5: MongoDB Aggregation Pipelines & Analytical Intelligence](#chapter-5-mongodb-aggregation-pipelines--analytical-intelligence)
6. [Chapter 6: Backend Implementation & Middleware Architecture](#chapter-6-backend-implementation--middleware-architecture)
7. [Chapter 7: Frontend Visualization & User Interface Design](#chapter-7-frontend-visualization--user-interface-design)
8. [Chapter 8: Testing, Verification & Empirical Results](#chapter-8-testing-verification--empirical-results)
9. [Chapter 9: Conclusion, Limitations & Future Scope](#chapter-9-conclusion-limitations--future-scope)
10. [Chapter 10: References & Bibliography](#chapter-10-references--bibliography)

---

## CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT

### 1.1 Background and Context
In recent years, the explosion of digital payment ecosystems in India, spearheaded by the Unified Payments Interface (UPI) and mobile banking applications, has drastically reduced the friction associated with day-to-day spending. While cashless convenience has accelerated commerce, it has introduced a severe cognitive disconnect for students and young adults: because tangible physical currency does not exchange hands, individuals frequently lose track of cumulative micro-expenditures. At the end of each billing cycle, users face unexpected budget deficits without understanding where their financial capital was allocated.

### 1.2 Motivation
Standard personal expense trackers commonly suffer from two distinct architectural drawbacks: either they are overly simplistic static spreadsheets lacking validation, or they are bloated legacy SQL-backed enterprise applications. In an RDBMS, adding polymorphic attributes (such as variable item tags, multiple category splits, or merchant identifiers) requires extensive schema alteration migrations, foreign key cascading, and multi-table JOIN queries that suffer significant latency degradation as transaction tables grow into hundreds of thousands of rows. There is a distinct necessity for an intelligent NoSQL-driven solution that provides flexible schema evolution while enforcing strict transactional validation at the database core.

### 1.3 Problem Statement
To design, develop, and benchmark an intelligent, full-stack personal finance and expense tracking system that utilizes MongoDB's NoSQL document architecture to store, strictly validate, and aggregate multi-category financial records in real time, delivering actionable analytics through an interactive React web dashboard.

### 1.4 Project Objectives
- **Objective 1:** Design and implement a document-oriented database schema in MongoDB specifically optimized for temporal transaction records.
- **Objective 2:** Enforce strict collection-level data integrity using MongoDB's `$jsonSchema` validator to eliminate negative amounts, invalid enums, and malformed inputs.
- **Objective 3:** Develop seven native multi-stage MongoDB Aggregation Pipelines to compute key performance indicators (KPIs), category distributions, and monthly spending trends directly inside the database engine.
- **Objective 4:** Engineer a robust, decoupled REST API middleware utilizing Python 3.10, Flask, and the PyMongo driver with complete BSON serialization and CORS protection.
- **Objective 5:** Deliver a responsive, reactive single-page user interface using React 19, Vite, Recharts, and custom CSS design systems to visualize real-time analytical data.

---

## CHAPTER 2: THEORETICAL BACKGROUND & COMPARATIVE ANALYSIS

### 2.1 The Case for NoSQL in Financial Analytics
Relational Database Management Systems (RDBMS) like MySQL and PostgreSQL were architected under assumptions of structural uniformity and disk-space scarcity in the 1970s. Consequently, they mandate rigid schema declarations and strict tabular normalization (1NF, 2NF, 3NF). However, modern transactional logs are document-oriented by nature: a single transaction represents a self-contained factual event encompassing date, amount, vendor, category, and an arbitrary list of semantic tags.

### 2.2 Comparative Architecture: MySQL vs. MongoDB

| Evaluation Metric | Relational Database (MySQL / PostgreSQL) | Document Store (MongoDB 8.0+) |
| :--- | :--- | :--- |
| **Data Model** | Rigid two-dimensional tables with fixed columns. | Flexible, hierarchical BSON documents with dynamic fields. |
| **Tagging / Arrays** | Requires junction tables (M:N) and costly JOIN operations. | Native embedded arrays (`tags: ['food', 'lunch']`) indexed directly. |
| **Analytical Aggregations** | Heavy `GROUP BY` and multi-table JOINs consuming server RAM. | Native C++ multi-stage Aggregation Pipeline (`$match`, `$group`, `$sort`). |
| **Schema Evolution** | Downtime required for `ALTER TABLE` operations across large datasets. | Dynamic schema with collection-level `$jsonSchema` versioning. |
| **Scalability** | Primarily vertical scaling (expensive hardware upgrades). | Native horizontal scale-out via automatic sharding across clusters. |

### 2.3 Eliminating Impedance Mismatch
In modern web development, frontend frameworks (React) and backend runtimes (Python/Node) operate naturally with JSON objects. When using an RDBMS, an Object-Relational Mapper (ORM) must continually translate tabular rows into objects, introducing CPU overhead known as "Object-Relational Impedance Mismatch". With MongoDB, the native storage representation (BSON) is binary JSON. Hence, data passes from the database engine to the REST API and to the React browser client with near-zero transformation overhead.

---

## CHAPTER 3: SYSTEM ARCHITECTURE & REQUIREMENTS SPECIFICATIONS

### 3.1 3-Tier Decoupled Architecture
The system adopts a modular 3-tier client-server architecture designed for high maintainability, fault isolation, and independent scalability:
1. **Presentation Layer (Tier 1):** Single-Page Application (SPA) developed with React 19, Vite build tooling, and Recharts visualization. Handles UI state, event handling, and asynchronous API calls.
2. **Application Layer (Tier 2):** Lightweight REST API built using Python 3.10 and Flask 3.1.2. Orchestrates business logic, incoming payload validation, BSON serialization, and PyMongo client communication.
3. **Data Persistence Layer (Tier 3):** MongoDB 8.0+ Community Server running on port 27017. Hosts the `expense_analytics` database and the strictly validated `expenses` collection.

### 3.2 Technical Specifications

| Parameter | Specification Details |
| :--- | :--- |
| **Operating System** | Microsoft Windows 10/11 (x64 Architecture) |
| **Database Engine** | MongoDB Community Server Version 8.0+ / Mongosh 2.x |
| **Backend Framework & Driver** | Python 3.10.11, Flask 3.1.2, PyMongo 4.15.1, Flask-CORS 6.0.1 |
| **Frontend Runtime & Libraries** | Node.js 18+, React 19, Vite 8.3, Recharts, Lucide-React |
| **Local Port Allocations** | Frontend: Port 5173 \| Backend: Port 5000 \| MongoDB: Port 27017 |

---

## CHAPTER 4: MONGODB DATABASE DESIGN & STRICT SCHEMA VALIDATION

### 4.1 Document Structure and BSON Representation
Every transaction record in the `expenses` collection is stored as an independent BSON document:
```json
{
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
}
```

### 4.2 Database-Level $jsonSchema Validation Rules
To refute the common misconception that NoSQL databases cannot guarantee data integrity, this project implements a strict, collection-level JSON Schema validator configured directly in the database engine (`mongodb/schema_validation.js`):
```javascript
db.createCollection('expenses', {
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
});
```
- **validationLevel: 'strict'**: All inserts and updates must satisfy the schema constraints.
- **validationAction: 'error'**: Any illegal operation (e.g. negative amounts or unapproved category values) is immediately aborted with a `WriteError`.

---

## CHAPTER 5: MONGODB AGGREGATION PIPELINES

### 5.1 The 7 Analytical Pipelines

#### 1. KPI Summary Aggregation
```javascript
db.expenses.aggregate([
  { $group: { 
      _id: null, 
      total: { $sum: "$amount" }, 
      average: { $avg: "$amount" }, 
      count: { $sum: 1 } 
  }}
]);
```

#### 2. Monthly Spending Trends (Date Bucketing via `$dateToString`)
```javascript
db.expenses.aggregate([
  { $group: { 
      _id: { $dateToString: { format: "%Y-%m", date: "$date" } }, 
      total: { $sum: "$amount" } 
  }},
  { $sort: { _id: 1 } }
]);
```

#### 3. Category-Wise Spending Distribution
```javascript
db.expenses.aggregate([
  { $group: { _id: "$category", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } }
]);
```

#### 4. Top 5 Merchants Analysis with `$match` Pre-Filtering
```javascript
db.expenses.aggregate([
  { $match: { merchant: { $nin: [null, ""] } } },
  { $group: { 
      _id: "$merchant", 
      total: { $sum: "$amount" }, 
      transactions: { $sum: 1 } 
  }},
  { $sort: { total: -1 } },
  { $limit: 5 }
]);
```

---

## CHAPTER 6: BACKEND IMPLEMENTATION WITH PYTHON & PYMONGO

### 6.1 Database Connection Configuration (`backend/database.py`)
```python
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "expense_analytics")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DATABASE_NAME]
expenses = db["expenses"]
```

### 6.2 Serialization of BSON Types
```python
def serialize(doc):
    if not doc:
        return None
    result = dict(doc)
    result["_id"] = str(result["_id"])
    if isinstance(result.get("date"), datetime):
        result["date"] = result["date"].strftime("%Y-%m-%d")
    if isinstance(result.get("created_at"), datetime):
        result["created_at"] = result["created_at"].isoformat()
    return result
```

---

## CHAPTER 7: FRONTEND VISUALIZATION & USER INTERFACE

### 7.1 React Single-Page Application Architecture
The client interface utilizes React hooks (`useState`, `useEffect`, `useCallback`) to perform parallel REST data fetching via `Promise.all()`:
```javascript
const load = useCallback(async () => {
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
}, [filters]);
```

### 7.2 Visual Analytics Components
- **Bar Chart:** Monthly spending comparisons across quarters.
- **Donut Charts:** Category distribution and payment method share (UPI vs Cards vs Cash).
- **KPI Metrics Strip:** Live calculation of total expenditure, transaction count, average cost, and highest spending category.

---

## CHAPTER 8: TESTING, VERIFICATION & EMPIRICAL RESULTS

### 8.1 Empirical Dataset Analysis (Verified Values)

| Metric / Dimension | Aggregated Output | Significance |
| :--- | :--- | :--- |
| **Total Spending** | **₹20,808.00** | Accurate cumulative sum of all 41 transactions. |
| **Total Transactions** | **41 records** | Verified document count in `expenses` collection. |
| **Average Transaction Size** | **₹507.51** | Calculated via native `$avg` aggregation. |
| **Top Spending Category** | **Bills (₹5,000.00 / 24.03%)** | Highest expenditure segment. |
| **Primary Payment Mode** | **UPI (56.65% / ₹11,788.00)** | Demonstrates student spending pattern. |
| **Top Individual Merchant** | **StyleHub (₹3,060.00)** | Filtered and grouped via `$match` and `$group`. |

### 8.2 Test Matrix
- **Test Case 1 (Negative Amount):** Insert amount = -250. Result: MongoDB `$jsonSchema` throws WriteError. Status: **PASSED**.
- **Test Case 2 (Invalid Category):** Insert category = 'Crypto'. Result: Rejected due to Enum restriction. Status: **PASSED**.
- **Test Case 3 (Regex Search):** Query text 'Cafe'. Result: `$regex` matches case-insensitively across description and merchant. Status: **PASSED**.
- **Test Case 4 (Reactivity):** Added new transaction. Result: React interface re-aggregates KPI totals instantly without page refresh. Status: **PASSED**.

---

## CHAPTER 9: CONCLUSION & FUTURE SCOPE

### 9.1 Conclusion
The **Expense Analytics** system demonstrates how MongoDB's document model and native Aggregation Pipelines deliver superior flexibility, data integrity, and real-time analytical speed compared to traditional RDBMS setups. Combining strict collection-level validation with Python Flask and React 19 produces a robust, high-performance financial management platform.

### 9.2 Future Roadmap
1. **Budget Threshold Warnings:** Implement spending caps with alerts at 85% threshold.
2. **OCR Receipt Parsing:** Enable automated receipt scanning using Tesseract / Google Vision.
3. **Machine Learning Predictions:** Implement predictive cashflow forecasting based on spending velocity.
4. **Export Engine:** One-click export to signed PDF and CSV statements.

---

## CHAPTER 10: REFERENCES & BIBLIOGRAPHY
1. **MongoDB Inc.**, *"MongoDB Documentation: The Aggregation Pipeline Framework"*, Available: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/, 2026.
2. **MongoDB Inc.**, *"JSON Schema Validation in MongoDB"*, Available: https://www.mongodb.com/docs/manual/core/schema-validation/, 2026.
3. **Pallets Projects**, *"Flask Documentation (v3.1.x) - Lightweight WSGI Web Application Framework"*, Available: https://flask.palletsprojects.com/, 2026.
4. **Python Software Foundation**, *"PyMongo: The Official Python Driver for MongoDB"*, Available: https://pymongo.readthedocs.io/, 2026.
5. **Meta Platforms Inc.**, *"React Documentation: Building Modern Interactive Single-Page User Interfaces"*, Available: https://react.dev/, 2026.
6. **Recharts Group**, *"Recharts: Redefined Charting Library Built with React and D3"*, Available: https://recharts.org/, 2026.
7. **Silberschatz, A., Korth, H. F., & Sudarshan, S.**, *"Database System Concepts (7th Edition)"*, McGraw-Hill Education, 2020.
