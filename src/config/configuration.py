from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')

BOT_EMAIL_USERNAME = os.getenv('BOT_EMAIL_USERNAME')
BOT_EMAIL_PASSWORD = os.getenv('BOT_EMAIL_PASSWORD')

DB_CONN = {
    'db_name': os.getenv('DB_NAME'),
    'db_user': os.getenv('DB_USER'),
    'db_pass': os.getenv('DB_PASSWORD'),
    'db_host': os.getenv('DB_HOST'),
    'db_port': os.getenv('DB_PORT'),
}
