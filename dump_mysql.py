import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

host = os.getenv('MYSQL_DB_HOST')
database = os.getenv('MYSQL_DB_NAME')
username = os.getenv('MYSQL_DB_USER')
password = os.getenv('MYSQL_DB_PASSWORD')
port = os.getenv('MYSQL_DB_PORT')

def dump():
    if host is None or database is None or username is None or password is None or port is None:
        return logging.error("MYSQL_DB_HOST, MYSQL_DB_NAME, MYSQL_DB_USER, MYSQL_DB_PASSWORD, or MYSQL_DB_PORT is not set in the .env file")
    
    mysql_dump_dir = "mysql-dump"
    
    print(f"MYSQL_DUMP: {datetime.now()}: Starting MySQL dump")
    try:
        # Create the dump directory if it does not exist
        if not os.path.exists(mysql_dump_dir):
            os.makedirs(mysql_dump_dir)
            
        # Define the dump file name
        unix_timestamp = int(datetime.now().timestamp())
        dump_file_name = os.path.join(mysql_dump_dir, f"dump_{unix_timestamp}.sql")
            
        
        print(f"Dump file will be saved to: {dump_file_name}")

        # Define the mysqldump command
        mysqldump_command = [
            'mysqldump',
            f'--user={username}',
            f'--password={password}',
            f'--host={host}',
            f'--port={port}',
            '--no-tablespaces',
            database
        ]
        
        # Run the mysqldump command
        with open(dump_file_name, 'w') as dump_file:
            result = subprocess.run(mysqldump_command, stdout=dump_file, stderr=subprocess.PIPE, text=True)

        # Check if the dump was successful
        if result.returncode != 0:
            print(f"Error creating dump: {result.stderr}")
            return

        print(f"MYSQL_DUMP: {datetime.now()}: Finished MySQL dump")

    except Exception as error:
        print(f"MYSQL_DUMP: {datetime.now()}: Error during MySQL dump: {error}")

if __name__ == '__main__':
    dump()