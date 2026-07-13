import os
from utils import generate_pdf_report

def main():
    corpus_path = "data/corpus"
    if not os.path.exists(corpus_path):
        os.makedirs(corpus_path)
    
    text = """
    İlaç İsmi: Parasetamol 500mg
    Endikasyonlar: Hafif ve orta şiddetli ağrılar ile ateşin semptomatik tedavisinde kullanılır.
    Yan Etkiler: Nadir durumlarda alerjik reaksiyonlar, deri döküntüleri, uzun süreli ve yüksek doz kullanımında karaciğer toksisitesi.
    Kimler Kullanamaz (Kontrendikasyonlar): Şiddetli böbrek ve karaciğer yetmezliği olan hastalar.
    Üretici Firma: Örnek İlaç Sanayi A.Ş.
    """
    
    output_path = os.path.join(corpus_path, "parasetamol_prospektus.pdf")
    generate_pdf_report(text, output_path)
    print(f"Örnek PDF oluşturuldu: {output_path}")

if __name__ == "__main__":
    main()
