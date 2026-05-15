import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres+psycopg.qngaklwvwyhsjseiyjcm:TS07GN9547_28@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres")
