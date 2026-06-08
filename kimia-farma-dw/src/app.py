import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ============================================================
# 1. KONFIGURASI HALAMAN UTAMA DASHBOARD
# ============================================================
st.set_page_config(
    page_title="Kimia Farma DW Platform",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. KONEKSI DATABASE SUPABASE (via secrets.toml)
# ============================================================
@st.cache_resource
def init_db_engine():
    return create_engine(st.secrets["DB_URL"])

engine = init_db_engine()

# ============================================================
# 3. GLOBAL CUSTOM CSS
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .main { background-color: #F0F4FF; }
    .block-container { padding-top: 1.8rem; padding-bottom: 2rem; }

    /* Header Halaman */
    .page-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 60%, #3B82F6 100%);
        border-radius: 16px;
        padding: 2rem 2.4rem 1.8rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.18);
    }
    .page-header .main-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 0.3rem;
    }
    .page-header .sub-title {
        font-size: 0.92rem;
        color: rgba(255,255,255,0.72);
        font-weight: 500;
    }

    /* KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #E0E7FF;
        border-radius: 14px;
        padding: 1.3rem 1.2rem;
        box-shadow: 0 2px 12px rgba(30,58,138,0.07);
        text-align: center;
        transition: box-shadow 0.2s;
    }
    .kpi-card:hover { box-shadow: 0 6px 24px rgba(30,58,138,0.13); }
    .kpi-icon { font-size: 1.6rem; margin-bottom: 0.4rem; }
    .kpi-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1E3A8A;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -1px;
    }
    .kpi-lbl {
        font-size: 0.75rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 5px;
    }
    .kpi-badge {
        display: inline-block;
        background: #EEF2FF;
        color: #4F46E5;
        font-size: 0.7rem;
        font-weight: 700;
        border-radius: 999px;
        padding: 2px 8px;
        margin-top: 6px;
    }

    /* Info Boxes */
    .info-box {
        background: #EEF2FF;
        border-left: 4px solid #4F46E5;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #1E3A8A;
        font-size: 0.92rem;
    }
    .success-box {
        background: #F0FDF4;
        border-left: 4px solid #22C55E;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #166534;
        font-size: 0.92rem;
    }

    /* Section Label */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #6366F1;
        margin-bottom: 0.5rem;
    }

    /* Pipeline Steps */
    .pipeline-step {
        background: #ffffff;
        border: 1px solid #E0E7FF;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 1px 6px rgba(30,58,138,0.05);
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }
    .step-badge {
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        color: white;
        font-weight: 800;
        font-size: 0.8rem;
        border-radius: 8px;
        padding: 0.3rem 0.6rem;
        white-space: nowrap;
        font-family: 'JetBrains Mono', monospace;
    }
    .step-content h4 {
        margin: 0 0 0.2rem;
        font-size: 0.95rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .step-content p {
        margin: 0;
        font-size: 0.86rem;
        color: #4B5563;
        line-height: 1.55;
    }
    .step-content code {
        background: #EEF2FF;
        color: #4F46E5;
        border-radius: 4px;
        padding: 1px 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #1E3A8A !important;
    }
    [data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.88) !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 4. NAVIGASI SIDEBAR (3 HALAMAN)
# ============================================================
with st.sidebar:
    st.markdown("### 💊 Kimia Farma DW")
    st.markdown("---")
    menu_selection = st.radio(
        "Pilih Halaman:",
        ["🏠 Profil Proyek", "📊 OLAP Business Insight", "⚙️ Aliran Pipeline ETL"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.75rem; color:rgba(255,255,255,0.45); text-align:center;">Universitas Padjadjaran · 2024</p>',
        unsafe_allow_html=True
    )

# ============================================================
# PAGE 1: PROFIL PROYEK
# ============================================================
if menu_selection == "🏠 Profil Proyek":

    st.markdown("""
        <div class="page-header">
            <div class="main-title">💻 Ekosistem Data Warehouse Ritel Apotek</div>
            <div class="sub-title">Studi Kasus Jaringan Distribusi Internal Kimia Farma · Star Schema OLAP</div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<div class="section-label">Gambaran Arsitektur Sistem</div>', unsafe_allow_html=True)
        st.markdown("""
        Proyek ini mengimplementasikan arsitektur Data Warehouse berbasis **Star Schema** OLAP yang berjalan di **cloud Supabase PostgreSQL**. Data operasional diekstraksi melalui pipeline Python, dimuat ke staging area, ditransformasikan menjadi tabel dimensi dan fakta menggunakan SQL, kemudian dikonsumsi oleh dashboard Business Intelligence berbasis Streamlit.

        Pendekatan **ELT (Extract → Load → Transform**) digunakan untuk memuat data mentah ke staging area terlebih dahulu, kemudian mentransformasikannya menjadi model dimensional yang terdiri dari 6 tabel dimensi dan 1 tabel fakta, sehingga query analitik 
        bernilai bisnis tinggi dapat dieksekusi secara efisien tanpa membebani sumber daya server inti.
        """)

        st.markdown('<div class="section-label" style="margin-top:1.2rem">Skema Dimensional (Star Schema)</div>', unsafe_allow_html=True)
        schema_cols = st.columns(3)
        dim_tables = [
            ("dim_produk", "Produk & Obat"),
            ("dim_apotek", "Cabang Apotek"),
            ("dim_pelanggan", "Data Pelanggan"),
            ("dim_karyawan", "Staf & Kasir"),
            ("dim_supplier", "Mitra Supplier"),
            ("dim_waktu", "Kalender Waktu"),
        ]
        for i, (tbl, lbl) in enumerate(dim_tables):
            with schema_cols[i % 3]:
                st.markdown(
                    f'<div class="info-box" style="margin:0.3rem 0; padding:0.6rem 0.9rem;">'
                    f'<code style="background:transparent; color:#4F46E5; font-size:0.78rem;">{tbl}</code>'
                    f'<br><span style="font-size:0.82rem; color:#374151;">{lbl}</span></div>',
                    unsafe_allow_html=True
                )

        st.markdown('<div class="section-label" style="margin-top:1.2rem">Informasi Akademik</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        📚 <strong>Mata Kuliah:</strong> Data Warehouse<br>
        🎓 <strong>Program Studi:</strong> Teknik Informatika<br>
        🏛️ <strong>Institusi:</strong> Universitas Padjadjaran
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-label">Tim Pengembang</div>', unsafe_allow_html=True)
        members = [
            ("👩‍💻", "Fadhila Latsa Tsabita", "140810230005"),
            ("👨‍💻", "Adelia Felisha Putri", "140810230003"),
            ("👨‍💻", "Muhammad Ainur Rafiq Noantaria", "140810230009"),
        ]
        for icon, name, role in members:
            st.markdown(
                f'<div class="pipeline-step" style="padding:0.8rem 1rem; margin-bottom:0.5rem;">'
                f'<span style="font-size:1.4rem">{icon}</span>'
                f'<div><div style="font-weight:700; font-size:0.88rem; color:#1E3A8A;">{name}</div>'
                f'<div style="font-size:0.78rem; color:#6B7280;">{role}</div></div></div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="section-label" style="margin-top:1rem">Status Sistem</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="success-box">
        🟢 <strong>Status Koneksi:</strong> OLAP Supabase Terkoneksi<br>
        🗄️ <strong>Database:</strong> PostgreSQL via Supabase<br>
        📡 <strong>Mode Akses:</strong> SQLAlchemy Connection Pool<br>
        🔐 <strong>Kredensial:</strong> Disimpan di <code style="background:transparent; color:#166534;">.streamlit/secrets.toml</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1rem">Teknologi Stack</div>', unsafe_allow_html=True)
        tech_stack = {
            "Bahasa": "Python 3.11",
            "Dashboard": "Streamlit",
            "Database": "Supabase PostgreSQL",
            "Visualisasi": "Plotly Express",
            "ORM": "SQLAlchemy",
            "Pemodelan": "Star Schema OLAP",
        }
        for k, v in tech_stack.items():
            st.markdown(
                f'<div style="display:flex; justify-content:space-between; padding:0.35rem 0; '
                f'border-bottom:1px solid #E0E7FF; font-size:0.84rem;">'
                f'<span style="color:#6B7280; font-weight:600;">{k}</span>'
                f'<span style="color:#1E3A8A; font-weight:700; font-family:\'JetBrains Mono\', monospace; font-size:0.8rem;">{v}</span></div>',
                unsafe_allow_html=True
            )

# ============================================================
# PAGE 2: DASHBOARD OLAP BUSINESS INSIGHT (6 GRAFIK)
# ============================================================
elif menu_selection == "📊 OLAP Business Insight":

    st.markdown("""
        <div class="page-header">
            <div class="main-title">📊 Executive Business Intelligence Dashboard</div>
            <div class="sub-title">Analisis Keputusan Strategis Multi-Dimensional Berbasis OLAP View · v_analitik_penjualan</div>
        </div>
    """, unsafe_allow_html=True)

    # --- Ambil opsi filter dari tabel dimensi ---
    @st.cache_data
    def pull_filter_dropdowns():
        with engine.connect() as conn:
            prov = pd.read_sql(
                "SELECT DISTINCT provinsiapotek FROM v_analitik_penjualan WHERE provinsiapotek IS NOT NULL ORDER BY provinsiapotek",
                conn
            )["provinsiapotek"].tolist()
            kat = pd.read_sql(
                "SELECT DISTINCT kategoriproduk FROM v_analitik_penjualan WHERE kategoriproduk IS NOT NULL ORDER BY kategoriproduk",
                conn
            )["kategoriproduk"].tolist()
            thn = pd.read_sql(
                "SELECT DISTINCT tahun FROM v_analitik_penjualan WHERE tahun IS NOT NULL ORDER BY tahun DESC",
                conn
            )["tahun"].tolist()
        return prov, kat, thn

    try:
        list_prov, list_kat, list_thn = pull_filter_dropdowns()

        # --- Filter Sidebar ---
        with st.sidebar:
            st.markdown("### 🎯 Filter Dimensi")
            user_prov = st.multiselect("Provinsi Apotek", options=list_prov, default=list_prov)
            user_kat  = st.multiselect("Kategori Produk", options=list_kat,  default=list_kat)
            user_thn  = st.multiselect("Tahun Transaksi", options=list_thn,  default=list_thn)

        f_prov = user_prov if user_prov else list_prov
        f_kat  = user_kat  if user_kat  else list_kat
        f_thn  = [int(y) for y in user_thn] if user_thn else [int(y) for y in list_thn]

        # --- Fetch data dari OLAP view ---
        @st.cache_data
        def fetch_filtered_view(p, k, t):
            sql_query = """
                SELECT * FROM v_analitik_penjualan
                WHERE provinsiapotek IN %(p)s
                  AND kategoriproduk  IN %(k)s
                  AND tahun           IN %(t)s
            """
            return pd.read_sql(sql_query, engine, params={"p": tuple(p), "k": tuple(k), "t": tuple(t)})

        df = fetch_filtered_view(tuple(f_prov), tuple(f_kat), tuple(f_thn))

        if df.empty:
            st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi filter yang dipilih.")
        else:
            # ---- KPI CARDS ----
            k1, k2, k3, k4 = st.columns(4)
            kpis = [
                ("💰", f"Rp {df['totalpenjualan'].sum():,.0f}", "Total Revenue", "Akumulasi Omset"),
                ("📈", f"Rp {df['keuntungan'].sum():,.0f}",    "Total Profit",   "Margin Keuntungan"),
                ("📦", f"{df['jumlahterjual'].sum():,} pcs",   "Volume Terjual", "Unit Obat"),
                ("🧾", f"{df['fakturid'].nunique():,} Nota",   "Total Transaksi", "Nota Faktur"),
            ]
            for col, (icon, val, lbl, badge) in zip([k1, k2, k3, k4], kpis):
                with col:
                    st.markdown(
                        f'<div class="kpi-card">'
                        f'<div class="kpi-icon">{icon}</div>'
                        f'<div class="kpi-val">{val}</div>'
                        f'<div class="kpi-lbl">{lbl}</div>'
                        f'<div class="kpi-badge">{badge}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # Plotly theme shared
            CHART_TEMPLATE = "plotly_white"

            # ---- ROW 1 ----
            r1c1, r1c2 = st.columns(2, gap="medium")

            with r1c1:
                # INSIGHT 1: Pola beli lansia BPJS per kategori produk
                sub1 = df[
                    (df["kelompokusia"] == "56+") &
                    (df["tipepelanggan"] == "BPJS/Asuransi")
                ]
                if not sub1.empty:
                    agg1 = sub1.groupby('kategoriproduk')['jumlahterjual'].sum().reset_index().sort_values('jumlahterjual')
                    fig1 = px.bar(
                        agg1, x='jumlahterjual', y='kategoriproduk', orientation='h',
                        title="🛒 Pola Beli Kelompok Lansia Pengguna BPJS",
                        labels={'jumlahterjual': 'Item Terjual (pcs)', 'kategoriproduk': 'Kategori Produk'},
                        color='jumlahterjual', color_continuous_scale='Blues',
                        template=CHART_TEMPLATE
                    )
                    fig1.update_layout(coloraxis_showscale=False, title_font_size=13)
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("📭 Insight 1: Data kombinasi Lansia + BPJS kosong pada filter saat ini.")

            with r1c2:
                # INSIGHT 2: Rasio margin keuntungan per tipe cabang (Jawa Barat)
                sub2 = df[df['provinsiapotek'] == 'Jawa Barat']
                if not sub2.empty:
                    agg2 = sub2.groupby('tipecabang').agg(
                        totalpenjualan=('totalpenjualan', 'sum'),
                        keuntungan=('keuntungan', 'sum')
                    ).reset_index()
                    agg2['margin_pct'] = (agg2['keuntungan'] / agg2['totalpenjualan'].replace(0, pd.NA) * 100).fillna(0)
                    fig2 = px.bar(
                        agg2, x='tipecabang', y='margin_pct',
                        text=agg2['margin_pct'].round(1).astype(str) + '%',
                        title="🏢 Margin Keuntungan per Tipe Cabang (Jawa Barat)",
                        labels={'tipecabang': 'Tipe Cabang', 'margin_pct': 'Margin Keuntungan (%)'},
                        color='margin_pct', color_continuous_scale='Greens',
                        template=CHART_TEMPLATE
                    )
                    fig2.update_traces(textposition='outside')
                    fig2.update_layout(coloraxis_showscale=False, title_font_size=13)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("📭 Insight 2: Wilayah Jawa Barat tidak dipilih pada filter provinsi.")

            # ---- ROW 2 ----
            r2c1, r2c2 = st.columns(2, gap="medium")

            with r2c1:
                # INSIGHT 3: Top 10 supplier margin Q3
                sub3 = df[df['kuartal'] == 'Q3']
                if not sub3.empty:
                    agg3 = (
                        sub3.groupby('namasupplier')['keuntungan'].sum()
                        .reset_index()
                        .sort_values('keuntungan', ascending=False)
                        .head(10)
                    )
                    fig3 = px.bar(
                        agg3.sort_values('keuntungan'), x='keuntungan', y='namasupplier', orientation='h',
                        title="🤝 Top 10 Supplier Penyumbang Profit Tertinggi (Q3)",
                        labels={'keuntungan': 'Kontribusi Profit (Rp)', 'namasupplier': 'Nama Supplier'},
                        color='keuntungan', color_continuous_scale='Oranges',
                        template=CHART_TEMPLATE
                    )
                    fig3.update_layout(coloraxis_showscale=False, title_font_size=13)
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("📭 Insight 3: Tidak ada data transaksi pada Kuartal 3 (Q3) di filter ini.")

            with r2c2:
                # INSIGHT 4: Tren revenue bulanan multi-tahun
                agg4 = (
                    df.groupby(['tahun', 'nomorbulan', 'bulan'])['totalpenjualan']
                    .sum().reset_index()
                    .sort_values(['tahun', 'nomorbulan'])
                )
                agg4['periode'] = agg4['bulan'].str.strip() + " " + agg4['tahun'].astype(str)
                fig4 = px.line(
                    agg4, x='periode', y='totalpenjualan', markers=True,
                    title="📈 Tren Revenue Bulanan Multi-Tahun",
                    labels={'periode': 'Periode', 'totalpenjualan': 'Total Penjualan (Rp)'},
                    template=CHART_TEMPLATE
                )
                fig4.update_traces(line_color='#3B82F6', marker_color='#1E3A8A', line_width=2.5)
                fig4.update_layout(title_font_size=13)
                st.plotly_chart(fig4, use_container_width=True)

            # ---- ROW 3 ----
            r3c1, r3c2 = st.columns(2, gap="medium")

            with r3c1:
                # INSIGHT 5: Top 10 produk revenue terbesar
                agg5 = (
                    df.groupby('namaproduk')['totalpenjualan'].sum()
                    .reset_index()
                    .sort_values('totalpenjualan', ascending=False)
                    .head(10)
                )
                fig5 = px.bar(
                    agg5.sort_values('totalpenjualan'), x='totalpenjualan', y='namaproduk', orientation='h',
                    title="🏆 Top 10 Produk Penyumbang Revenue Terbesar",
                    labels={'totalpenjualan': 'Total Penjualan (Rp)', 'namaproduk': 'Nama Produk'},
                    color='totalpenjualan', color_continuous_scale='Purples',
                    template=CHART_TEMPLATE
                )
                fig5.update_layout(coloraxis_showscale=False, title_font_size=13)
                st.plotly_chart(fig5, use_container_width=True)

            with r3c2:
                # INSIGHT 6: Distribusi revenue per kota (top 10)
                agg6 = (
                    df.groupby('kotaapotek')['totalpenjualan'].sum()
                    .reset_index()
                    .sort_values('totalpenjualan', ascending=False)
                    .head(10)
                )
                fig6 = px.pie(
                    agg6, values='totalpenjualan', names='kotaapotek', hole=0.42,
                    title="📍 Pangsa Revenue 10 Kota Apotek Teratas",
                    template=CHART_TEMPLATE
                )
                fig6.update_traces(textposition='inside', textinfo='percent+label')
                fig6.update_layout(showlegend=False, title_font_size=13)
                st.plotly_chart(fig6, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Koneksi ke database OLAP Supabase gagal. Periksa konfigurasi `DB_URL` di `secrets.toml`. Detail: {e}")

# ============================================================
# PAGE 3: DOKUMENTASI PIPELINE ETL
# ============================================================
elif menu_selection == "⚙️ Aliran Pipeline ETL":

    st.markdown("""
        <div class="page-header">
            <div class="main-title">⚙️ Ekosistem Rekayasa Data & Pipeline ELT</div>
            <div class="sub-title">Arsitektur Aliran Data Transaksional Menuju Lapisan Konsumsi BI Platform</div>
        </div>
    """, unsafe_allow_html=True)

    # --- Ringkasan Pendekatan ELT ---
    st.markdown('<div class="section-label">Pendekatan ELT vs ETL</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    Proyek ini mengadopsi pendekatan <strong>ELT (Extract → Load → Transform)</strong> kelas industri, 
    berbeda dari ETL konvensional. Transformasi data dilakukan <em>setelah</em> data dimuat ke database cloud, 
    memanfaatkan computing power Supabase PostgreSQL secara penuh sehingga beban pemrosesan tidak jatuh ke memori lokal.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Pipeline Steps ---
    st.markdown('<div class="section-label">Alur Kerja Pipeline (5 Tahap)</div>', unsafe_allow_html=True)

    steps = [
        (
            "01 · EXTRACT",
            "Ekstraksi & Standardisasi Berkas Sumber",
            "Script <code>src/extract.py</code> membaca 6 berkas <code>.csv</code> mentah dari direktori <code>data/</code>. "
            "Nama kolom langsung di-standardisasi (lowercase, strip spasi) dan kolom kunci di-rename agar konsisten "
            "dengan skema DW (contoh: <code>id_faktur → fakturid</code>, <code>kode_barang → produkid</code>). "
            "Data tidak dimanipulasi secara substantif di tahap ini—hanya pembersihan struktural minimal."
        ),
        (
            "02 · LOAD",
            "Staging ke Supabase PostgreSQL (Tanpa Transformasi)",
            "Data mentah yang telah ter-standardisasi langsung diunggah ke tabel staging Supabase "
            "(<code>stg_produk</code>, <code>stg_apotek</code>, <code>stg_pelanggan</code>, "
            "<code>stg_karyawan</code>, <code>stg_supplier</code>, <code>stg_penjualan</code>) "
            "menggunakan <code>DataFrame.to_sql()</code> dengan mode <code>replace</code>. "
            "Tidak ada transformasi record—semua komputasi diserahkan ke engine database."
        ),
        (
            "03 · TRANSFORM",
            "Transformasi Database-Centric via SQL (<code>sql/transform.sql</code>)",
            "Seluruh operasi berat dieksekusi murni di dalam Supabase: konversi tipe data tanggal, "
            "normalisasi Primary/Foreign Key (UPPER + strip karakter), deduplikasi transaksi, "
            "imputasi nilai kosong dengan <code>COALESCE</code> & median, hingga kalkulasi finansial "
            "(<em>Revenue</em> = qty × harga − diskon, <em>Profit</em> = Revenue − modal). "
            "Script dieksekusi oleh <code>src/transform.py</code> yang membaca dan menjalankan file SQL secara transaksional."
        ),
        (
            "04 · MODEL",
            "Pemodelan Dimensional Star Schema",
            "Data bersih dimuat ke struktur <strong>Star Schema</strong>: "
            "<code>fact_penjualan</code> sebagai tabel fakta utama yang terhubung ke "
            "<code>dim_produk</code>, <code>dim_apotek</code>, <code>dim_pelanggan</code>, "
            "<code>dim_karyawan</code>, <code>dim_supplier</code>, dan <code>dim_waktu</code> "
            "melalui Foreign Key. Setiap dimensi memiliki nilai fallback <code>UNKNOWN</code> "
            "untuk menjaga integritas referensial tanpa menjatuhkan baris fakta."
        ),
        (
            "05 · CONSUME",
            "Lapisan Konsumsi: Analytical View → Streamlit Dashboard",
            "Dashboard tidak pernah memanggil tabel mentah atau melakukan JOIN langsung. "
            "Semua visualisasi dikonsumsi dari <code>v_analitik_penjualan</code>—sebuah SQL View matang "
            "yang menggabungkan seluruh dimensi ke fakta penjualan. Filter interaktif (provinsi, kategori, tahun) "
            "diteruskan sebagai parameter SQL, menjaga query tetap ringan dan responsif."
        ),
    ]

    for badge, title, desc in steps:
        st.markdown(
            f'<div class="pipeline-step">'
            f'<span class="step-badge">{badge}</span>'
            f'<div class="step-content"><h4>{title}</h4><p>{desc}</p></div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # --- Struktur File ---
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown('<div class="section-label">Struktur Berkas Proyek</div>', unsafe_allow_html=True)
        st.code("""
kimia-farma-dw/
├── .streamlit/
│   └── secrets.toml       ← DB_URL (private)
├── data/
│   ├── produk.csv
│   ├── apotek.csv
│   ├── pelanggan.csv
│   ├── karyawan.csv
│   ├── supplier.csv
│   └── penjualan.csv
├── sql/
│   ├── schema.sql         ← DDL: CREATE TABLE
│   ├── transform.sql      ← ELT: staging → DW
│   └── views.sql          ← OLAP View
├── src/
│   ├── extract.py         ← Extract & Load
│   └── transform.py       ← Eksekusi SQL
└── app.py                 ← Streamlit Dashboard
        """, language="")

    with col_b:
        st.markdown('<div class="section-label">Pemetaan Kolom Kunci (Konsistensi DW)</div>', unsafe_allow_html=True)
        col_map = {
            "CSV Sumber": ["id_faktur", "tgl_trx", "kode_barang", "id_apotek", "kasir_id", "harga_satuan"],
            "Staging (stg_)": ["fakturid", "tanggal", "produkid", "apotekid", "karyawanid", "hargasatuan"],
            "Tabel DW / View": ["fakturid", "tanggal", "produkid", "apotekid", "karyawanid", "hargasatuan"],
        }
        st.dataframe(pd.DataFrame(col_map), use_container_width=True, hide_index=True)

        st.markdown('<div class="section-label" style="margin-top:1rem">Metrik Kalkulasi Finansial</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <strong>totalpenjualan</strong> = (jumlahterjual × hargasatuan) − diskon<br>
        <strong>keuntungan</strong> = totalpenjualan − (jumlahterjual × hargamodal)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box" style="margin-top:1rem">
    🚀 <strong>Kesimpulan:</strong> Seluruh komputasi berat dieksekusi di sisi database cloud Supabase. 
    Dashboard Streamlit hanya mengonsumsi view agregat siap pakai, menjadikan performa aplikasi 
    responsif dan layak dideploy ke server publik tanpa risiko bottleneck memori.
    </div>
    """, unsafe_allow_html=True)