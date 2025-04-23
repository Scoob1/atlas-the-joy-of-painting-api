# 🎨 The Joy of Painting: ETL & API Project

Welcome to the **atlas-the-joy-of-painting-api** project! This repository contains all the components needed to design a database, perform ETL operations, and build an API to serve episode data from the beloved show *The Joy of Painting with Bob Ross*.

---

## 📚 Project Overview

This project explores the **ETL process**—**Extract**, **Transform**, and **Load**—using multiple datasets with information about episodes, paint colors, and subject matter featured across all 403 episodes of *The Joy of Painting*. The goal is to help your local public broadcasting station create a **filterable database and API** for users who want to:

- Watch episodes from a specific **month**
- Find episodes based on **subject matter** (like “mountains” or “cabin”)
- Search for paintings featuring a particular **color palette**

---

## 🗂️ Resources

- `episode_data.csv` – Detailed info about each episode (season, episode number, air date, etc.)
- `color_details.csv` – Characteristics and descriptions of Bob Ross’s paint colors
- Additional subject matter dataset(s)

---

## 🚀 Tasks

### 0. Database Design

- Analyze all datasets and determine how they relate to one another
- Design a **relational database schema** (UML included)
- Write SQL scripts to initialize the database
- Ensure the database supports filtering by **month**, **subject**, and **color palette**

✅ *Complete – Schema and SQL files included*

---

### 1. Extract, Transform, Load (ETL)

- Extract data from raw CSV files
- Clean and normalize data for consistency
- Transform data to match schema format
- Load it into the SQL database

✅ *Complete – `etl/etl.py` handles data processing*

---

### 2. Build the API

- RESTful API to serve episode data from the database
- Support **multiple simultaneous filters**:
  - Filter by month, subject(s), color(s)
  - Support AND/OR logic between filters
- Accept parameters via URL, query string, or POST body
- Return results in **JSON format**

✅ *Complete – API code found in `api/` directory*

---

## ⚙️ Tech Stack

- **Python 3.9+**
- **MySQL 8.0** (or PostgreSQL optional)
- **Pandas** for data wrangling
- **Flask** or **FastAPI** for the API layer
- **Postman** for API testing

---

## 🧪 Example API Usage

**Filter by multiple colors and subjects:**
```
GET /episodes?colors=Phthalo+Blue,Alizarin+Crimson&subjects=Mountain,River
```

**Filter by month:**
```
GET /episodes?month=November
```

**Combine filters with AND/OR logic:**
```
POST /episodes/filter
Body: {
  "colors": ["Van Dyke Brown", "Titanium White"],
  "subjects": ["Cabin"],
  "month": "January",
  "filter_logic": "AND"
}
```

---

## 🧼 Data Quality Considerations

- Handled missing or inconsistent values
- Standardized date and color formatting
- Ensured no duplicates in normalized tables

---

## 📸 UML Diagram

Check out the `uml/db_design.png` file for the visual structure of the database, showing relationships between episodes, colors, and subjects.

---

## 🧑‍🎨 Author

Tamara Walling
