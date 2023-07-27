import os
import psycopg2
import csv

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

# Columns to exclude from the CSV dump
excluded_columns = ["create_date", "write_date", "create_uid", "write_uid", "limit", "desc", "default", "binary", "group", "references", "password"]


def fetch_table_schema(cursor, table_name):
    # Get the list of columns and data types in the table
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
    return {row[0]: row[1] for row in cursor.fetchall()}


def are_schemas_equal(schema1, schema2):
    return schema1 == schema2


def fetch_table_data(cursor, table_name):
    # Get the list of columns in the table
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
    columns = [row[0] for row in cursor.fetchall()]

    # Filter columns excluding the ones to be excluded
    filtered_columns = [col for col in columns if col not in excluded_columns]

    # Fetch data from the database
    if 'id' in filtered_columns:
        query = f"SELECT {', '.join(filtered_columns)} FROM {table_name} ORDER BY id"
    else:
        query = f"SELECT {', '.join(filtered_columns)} FROM {table_name}"

    cursor.execute(query)
    return [tuple(row) for row in cursor.fetchall()]


def are_tables_equal(data1, data2):
    return data1 == data2

def export_schema_to_csv(schema1, schema2, table_name, db1_directory, db2_directory):
    output_file1 = os.path.join(db1_directory, f"{table_name}.schema.csv")
    output_file2 = os.path.join(db2_directory, f"{table_name}.schema.csv")

    with open(output_file1, "w", newline="") as csvfile1, open(output_file2, "w", newline="") as csvfile2:
        csvwriter1 = csv.writer(csvfile1)
        csvwriter2 = csv.writer(csvfile2)

        # Write header
        csvwriter1.writerow(["Column Name", "Data Type"])
        csvwriter2.writerow(["Column Name", "Data Type"])

        # Sort schema data by field names
        sorted_schema1 = sorted(schema1.items(), key=lambda x: x[0])
        sorted_schema2 = sorted(schema2.items(), key=lambda x: x[0])

        # Write sorted schema data to CSV files
        for col_name, data_type in sorted_schema1:
            csvwriter1.writerow([col_name, data_type])

        for col_name, data_type in sorted_schema2:
            csvwriter2.writerow([col_name, data_type])

    print(f"Exported schema for table '{table_name}' to {output_file1} and {output_file2}")


def export_table_to_csv(cursor1, cursor2, table_name, db1_directory, db2_directory):
    schema1 = fetch_table_schema(cursor1, table_name)
    schema2 = fetch_table_schema(cursor2, table_name)
    if not are_schemas_equal(schema1, schema2):
        print(f"Schema for table '{table_name}' is not equal in both databases. Exporting schema to CSV.")
        export_schema_to_csv(schema1, schema2, table_name, db1_directory, db2_directory)
    else:
        print(f"Schema for table '{table_name}' is equal in both databases. Skipping schema export.")

    data1 = fetch_table_data(cursor1, table_name)
    data2 = fetch_table_data(cursor2, table_name)

    if are_tables_equal(data1, data2):
        print(f"Table '{table_name}' has equal data in both databases. Skipping CSV export.")
        return

    output_file1 = os.path.join(db1_directory, f"{table_name}.csv")
    output_file2 = os.path.join(db2_directory, f"{table_name}.csv")

    with open(output_file1, "w", newline="") as csvfile1, open(output_file2, "w", newline="") as csvfile2:
        csvwriter1 = csv.writer(csvfile1)
        csvwriter2 = csv.writer(csvfile2)

        # Get the list of columns in the table
        cursor1.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = [row[0] for row in cursor1.fetchall()]

        # Filter columns excluding the ones to be excluded
        filtered_columns = [col for col in columns if col not in excluded_columns]

        # Write header
        csvwriter1.writerow(filtered_columns)
        csvwriter2.writerow(filtered_columns)

        # Write data to CSV files
        csvwriter1.writerows(data1)
        csvwriter2.writerows(data2)

    print(f"Exported table '{table_name}' to {output_file1} and {output_file2}")


def main():
    try:
        # Connect to the first PostgreSQL database
        conn1 = psycopg2.connect(**db_params1)
        cursor1 = conn1.cursor()

        # Connect to the second PostgreSQL database
        conn2 = psycopg2.connect(**db_params2)
        cursor2 = conn2.cursor()

        # Get the database names
        db_name1 = db_params1["database"]
        db_name2 = db_params2["database"]

        # Create directories if they don't exist
        if not os.path.exists(db_name1):
            os.makedirs(db_name1)
        if not os.path.exists(db_name2):
            os.makedirs(db_name2)

        # Export each table to separate CSV files for comparison
        cursor1.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor1.fetchall()]

        excluded_tables = ["muk_dms_file","stock_move"]
        for table in tables:
            print(table)
            if table in excluded_tables:
                print('Excluded: %s' % table)
                continue
            export_table_to_csv(cursor1, cursor2, table, db_name1, db_name2)

        # Close the database connections
        cursor1.close()
        conn1.close()
        cursor2.close()
        conn2.close()

        print("Data export completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
