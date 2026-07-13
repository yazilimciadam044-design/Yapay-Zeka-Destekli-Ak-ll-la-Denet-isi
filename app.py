import os
import sys

# Streamlit Cloud SQLite3 (ChromaDB) Fix
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
from agents import run_orchestrator
from utils import generate_pdf_report, init_rag_database

# Streamlit Cloud'da ilk başlatmada otomatik PDF ve RAG veritabanı oluştur
if not os.path.exists("data/corpus") or len([f for f in os.listdir("data/corpus") if f.endswith('.pdf')]) == 0:
    from create_dummy_pdf import main as create_pdfs
    create_pdfs()

if not os.path.exists("data/chroma_db"):
    init_rag_database()

# Sayfa Ayarları
st.set_page_config(
    page_title="Pharma-Guard AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
    <style>
    /* Genel yazi boyutu ve rengi */
    .main {
        background-color: #0e1117;
        color: #e8eaed;
        font-size: 18px;
    }
    /* Tum paragraflar ve metinler */
    .main p, .main li, .main span, .main div {
        font-size: 18px !important;
        color: #e8eaed !important;
        line-height: 1.8 !important;
    }
    /* Basliklar */
    h1 {
        color: #4facfe !important;
        font-size: 36px !important;
    }
    h2 {
        color: #00f2fe !important;
        font-size: 28px !important;
    }
    h3 {
        color: #7dd3fc !important;
        font-size: 24px !important;
    }
    /* Sidebar yazilari ve arka plani */
    section[data-testid="stSidebar"] {
        background-color: #1a1c24 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-size: 16px !important;
        color: #ffffff !important;
    }
    /* Butonlar */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: bold;
        font-size: 18px !important;
        transition: all 0.3s ease 0s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
    }
    /* Rapor kutusu */
    .report-box {
        background-color: #1e2030;
        padding: 30px;
        border-radius: 12px;
        border-left: 5px solid #4facfe;
        margin-top: 20px;
        font-size: 18px !important;
        color: #f0f0f0 !important;
        line-height: 1.9 !important;
    }
    .report-box h1, .report-box h2, .report-box h3 {
        color: #4facfe !important;
    }
    .report-box p, .report-box li, .report-box span {
        color: #f0f0f0 !important;
        font-size: 18px !important;
    }
    /* Input alani */
    .stTextInput input {
        font-size: 18px !important;
        padding: 12px !important;
    }
    .stTextInput label {
        font-size: 18px !important;
        color: #d1d5db !important;
    }
    /* Download butonu */
    .stDownloadButton>button {
        font-size: 18px !important;
        padding: 12px 28px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    st.title("Pharma-Guard AI")
    st.markdown("Yapay Zeka Destekli Akıllı İlaç Denetçisi")
    st.divider()
    st.markdown("### Sistem Durumu")
    
    # RAG Veritabanı Başlatma Modülü
    if st.button("🔄 RAG Veritabanını Güncelle"):
        with st.spinner("PDF'ler taranıyor ve vektörleştiriliyor..."):
            db = init_rag_database()
            if db:
                st.success("Veritabanı güncellendi!")
            else:
                st.warning("data/corpus/ dizininde PDF bulunamadı.")
                
    st.info("💡 Ajanlar hazır. (Groq/Llama-3, LLaVA-Mock, RAG)")

# Ana Ekran
st.title("💊 Akıllı İlaç Denetimi")
st.markdown("Lütfen denetlemek istediğiniz ilacın ismini veya fotoğrafını (metin olarak) giriniz.")

# Input Alanı
col1, col2 = st.columns([2, 1])

with col1:
    input_text = st.text_input("İlaç İsmi / Etken Madde (Örn: Parasetamol 500mg)", placeholder="İlaç adını buraya yazın...")
    # image_file = st.file_uploader("Veya İlaç Fotoğrafı Yükleyin", type=['png', 'jpg', 'jpeg'])

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    start_btn = st.button("🚀 Denetimi Başlat", use_container_width=True)

if start_btn:
    if not input_text:
        st.error("Lütfen bir ilaç ismi giriniz!")
    else:
        st.markdown("---")
        
        # Ajanların çalıştığını gösteren animasyonlu yapı
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("🕵️ **[Vision-Scanner]** Giriş verisi analiz ediliyor...")
        progress_bar.progress(20)
        
        status_text.markdown("📚 **[RAG-Specialist]** Tıbbi prospektüs veritabanı taranıyor...")
        progress_bar.progress(40)
        
        status_text.markdown("⚠️ **[Safety-Auditor]** Kontrendikasyonlar ve riskler denetleniyor...")
        progress_bar.progress(60)
        
        status_text.markdown("🏢 **[Corporate-Analyst]** Üretici profili çıkarılıyor...")
        progress_bar.progress(80)
        
        status_text.markdown("🧠 **[PG-MO]** Master Orkestratör (Groq) raporu sentezliyor...")
        
        try:
            # Backend çağrısı
            final_report = run_orchestrator(input_text)
            progress_bar.progress(100)
            status_text.success("Denetim Tamamlandı!")
            
            # Raporu Ekrana Bas
            st.markdown("### 📋 Analiz Raporu")
            st.markdown(f'<div class="report-box">{final_report}</div>', unsafe_allow_html=True)
            
            # PDF Oluştur ve İndir Butonu
            with st.spinner("PDF Raporu hazırlanıyor..."):
                pdf_path = generate_pdf_report(final_report)
                
                with open(pdf_path, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                    
                st.download_button(
                    label="📄 PDF Olarak İndir",
                    data=PDFbyte,
                    file_name="pharma_guard_rapor.pdf",
                    mime="application/octet-stream"
                )
                
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")

