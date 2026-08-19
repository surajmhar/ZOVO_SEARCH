# ZOVO SEARCH

**ZOVO SEARCH** is a full-stack, AI-driven SEO agency website and SEO analysis platform built with **Python and Flask**.

The platform combines a professional SEO agency website with a functional SEO analyzer that can inspect public websites, calculate SEO scores, identify optimization issues, and generate recommendations.

Registered users can create accounts, run SEO analyses, store their analysis history, and view personalized SEO statistics through a protected dashboard.

---

## 📌 Project Overview

Many website owners, startups, and small businesses struggle to understand the SEO problems affecting their websites.

Professional SEO tools can be expensive, complex, or difficult for beginners to understand.

ZOVO SEARCH aims to provide a simple and accessible platform where users can analyze important SEO factors, understand their website's SEO health, and identify opportunities to improve search visibility.

The project currently functions as a **working full-stack prototype**.

---

## 🎯 Problem Statement

Website owners often face problems such as:

- Poor search engine visibility
- Missing or poorly optimized metadata
- Incorrect heading structures
- Technical SEO issues
- Missing image alternative text
- Mobile optimization problems
- Lack of understandable SEO recommendations
- Difficulty tracking previous SEO analyses

Many existing SEO platforms also contain advanced features that may be overwhelming for beginners.

ZOVO SEARCH provides a simpler interface for performing basic SEO analysis and understanding important optimization opportunities.

---

## 💡 Proposed Solution

ZOVO SEARCH provides a web-based SEO analysis system that can:

- Accept a public website URL
- Fetch and analyze the webpage
- Inspect important SEO elements
- Calculate SEO category scores
- Generate optimization recommendations
- Display results through a modern interface
- Store analysis history for authenticated users
- Calculate personalized dashboard statistics
- Allow visitors to submit SEO project enquiries

---

# ✨ Core Features

## 🌐 Professional SEO Agency Website

The public website currently includes:

- Home Page
- About Page
- Services Page
- Portfolio Page
- Contact Page
- SEO Analyzer
- Login Page
- Registration Page
- User Dashboard

The interface follows a modern SaaS-inspired visual style with responsive layouts, animations, and reusable components.

---

## 🔍 SEO Analyzer

ZOVO SEARCH includes a custom backend SEO analyzer.

Users can enter a public website URL and receive an SEO report based on multiple website signals.

The current analyzer checks information including:

- Page title
- Title length
- Meta description
- Meta description length
- H1 headings
- H2 headings
- HTTPS availability
- Canonical tag
- Robots meta directives
- Mobile viewport
- Image alt attributes
- Internal links
- External links
- Page content / word count
- Website response time

The analyzer generates multiple scores:

- Overall SEO Score
- Performance Score
- On-Page SEO Score
- Technical SEO Score
- Mobile SEO Score

It also produces recommendations based on detected SEO issues.

---

## 📊 SEO Recommendations

Depending on the website analysis, ZOVO SEARCH can identify issues such as:

- Missing meta descriptions
- Poor title length
- Missing canonical tags
- Limited page content
- Missing image alt attributes
- SEO structure problems

Recommendations are returned together with the SEO analysis result.

---

# 👤 User Authentication

ZOVO SEARCH includes a complete basic authentication system using **Flask-Login**.

Users can:

- Create an account
- Login
- Logout
- Access protected pages
- Maintain a logged-in session

The registration system includes validation for:

- Required fields
- Password confirmation
- Minimum password length
- Duplicate email addresses

Passwords are not stored as plain text. Password hashing is used before credentials are stored in the database.

---

# 📈 User Dashboard

Authenticated users receive access to a protected personal dashboard.

The dashboard currently displays:

- User account information
- Total SEO analyses
- Average SEO score
- Best SEO score
- Recent SEO analysis history
- Overall scores
- Performance scores
- On-Page SEO scores
- Technical SEO scores
- Mobile SEO scores
- Analysis dates

Each user's analysis history is associated with their own account.

---

# 👥 Guest Analyzer Access

The SEO Analyzer is publicly accessible.

This means visitors can analyze a website without creating an account.

However:

**Guest analysis results are not stored in a registered user's analysis history.**

When an authenticated user performs an SEO analysis, the analysis is automatically associated with that user and saved to the database.

This creates the following workflow:

```text
Guest User
    ↓
SEO Analyzer
    ↓
Website Analysis
    ↓
SEO Results
    ↓
Result Displayed
    ↓
Not Stored in User History
```

For authenticated users:

```text
Registered User
      ↓
Login
      ↓
SEO Analyzer
      ↓
Website Analysis
      ↓
SEO Results
      ↓
Database Storage
      ↓
Personal Dashboard
```

---

# 📩 Contact Enquiry System

ZOVO SEARCH includes a functional contact enquiry system.

Visitors can provide:

- Name
- Email address
- Website URL
- Required SEO service
- Project message

The frontend submits the enquiry to the Flask backend.

The backend validates the request and stores successful enquiries in the database.

Users receive a success or error message without being redirected to a raw API response.

---

# 🛠 Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates
- Lucide Icons
- AOS (Animate On Scroll)
- Google Fonts

## Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login

## Database

- SQLite
- SQLAlchemy ORM

## SEO Analysis

The project uses a custom Python-based SEO analysis module that retrieves public webpages and processes important HTML and technical SEO signals.

---

# 🏗 System Architecture

The general application architecture is:

```text
USER
 │
 ▼
FRONTEND
HTML + CSS + JavaScript + Jinja2
 │
 ▼
FLASK APPLICATION
 │
 ├───────────────┬─────────────────┬──────────────────┐
 │               │                 │                  │
 ▼               ▼                 ▼                  ▼
Authentication   SEO Analyzer      Contact System     Dashboard
 │               │                 │                  │
 └───────────────┴─────────────────┴──────────────────┘
                         │
                         ▼
                  SQLAlchemy ORM
                         │
                         ▼
                  SQLite Database
```

---

# 🔎 SEO Analysis Workflow

```text
User Enters Website URL
          ↓
Frontend Analyzer Form
          ↓
POST /api/analyze
          ↓
Flask Backend
          ↓
SEO Analyzer Module
          ↓
Fetch Public Website
          ↓
Analyze SEO Signals
          ↓
Calculate Scores
          ↓
Generate Recommendations
          ↓
Return JSON Response
          ↓
Frontend Displays SEO Report
          ↓
Is User Authenticated?
       /          \
     YES           NO
      ↓             ↓
Save Analysis     Do Not Save
      ↓
User Dashboard
```

---

# 🗄 Database

The current prototype uses **SQLite** with **SQLAlchemy ORM**.

The database currently contains three main tables.

## 👤 users

Stores registered user account information.

It is responsible for user authentication and account identification.

---

## 📊 seo_analyses

Stores SEO analysis history for authenticated users.

Each saved analysis is linked to a user through a user ID.

Stored information includes SEO scores and the analyzed website URL.

---

## 📩 contact_messages

Stores enquiries submitted through the website contact form.

---

# 📁 Project Structure

The project follows a modular Flask structure.

```text
ZOVO_SEARCH/
│
├── analyzer/
│   ├── __init__.py
│   └── seo_analyzer.py
│
├── database/
│   ├── __init__.py
│   └── zovo_search.db
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── seo_analysis.py
│   └── contact_message.py
│
├── static/
│   │
│   ├── css/
│   │   ├── style.css
│   │   ├── navbar.css
│   │   ├── hero.css
│   │   ├── services.css
│   │   ├── about.css
│   │   ├── contact-page.css
│   │   ├── analyzer-page.css
│   │   ├── auth.css
│   │   ├── dashboard.css
│   │   └── ...
│   │
│   ├── js/
│   │   ├── script.js
│   │   ├── analyzer-page.js
│   │   ├── contact-page.js
│   │   └── ...
│   │
│   └── images/
│
├── templates/
│   │
│   ├── components/
│   │   ├── navbar.html
│   │   └── footer.html
│   │
│   ├── layout/
│   │   └── base.html
│   │
│   ├── pages/
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── services.html
│   │   ├── portfolio.html
│   │   ├── contact.html
│   │   ├── analyzer.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   │
│   └── sections/
│       ├── auth/
│       ├── contact/
│       ├── analyzer/
│       ├── dashboard/
│       └── ...
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🔐 Authentication Flow

```text
New User
   ↓
Registration Form
   ↓
Input Validation
   ↓
Duplicate Email Check
   ↓
Password Hashing
   ↓
Database
   ↓
User Account Created
   ↓
Authenticated Session
```

Existing user:

```text
Login Form
    ↓
Find User by Email
    ↓
Verify Password Hash
    ↓
Flask-Login
    ↓
Authenticated Session
    ↓
Protected Dashboard Access
```

---

# 🧪 Prototype Testing

The core functionality of ZOVO SEARCH Prototype V1 has been manually tested.

## Authentication Testing

Successfully tested:

- User registration
- Required field validation
- Duplicate email protection
- Password confirmation validation
- Password length validation
- Valid login
- Invalid login handling
- Logout
- Protected dashboard access

## SEO Analyzer Testing

Successfully tested:

- Public website analysis
- Different websites generating different results
- SEO score calculation
- Category score generation
- SEO recommendation generation
- Analyzer frontend/backend communication

## Analysis History Testing

Successfully tested:

- Logged-in analysis database storage
- User-specific analysis history
- Total analysis calculation
- Average score calculation
- Best score calculation
- Recent analysis display

## Guest Analyzer Testing

Successfully tested:

- Analyzer access without login
- Guest website analysis
- Guest results displayed normally
- Guest analyses not stored in registered user history

## Contact Testing

Successfully tested:

- Contact form submission
- Backend request processing
- Success response
- Database storage
- Contact record retrieval

---

# 🔄 Complete Prototype Workflow

The current full-stack workflow is:

```text
Visitor
   ↓
Explore ZOVO SEARCH
   ↓
Use Free SEO Analyzer
   │
   ├── Guest → View Results
   │
   └── Registered User
             ↓
           Login
             ↓
       Analyze Website
             ↓
       SEO Backend Engine
             ↓
         SEO Scores
             ↓
        Recommendations
             ↓
        Save Analysis
             ↓
          Database
             ↓
       Personal Dashboard
             ↓
        Analysis History
```

---

# ⚠️ Current Limitations

ZOVO SEARCH Prototype V1 is an academic and functional prototype.

The current SEO analyzer focuses on selected on-page and technical SEO signals and does not attempt to replace enterprise SEO platforms.

The current version does not yet include every advanced SEO metric or external SEO data source.

---

# Future Enhancements

Future versions of ZOVO SEARCH may include:

- Google PageSpeed Insights API
- Core Web Vitals
- Advanced performance auditing
- XML sitemap analysis
- Advanced robots.txt analysis
- Structured data / Schema validation
- Broken link detection
- Keyword density and keyword analysis
- Search intent analysis
- Advanced content quality analysis
- AI-generated SEO recommendations
- Competitor SEO comparison
- SEO report comparison over time
- Downloadable PDF SEO reports
- Email reports
- User profile management
- Password recovery
- Email verification
- Admin dashboard
- Contact enquiry management
- Advanced analytics
- Production deployment
- Cloud database integration

---

# 📌 Project Category

ZOVO SEARCH can be categorized as a:

**Full-Stack Web Application + SEO Analysis Platform + AI-Driven SEO Agency Website**

---

# 📊 Development Status

### 🟢 Prototype V1 — Functional

The following major components are operational:

**Frontend ✅**

**Flask Backend ✅**

**SQLite Database ✅**

**SEO Analyzer Backend ✅**

**SEO Scoring System ✅**

**SEO Recommendations ✅**

**User Registration ✅**

**User Login / Logout ✅**

**Protected Dashboard ✅**

**SEO Analysis History ✅**

**Dashboard Statistics ✅**

**Guest Analyzer Access ✅**

**Contact Enquiry Backend ✅**

**Dynamic Authentication Navbar ✅**

The project remains open for advanced feature development and production-level improvements.

---

# 👨‍💻 Developer

**Suraj Mahar**

ZOVO SEARCH was developed as a full-stack web project focused on combining modern web development with practical Search Engine Optimization analysis.

---

## ⭐ ZOVO SEARCH

**Analyze. Understand. Optimize. Grow.**
