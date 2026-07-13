import os
import sys

# Windows konsol encoding sorununu coz
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from utils import init_rag_database, generate_pdf_report
from agents import run_orchestrator

def run_tests():
    print("--- TEST 1: RAG DB BASLATMA ---")
    db = init_rag_database()
    if db:
        print("RAG Veritabani basariyla olusturuldu/yuklendi.")
    else:
        print("HATA: RAG Veritabani olusturulamadi!")

    print("\n--- TEST 2: ORCHESTRATOR (AJANLAR) CALISTIRMA ---")
    try:
        report = run_orchestrator("Parasetamol 500mg")
        print("Orkestrator Raporu Basariyla Olusturuldu. Rapor Uzunlugu:", len(report))
        preview = report[:300].encode('ascii', errors='replace').decode('ascii')
        print("Onizleme:\n", preview, "...\n")
    except Exception as e:
        print("HATA: Orkestrator calisirken bir hata olustu:", e)
        return

    print("\n--- TEST 3: PDF RAPOR URETIMI ---")
    try:
        pdf_path = generate_pdf_report(report)
        print(f"PDF Raporu basariyla olusturuldu: {pdf_path}")
        if os.path.exists(pdf_path):
            print("Dosya boyutu:", os.path.getsize(pdf_path), "bayt.")
    except Exception as e:
        print("HATA: PDF olusturulurken hata:", e)
        return
        
    print("\n[BASARILI] TUM TESTLER BASARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    run_tests()
