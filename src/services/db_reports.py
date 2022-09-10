import psycopg2 as ps
import psycopg2.extras
import pandas as pd
from sqlalchemy import create_engine


class ReportWorker:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, echo=True)

    def extract_data(self, user_id):
        df = pd.read_sql(f'''
        select * from telegram_bot.TodayExpense
        where telegraid = '{user_id}'
        ''', con=self.engine)

        return df

    def make_report(self):
        pass

    def send_report_to_user(self):
        pass
