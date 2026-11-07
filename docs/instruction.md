# Cold Chain Logistics AI Assistant

## Project Setup & Implementation Instructions

This project follows an end-to-end AI Forward Deployed Engineer (FDE) architecture inspired by Krish Naik's implementation.

**Infrastructure adaptation:** Instead of hosting SQL Server on AWS EC2, we run SQL Server 2022 locally using Docker Desktop. This keeps development costs low while preserving the database ingestion workflow.

---

# Phase 1: Project Environment

### 1. Project Structure

```text
cold-chain-logistics/
│
├── data/
│   ├── raw/
│   │   └── dynamic_supply_chain_logistics_dataset.csv
│   │
│   └── source/
│       └── data.txt
│
├── docs/
│   └── instruction.md
│
├── scripts/
│   └── ingest_legacy_data.py
│
├── .env
├── .gitignore
└── requirements.txt
```

### 2. Python Environment

Use Anaconda Prompt or an initialized PowerShell terminal.

```bash
conda create -n cold-chain python=3.12 -y
conda activate cold-chain
```

Navigate to the project:

```bash
cd /d D:\Desktop\cold-chain-logistics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify Python:

```bash
python --version
```

Expected: Python 3.12.x

---

# Phase 2: Local SQL Server Setup Using Docker

### 1. Download SQL Server 2022 Image

```bash
docker pull mcr.microsoft.com/mssql/server:2022-latest
```

### 2. Create Persistent Docker Volume

```bash
docker volume create sqlserver-data
```

The volume stores database files separately from the container.

### 3. Start SQL Server Container

For a fresh installation:

```bash
docker run -d \
  --name sqlserver \
  -e ACCEPT_EULA=Y \
  -e MSSQL_SA_PASSWORD="YOUR_STRONG_PASSWORD" \
  -p 1433:1433 \
  -v sqlserver-data:/var/opt/mssql \
  mcr.microsoft.com/mssql/server:2022-latest
```

Note: This is the initial setup command. Do not execute it again if the `sqlserver` container already exists.

### 4. Verify Container

```bash
docker ps
```

If the container is stopped:

```bash
docker start sqlserver
```

### 5. Check SQL Server Version

```bash
docker exec -it sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -C
```

Enter the SQL Server password when prompted.

Execute:

```sql
SELECT @@VERSION;
GO
```

---

# Phase 3: Create Project Database

Inside SQL Server, execute:

```sql
CREATE DATABASE ColdChainLogistics;
GO
```

Verify:

```sql
SELECT name FROM sys.databases;
GO
```

Switch to the project database:

```sql
USE ColdChainLogistics;
GO
```

Our target database is:

`ColdChainLogistics`

---

# Phase 4: Configure Python Database Connectivity

### 1. Install Microsoft ODBC Driver 18

Install Microsoft ODBC Driver 18 for SQL Server (Windows x64).

Official documentation:

https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### 2. Install Python Database Libraries

```bash
pip install pyodbc sqlalchemy python-dotenv
```

### 3. Verify ODBC Driver

```bash
python -c "import pyodbc; print(pyodbc.drivers())"
```

Expected output should include:

```text
ODBC Driver 18 for SQL Server
```

### 4. Configure Environment Variables

Create or update the project's `.env` file:

```env
SQL_SERVER_HOST=localhost
SQL_SERVER_PORT=1433
SQL_ADMIN_USER=sa
SQL_ADMIN_PASSWORD=YOUR_SQL_SERVER_PASSWORD
```

Never commit `.env` or expose database credentials.

### 5. Database Connectivity Architecture

```text
Python Application
       |
       v
   SQLAlchemy
       |
       v
     pyodbc
       |
       v
 ODBC Driver 18
       |
       v
 SQL Server 2022
       |
       v
ColdChainLogistics
```

---

# Phase 5: Legacy Data Ingestion

### 1. Dataset

Dataset:

`data/raw/dynamic_supply_chain_logistics_dataset.csv`

Source:

https://www.kaggle.com/datasets/datasetengineer/logistics-and-supply-chain-dataset

### 2. Data Ingestion Script

Script location:

`scripts/ingest_legacy_data.py`

Responsibilities:

1. Load environment variables.
2. Read the raw CSV using Pandas.
3. Select relevant logistics columns.
4. Rename columns into a legacy enterprise-style schema.
5. Add a system ingestion flag.
6. Establish a SQL Server connection using SQLAlchemy and pyodbc.
7. Insert records into SQL Server.

### 3. Target Table

Database:

`ColdChainLogistics`

Schema:

`dbo`

Table:

`TBL_SC_FLEET_HIST_RAW`

The ingestion script uses:

```python
df_legacy.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False,
    schema='dbo'
)
```

Note: `replace` drops and recreates the table if it already exists. Use carefully when preserving existing records.

### 4. Execute Ingestion

Activate the Conda environment and navigate to the project directory.

```bash
conda activate cold-chain
```

```bash
python scripts/ingest_legacy_data.py
```

Expected output:

```text
Loading CSV...
Connecting to legacy MSSQL Database...
Ingesting into TBL_SC_FLEET_HIST_RAW...
Legacy data ingestion complete!
```

---

# Phase 6: Validate Ingested Data

Connect to SQL Server:

```bash
docker exec -it sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -C
```

Switch database:

```sql
USE ColdChainLogistics;
GO
```

Check available tables:

```sql
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';
GO
```

Check total records:

```sql
SELECT COUNT(*) AS TotalRecords
FROM dbo.TBL_SC_FLEET_HIST_RAW;
GO
```

Preview records:

```sql
SELECT TOP 10 *
FROM dbo.TBL_SC_FLEET_HIST_RAW;
GO
```

Check columns:

```sql
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'TBL_SC_FLEET_HIST_RAW';
GO
```

---

### Connecting to the Database

Frostline uses **Microsoft SQL Server 2022 Developer Edition** running locally inside a Docker container.

We use the Microsoft **SQL Server (mssql)** extension in Visual Studio Code to connect to and manage the database.

### 1. Database Environment

| Component | Configuration |
|---|---|
| Database Engine | Microsoft SQL Server 2022 |
| Edition | Developer Edition |
| Runtime | Docker Desktop |
| Container Name | `sqlserver` |
| Host | `localhost` |
| Port | `1433` |
| Database | `ColdChainLogistics` |
| Authentication | SQL Login |
| Username | `sa` |
| VS Code Extension | SQL Server (mssql) by Microsoft |

### 2. Start SQL Server

Ensure Docker Desktop is running.

Check the SQL Server container:

```powershell
docker ps
```

If the container is stopped, start it:

```powershell
docker start sqlserver
```

### 3. Connect Through VS Code

Install the **SQL Server (mssql)** extension published by Microsoft.

Open the Command Palette (`Ctrl + Shift + P`) and select:

`MS SQL: Connect`

Use the following connection settings:

- Profile Name: `Frostline Local SQL Server`
- Server Name: `localhost`
- Port: `1433`
- Authentication Type: `SQL Login`
- Username: `sa`
- Password: Your local SQL Server password
- Database: `ColdChainLogistics`
- Trust Server Certificate: Enabled
- Encrypt: Optional

Test the connection and click Connect.

### 4. Verify the Database Connection

Open a new SQL query in VS Code and execute:

```sql
SELECT DB_NAME() AS CurrentDatabase, COUNT(*) AS TotalRecords FROM dbo.TBL_SC_FLEET_HIST_RAW;
```

Expected database: `ColdChainLogistics`

Expected record count: `32065`

### 5. Database Explorer

Use the SQL Server panel in VS Code to explore:

- Tables
- Views
- Synonyms
- Programmability
- External Resources

The existing legacy table is:

`dbo.TBL_SC_FLEET_HIST_RAW`

### 6. Python Database Connectivity

Python connects to SQL Server through the following stack:

`Python → SQLAlchemy → pyodbc → ODBC Driver 18 → SQL Server`

Database connection settings are stored in the project's `.env` file. Never commit database credentials to GitHub.

### 7. Important Notes

- SQL Server runs locally through Docker; it is not hosted on AWS.
- The SQL Server data volume persists database files across container restarts.
- VS Code is our primary interface for writing and executing SQL queries.
- Python is used for data ingestion, transformation, analytics and machine learning.
- Azure Data Studio is not required for this project.
- Keep sensitive credentials in `.env` and exclude the file through `.gitignore`.
