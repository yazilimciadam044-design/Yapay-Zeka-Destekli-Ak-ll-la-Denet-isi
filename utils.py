import os
from fpdf import FPDF
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile

class ReportPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Arial fontunu tanimla (bir kere)
        self.add_font('ArialCustom', '', r"C:\Windows\Fonts\arial.ttf")
        self.add_font('ArialCustom', 'B', r"C:\Windows\Fonts\arialbd.ttf")
        self.add_font('ArialCustom', 'I', r"C:\Windows\Fonts\ariali.ttf")

    def header(self):
        self.set_font('ArialCustom', 'B', 15)
        self.cell(0, 10, 'Pharma-Guard AI - Akıllı İlaç Denetçisi Raporu', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('ArialCustom', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}/{{nb}} - DİKKAT: Bilgiler %100 doğrulanamadı, profesyonel yardım alın', 0, 0, 'C')

def generate_pdf_report(report_content: str, output_path: str = None) -> str:
    """
    Rapor içeriğini PDF formatına çevirip kaydeder.
    Eğer output_path verilmezse geçici bir dosya yolu döndürür.
    """
    import unidecode
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('ArialCustom', '', 12)
    
    # Doğrudan Türkçe karakterli gerçek raporu yazdır
    pdf.multi_cell(0, 10, txt=report_content)
    
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
    return db.as_retriever(search_kwargs={"k": 3})

