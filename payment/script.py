from django.db import connection

def truncate_table_sqlite(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'DELETE FROM {table_name};')  # Delete all rows

        # Optionally, reset the auto-increment primary key (if needed)
        cursor.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{table_name}";')
