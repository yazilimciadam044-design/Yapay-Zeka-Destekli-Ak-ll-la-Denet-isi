import os
import sys
from fpdf import FPDF
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile

def _get_font_path(style=""):
    """Windows ve Linux'ta uygun Unicode font dosyasını bul."""
    # Windows fontları
    win_fonts = {
        "": r"C:\Windows\Fonts\arial.ttf",
        "B": r"C:\Windows\Fonts\arialbd.ttf",
        "I": r"C:\Windows\Fonts\ariali.ttf",
    }
    if sys.platform == "win32" and os.path.exists(win_fonts.get(style, "")):
        return win_fonts[style]
    
    # Linux (Streamlit Cloud) - DejaVuSans kullan
    linux_fonts = {
        "": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "B": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "I": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    }
    if os.path.exists(linux_fonts.get(style, "")):
        return linux_fonts[style]
    
    return None

class ReportPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Unicode destekli fontu tanimla (bir kere)
        font_regular = _get_font_path("")
        font_bold = _get_font_path("B")
        
        self._has_unicode_font = False
        if font_regular:
            self.add_font('UnicodeFont', '', font_regular)
            self._has_unicode_font = True
        if font_bold:
            self.add_font('UnicodeFont', 'B', font_bold)

    def header(self):
        if self._has_unicode_font:
            self.set_font('UnicodeFont', 'B', 15)
        else:
            self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'Pharma-Guard AI - Akilli Ilac Denetcisi Raporu', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if self._has_unicode_font:
            self.set_font('UnicodeFont', '', 8)
        else:
            self.set_font('Helvetica', '', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}/{{nb}} - DIKKAT: Bilgiler dogrulanamadi, profesyonel yardim alin', 0, 0, 'C')

def generate_pdf_report(report_content: str, output_path: str = None) -> str:
    """
    Rapor içeriğini PDF formatına çevirip kaydeder.
    Eğer output_path verilmezse geçici bir dosya yolu döndürür.
    """
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    if pdf._has_unicode_font:
        pdf.set_font('UnicodeFont', '', 12)
        pdf.multi_cell(0, 10, txt=report_content)
    else:
        # Fallback: unidecode ile Türkçe karakterleri ASCII'ye çevir
        import unidecode
        pdf.set_font('Helvetica', '', 12)
        pdf.multi_cell(0, 10, txt=unidecode.unidecode(report_content))
    
    if output_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        output_path = temp_file.name
        temp_file.close()
        
    pdf.output(output_path)
    return output_path

def init_rag_database(corpus_path: str = "data/corpus", persist_directory: str = "data/chroma_db"):
    """
    Belirtilen dizindeki PDF'leri okur, vektörleştirir ve ChromaDB'ye kaydeder.
    """
    if not os.path.exists(corpus_path):
        os.makedirs(corpus_path)
        print(f"Uyarı: '{corpus_path}' dizini yoktu, oluşturuldu. Lütfen içine PDF ekleyin.")
        return None
        
    pdf_files = [f for f in os.listdir(corpus_path) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"Uyarı: '{corpus_path}' dizininde hiç PDF dosyası bulunamadı.")
        return None
        
    print(f"RAG Veritabanı başlatılıyor... {len(pdf_files)} PDF bulundu.")
    loader = PyPDFDirectoryLoader(corpus_path)
    documents = loader.load_and_split()
    
    # HuggingFace tabanlı ücretsiz, hafif bir embedding modeli kullanıyoruz.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db = Chroma.from_documents(
        documents, 
        embeddings, 
        persist_directory=persist_directory
    )
    return db

def get_rag_retriever(persist_directory: str = "data/chroma_db"):
    """
    Kaydedilmiş olan ChromaDB veritabanını yükler ve retriever döner.
    """
    if not os.path.exists(persist_directory):
        return None
        
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return db.as_retriever(search_kwargs={"k": 5})

