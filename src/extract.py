import os
import pandas as pd
from sqlalchemy import create_engine
import toml

def get_engine():
    # Mengambil DB URL langsung dari secrets Streamlit demi konsistensi data
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        with open(secrets_path, "r") as f:
            secrets = toml.load(f)
            if "DB_URL" in secrets:
                return create_engine(secrets["DB_URL"])
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL tidak ditemukan di .streamlit/secrets.toml maupun Environment Variable.")
    return create_engine(db_url)

def extract_to_staging():
    engine = get_engine()
    # Peta berkas CSV masukan mentah
    data_files = {
        "produk": "data/produk.csv",
        "apotek": "data/apotek.csv",
        "pelanggan": "data/pelanggan.csv",
        "karyawan": "data/karyawan.csv",
        "supplier": "data/supplier.csv",
        "penjualan": "data/penjualan.csv"
    }
    
    print("=== MEMULAI TAHAP 1: EXTRACT & LOAD DATA MENTAH KE STAGING ===")
    for table, path in data_files.items():
        if not os.path.exists(path):
            print(f"⚠️ Berkas '{path}' tidak ditemukan di lokal. Dilewati.")
            continue
            
        df = pd.read_csv(path)
        df = df.drop_duplicates()
        df.columns = df.columns.str.replace(' ', '').str.strip().str.lower()

        if table == "penjualan":
            df = df.rename(columns={
                "id_faktur": "fakturid",
                "tgl_trx": "tanggal",
                "kode_barang": "produkid",
                "id_apotek": "apotekid",
                "kasir_id": "karyawanid",
                "harga_satuan": "hargasatuan"
            })
            df["tanggal"] = pd.to_datetime(
                df["tanggal"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            ).dt.strftime("%Y-%m-%d")

        elif table == "produk":
            df = df.rename(columns={
                "nama_produk": "namaproduk"
            })

        print(f"\n=== KOLOM {table.upper()} ===")
        print(df.columns.tolist())
        
        staging_table_name = f"stg_{table}"
        # Kirim utuh langsung tanpa pengubahan record data ke Supabase
        df.to_sql(staging_table_name, engine, if_exists="replace", index=False)
        print(f"✅ Sukses mengunggah {path} ke tabel '{staging_table_name}' [{len(df)} baris]")
    print("=== TAHAP EXTRACT & LOAD SELESAI ===")

if __name__ == "__main__":
    extract_to_staging()