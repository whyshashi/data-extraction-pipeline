#  Python extract, clean, visualize Pipeline (Tabula-Based)

This project implements a simple **ETL (Extract, Transform, Load)**
pipeline in Python using **Tabula** to extract tables from PDF files and
process them.

------------------------------------------------------------------------

##  Features
-   The pipeline is created for 2 tables segment_table on page 254, consolidated table on page 239.
-   Extract tables from PDF files using Tabula
-   Transform extracted data using Python
-   Clean and modular structure
-   Store all csv, clean csv files, llm results inside the outputs folder.

------------------------------------------------------------------------

## 🛠 Requirements

-   Python 3+
-   Java Runtime Environment (required by Tabula)
-   pip
-   GOOGLE_API_KEY in .env

------------------------------------------------------------------------

##  Setup Instructions

###  Create a Virtual Environment

``` bash
python -m venv venv
```

###  Activate the Virtual Environment

####  Windows

``` bash
.\venv\Scripts\activate.bat
```

####  macOS / Linux

``` bash
source venv/bin/activate
```

###  Install Dependencies

``` bash
pip install -r requirements.txt
```

###  GOOGLE_API_KEY

add GOOGLE_API_KEY in .env for llm.

------------------------------------------------------------------------

##  Running the Pipeline

``` bash
python app.py
```

------------------------------------------------------------------------

##  Project Structure

    project-root/
    │
    ├── app.py
    ├── requirements.txt
    ├── docs/
    ├── main.py
    ├── outputs/
    ├── extract_table.py
    ├── clean_col.py
    ├── clean.py
    ├── graphplot.py
    ├── llmgenerated_insights.py
    └── README.md

------------------------------------------------------------------------

## 🔎 How It Works

1.  **Extract** -- Use Tabula to extract tables from PDF files\
2.  **clean** -- Clean and process data using Python\
3.  **plot** -- plot data 
4.  **Ensights** -- generate ensights using llm

------------------------------------------------------------------------

## ⚠️ Important Notes

-   Ensure **Java** is installed and added to your system PATH.
-   Verify Java installation:

``` bash
java -version
```

------------------------------------------------------------------------

## 📌 Example Dependencies (requirements.txt)

    tabula-py
    pandas
    numpy
