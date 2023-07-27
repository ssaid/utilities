# Database Schema and Data Export Script

This script is a Python program designed to compare the schema and data between two PostgreSQL databases and export the differences to CSV files for further analysis. It establishes connections to two databases and iterates through the tables in one of the databases (devel_original) to compare their schema and data with the corresponding tables in the other database (devel). The script then exports the differences to separate CSV files.

## Prerequisites

- Python 3.x
- `psycopg2` library (for PostgreSQL database connections)
- Access to the two PostgreSQL databases

## Setup

1. Install the required dependencies by running the following command:
   ```
   pip install psycopg2
   ```

2. Modify the database connection parameters in the script to match the details of your PostgreSQL databases:

   ```python
   # PostgreSQL database connection parameters for the first database
   db_params1 = {
       "host": "127.0.0.1",
       "database": "devel_original",
       "user": "user",
       "password": "password"
   }

   # PostgreSQL database connection parameters for the second database
   db_params2 = {
       "host": "127.0.0.1",
       "database": "devel",
       "user": "user",
       "password": "password"
   }
   ```

   Replace `host`, `database`, `user`, and `password` with the appropriate values for your databases.

3. Optionally, specify any columns to be excluded from the data export in the `excluded_columns` list:

   ```python
   excluded_columns = ["create_date", "write_date", "create_uid", "write_uid", "limit", "desc", "default", "binary", "group", "references", "password"]
   ```

   These columns will be excluded from the CSV dump when exporting data.

## How to Use

1. Save the modified script to a file, e.g., `database_export_script.py`.

2. Open a terminal or command prompt and navigate to the directory containing the script.

3. Run the script using Python:

   ```
   python database_export_script.py
   ```

   The script will connect to the two databases, compare the schema and data for each table, and export the differences to CSV files. If there are no differences, the script will skip the export for that particular table.

4. The CSV files will be exported to directories named after the respective database names, and each table's schema and data will be saved in separate CSV files.

## Note

- The script assumes that both databases are accessible and the user has appropriate privileges to access the schema and data of the tables.

- Tables listed in the `excluded_tables` list will be skipped from the comparison and export process. Modify this list if you want to exclude specific tables from the comparison.

- Please exercise caution when handling sensitive data, and ensure that you have the necessary permissions before running the script on production databases.

- The script does not handle database schema changes during the export process. To ensure accurate results, run the script when the databases have consistent and stable schemas.

- If any errors occur during the script execution, relevant error messages will be displayed, and the script will terminate.

- For large databases, the script may take some time to complete the export process. Be patient and let the script finish the comparison and export tasks.

---

**Important:** Always backup your databases before running any scripts that modify or export data. This script is provided as a tool to help with schema and data comparison, and it is your responsibility to ensure its proper usage and validation in your specific use case. The authors and maintainers of this script disclaim any liability for any damages or data loss caused by the use or misuse of this script.
