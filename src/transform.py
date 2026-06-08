import os
from sqlalchemy import create_engine, text
import toml

def get_engine():
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        with open(secrets_path, "r") as f:
            secrets = toml.load(f)
            if "DB_URL" in secrets:
                return create_engine(secrets["DB_URL"])
    db_url = os.getenv("DB_URL")
    return create_engine(db_url)

def execute_sql_file(file_path, engine):
    if not os.path.exists(file_path):
        print(f"⚠️ Berkas SQL '{file_path}' tidak ditemukan.")
        return
        
    with open(file_path, "r") as f:
        sql_content = f.read()
        
    # Memisahkan perintah sql berdasarkan titik koma
    queries = sql_content.split(";")
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            for query in queries:
                clean_query = query.strip()
                if clean_query:
                    connection.execute(text(clean_query))
            transaction.commit()
            print(f"✅ Sukses mengeksekusi berkas: {file_path}")
        except Exception as error:
            transaction.rollback()
            print(f"❌ Gagal memproses berkas {file_path}. Pembatalan dilakukan. Error: {error}")
            raise error

def main():
    engine = get_engine()
    print("=== MEMULAI TAHAP 2: TRANSFORMASI DATABASE CENTRIC (ELT) ===")
    
    print("[1/3] Merancang struktur database awal (Schema Data Warehouse)...")
    execute_sql_file("sql/schema.sql", engine)
    
    print("[2/3] Memproses data staging ke tabel Fakta & Dimensi (Cleansing & Loading)...")
    execute_sql_file("sql/transform.sql", engine)
    
    print("[3/3] Membangun Analytical Views cerdas untuk dashboard...")
    execute_sql_file("sql/views.sql", engine)
    
    print("=== PROSES ELT 100% SELESAI! DATA WAREHOUSE SIAP DIKONSUMSI ===")

if __name__ == "__main__":
    main()