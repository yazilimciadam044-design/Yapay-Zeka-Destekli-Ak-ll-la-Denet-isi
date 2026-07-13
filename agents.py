import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from groq import Groq
from utils import get_rag_retriever

load_dotenv()

# API Keys and configs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Clients
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY and GROQ_API_KEY != "BURAYA_API_ANAHTARINIZI_YAZIN" else None

MASTER_PROMPT = """
### ROLE: PHARMA-GUARD MASTER ORCHESTRATOR (PG-MO) ###

Sen, Llama-4 Scout (Groq) tabanli, coklu ajan (Multi-Agent) ekosistemini yoneten bas mimarsin. Gorevin; gorsel veya metinsel girisi alinan bir ilaci, sifir hata toleransi ile analiz etmektir.

AŞAĞIDAKİ 5 ALT AJANI AYNI ANDA KOORDİNE ET:

1. [Vision-Scanner]: LLaVA mimarisini kullanarak görseli tara. İlaç ismi (Ticari Ad), Etken Madde (Kimyasal Ad), Dozaj (mg/ml), Form (Tablet/Şurup) ve varsa Barkod bilgilerini JSON formatında ana belleğe aktar.
2. [RAG-Specialist]: "data/corpus/" dizinindeki PDF prospektüsleri semantik olarak tara. İnternetteki genel yorumları değil, sadece TİTCK ve FDA onaylı prospektüs verilerini kaynak al.
3. [Safety-Auditor]: İlacın "Yan Etkiler", "Diğer İlaçlarla Etkileşim" ve "Kimler Kullanamaz" kısımlarını derinlemesine analiz et. Kritik bir risk (örn: hamilelikte kullanım, yüksek tansiyon uyarısı, ilaç etkileşimleri) tespit edersen "KIRMIZI ALARM" etiketi oluştur.
4. [Corporate-Analyst]: İlacı üreten firmanın geçmişini, üretim sertifikalarını (GMP, FDA onayı vb.), menşe ülkesini ve kurumsal tıbbi itibarını detaylı bir şekilde raporla.
5. [Report-Synthesizer]: Tum ajanlardan gelen veriyi birlestir. Llama-4 Scout (Groq) gucunde detayli, eksiksiz ve derinlikli bir analiz raporu hazirla.

### OPERASYONEL PROTOKOLLER VE KISITLAMALAR:
- SIFIR VERİ KAYBI (ZERO DATA LOSS): Bulduğun hiçbir detayı özetleme, kırpma veya eksiltme. Disiplinli, akademik ve son derece detaylı bir rapor oluştur.
- GÜVEN PUANI (Confidence Score): Her bilgi parçası için 1-10 arası bir puan ver. Eğer ortalama güven 8'in altındaysa raporun başına "DİKKAT: Bilgiler %100 doğrulanamadı, profesyonel yardım alın" uyarısı ekle.
- FORMAT: Hiyerarşik başlıklar (Markdown), net madde işaretleri (bullet points) ve profesyonel/akademik bir Tıp dili kullan. Uzun, tatmin edici ve tıbbi açıdan eksiksiz olmalı.
- HALÜSİNASYON ENGELİ: Eğer ilacın etken maddesi ile prospektüs bilgisi eşleşmiyorsa, 'Fact-Checker' devreye girsin ve süreci durdurup hata mesajı versin.
- DİL VE ÜSLUP: Rapor tamamen Türkçe, tıbbi terimleri parantez içinde açıklayan, güven veren ve profesyonel bir tonda olmalıdır.
- İNDİRME FORMATI: Çıktıyı, "İndirilebilir Rapor" için uygun bir Markdown hiyerarşisinde sun.

### ÇIKTI HİYERARŞİSİ (ZORUNLU):
1. İlaç Kimlik Özeti
2. Kullanım Amacı (Endikasyonlar)
3. Kritik Uyarılar ve Yan Etkiler
4. Etken Madde ve Üretici Detayları
5. RAG / Kaynakça (Hangi belgeden, hangi sayfa/linkten alındı?)
"""

class Agents:
    @staticmethod
    def vision_scanner(image_path: str = None, text_input: str = None) -> dict:
        """
        LLaVA (veya fallback olarak Gemini Vision) kullanarak ilaç kimliğini çıkarır.
        """
        # Burada LLaVA API (Ollama veya Replicate) çağrısı simüle ediliyor.
        # Eğer gerçek LLaVA API eklenecekse buraya requests modülü ile Ollama sunucusuna istek atılabilir.
        
        # Basit bir mock/fallback mantığı (API'ler tam set edilmemişse çalışması için):
        if text_input:
            query = text_input
        else:
            query = "Görsel analizi yapıldı varsayılıyor."
            
        print("[Vision-Scanner] İlaç bilgileri ayrıştırılıyor...")
        
        # Groq Llama-3 ile JSON çıkartalım (Eğer görsel verilemiyorsa text input'u JSON'a çevirelim)
        if groq_client:
            prompt = f"""Şu metinden veya görselden (temsili) ilaç bilgilerini çıkar. SADECE JSON dön:
Metin: {query}
Format: {{"ilac_ismi": "", "etken_madde": "", "dozaj": "", "form": ""}}"""
            try:
                response = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    temperature=0.1
                )
                try:
                    content = response.choices[0].message.content.strip()
                    if content.startswith("```json"):
                        content = content.replace("```json", "").replace("```", "").strip()
                    elif content.startswith("```"):
                        content = content.replace("```", "").strip()
                    return json.loads(content)
                except Exception as parse_e:
                    print("JSON Parse Hatası:", parse_e)
            except Exception as e:
                print("Groq API Hatası:", e)
                
        # Fallback Mock Data
        return {
            "ilac_ismi": text_input or "Bilinmeyen İlaç",
            "etken_madde": "Bilinmiyor",
            "dozaj": "Bilinmiyor",
            "form": "Bilinmiyor"
        }

    @staticmethod
    def rag_specialist(ilac_ismi: str, etken_madde: str) -> str:
        """
        RAG veritabanından ilaç prospektüs bilgilerini tarar.
        """
        retriever = get_rag_retriever()
        if not retriever:
            return "RAG Sistemi aktif değil (PDF veritabanı bulunamadı)."
            
        print(f"[RAG-Specialist] '{ilac_ismi}' için RAG taraması yapılıyor...")
        query = f"{ilac_ismi} {etken_madde} prospektüs endikasyon yan etkiler dozaj"
        docs = retriever.invoke(query)
        
        context = "\\n\\n".join([doc.page_content for doc in docs])
        return context if context else "Bu ilaçla ilgili yerel veritabanında (PDF) bilgi bulunamadı."

    @staticmethod
    def safety_auditor(rag_context: str, ilac_ismi: str) -> dict:
        """
        RAG verisindeki yan etkileri ve kontrendikasyonları denetler.
        """
        print(f"[Safety-Auditor] '{ilac_ismi}' için güvenlik denetimi yapılıyor...")
        if groq_client:
            prompt = f"""Aşağıdaki prospektüs metnine göre '{ilac_ismi}' için 'Yan Etkiler' ve 'Kimler Kullanamaz' bilgilerini çok katı ve eksiksiz bir disiplinle analiz et. Metinde geçen TÜM yan etkileri ve TÜM kontrendikasyonları hiçbir eksiltme yapmadan listele. Eğer ciddi bir risk (hamilelik, kalp krizi, intihar, mide kanaması vs) varsa kirmizi_alarm: true yap. SADECE JSON formatında dön: {{"yan_etkiler": ["etki 1", "etki 2", ...], "kontrendikasyonlar": ["durum 1", "durum 2", ...], "kirmizi_alarm": true/false}}

Metin:
{rag_context}"""
            try:
                response = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    temperature=0
                )
                try:
                    return json.loads(response.choices[0].message.content)
                except:
                    pass
            except:
                pass
        
        return {"yan_etkiler": ["Veri analiz edilemedi"], "kontrendikasyonlar": [], "kirmizi_alarm": False}

    @staticmethod
    def corporate_analyst(rag_context: str, ilac_ismi: str) -> str:
        """
        İlaç üreticisi hakkında bilgi toplar.
        """
        print(f"[Corporate-Analyst] Üretici firma araştırması yapılıyor...")
        if groq_client:
            prompt = f"""Lütfen '{ilac_ismi}' adlı ilacın üretici firması, firmanın menşei, tıbbi üretim geçmişi ve genel kurumsal güvenilirliği hakkında son derece detaylı, akademik ve eksiksiz bir kurumsal araştırma raporu sun (En az 2 paragraf).
Şu kurala KESİNLİKLE UY: Asla ve asla "[Firma İsmi]", "[Ülke]", "[Kuruluş Yılı]" gibi KÖŞELİ PARANTEZLİ ŞABLON (TEMPLATE) kullanma.
Aşağıdaki tıbbi prospektüs verisini (RAG Context) referans al ve içerisindeki "Üretici Firma" bilgisine dayanarak gerçek ve kesin bir analiz yap. Eğer veride geçmiyorsa, bilinen gerçek tıbbi verilerine dayanarak kesin isimler kullan.

Prospektüs Verisi:
{rag_context}
"""
            try:
                response = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="meta-llama/llama-4-scout-17b-16e-instruct"
                )
                return response.choices[0].message.content
            except:
                pass
        return "Firma bilgisi sorgulanamadı."

    @staticmethod
    def report_synthesizer(vision_data: dict, rag_data: str, safety_data: dict, corporate_data: str) -> str:
        """
        Groq (Master Orchestrator) kullanarak final markdown raporunu hazırlar.
        API anahtarı yoksa yapılandırılmış bir fallback rapor üretir.
        """
        print("[Report-Synthesizer] Sonuçlar sentezleniyor...")
        
        if groq_client:
            # --- GROQ API İLE RAPOR ÜRETİMİ ---
            system_instruction = MASTER_PROMPT
            
            prompt = f"""
            Aşağıdaki alt ajanlardan gelen verileri birleştirerek MASTER PROMPT kurallarına harfiyen uygun bir MARKDOWN rapor oluştur:
            
            1. [Vision-Scanner] Verisi (İlaç Kimliği):
            {json.dumps(vision_data, ensure_ascii=False, indent=2)}
            
            2. [RAG-Specialist] Verisi (Prospektüs):
            {rag_data}
            
            3. [Safety-Auditor] Verisi (Güvenlik Riskleri):
            {json.dumps(safety_data, ensure_ascii=False, indent=2)}
            
            4. [Corporate-Analyst] Verisi (Firma):
            {corporate_data}
            
            KURAL: Eğer etken madde RAG verisiyle uyumsuzsa Halüsinasyon Engelini (Fact-Checker) devreye sok.
            """
            
            try:
                response = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Groq API hatası, fallback rapora geçiliyor: {e}")

        # --- FALLBACK: API OLMADAN YAPILANDIRILMIŞ RAPOR ---
        ilac_ismi = vision_data.get("ilac_ismi", "Bilinmiyor")
        etken_madde = vision_data.get("etken_madde", "Bilinmiyor")
        dozaj = vision_data.get("dozaj", "Bilinmiyor")
        form = vision_data.get("form", "Bilinmiyor")
        
        yan_etkiler = safety_data.get("yan_etkiler", ["Veri bulunamadı"])
        kontrendikasyonlar = safety_data.get("kontrendikasyonlar", [])
        kirmizi_alarm = safety_data.get("kirmizi_alarm", False)
        
        alarm_banner = ""
        if kirmizi_alarm:
            alarm_banner = "\n> **[!] KIRMIZI ALARM**: Bu ilacta ciddi risk faktorleri tespit edilmistir. Kullanmadan once mutlaka bir saglik uzmanina danisiniz!\n"
        
        yan_etkiler_str = "\n".join([f"- {y}" for y in yan_etkiler]) if yan_etkiler else "- Bilgi bulunamadı"
        kontrendikasyonlar_str = "\n".join([f"- {k}" for k in kontrendikasyonlar]) if kontrendikasyonlar else "- Bilgi bulunamadı"
        
        rag_section = rag_data if rag_data and "bulunamadı" not in rag_data.lower() else "Yerel veritabanında bu ilaçla ilgili prospektüs bilgisi bulunamadı."
        
        report = f"""# PHARMA-GUARD AI - Ilac Denetim Raporu

> **DIKKAT**: Bu rapor Groq API baglantisi olmadan olusturulmustur. AI destekli derinlemesine analiz icin lutfen `.env` dosyasina gecerli bir Groq API anahtari ekleyiniz.
{alarm_banner}
---

## 1. İlaç Kimlik Özeti

| Bilgi | Değer |
|-------|-------|
| **Ticari Ad** | {ilac_ismi} |
| **Etken Madde** | {etken_madde} |
| **Dozaj** | {dozaj} |
| **Form** | {form} |
| **Güven Puanı** | 5/10 (API bağlantısız mod) |

---

## 2. Kullanım Amacı (Endikasyonlar)

Prospektüs veritabanından elde edilen bilgiler:

{rag_section}

---

## 3. Kritik Uyarılar ve Yan Etkiler

### Yan Etkiler
{yan_etkiler_str}

### Kontrendikasyonlar (Kimler Kullanamaz)
{kontrendikasyonlar_str}

---

## 4. Üretici Firma Bilgileri

{corporate_data}

---

## 5. Kaynakça

- Veri Kaynağı: Yerel RAG veritabanı (`data/corpus/`)
- Analiz Motoru: Pharma-Guard AI (Fallback Modu)
- Not: Tam AI destekli analiz için Groq API anahtarı gereklidir.

---
*Bu rapor Pharma-Guard AI tarafından otomatik olarak oluşturulmuştur. Tıbbi kararlarınızda mutlaka bir sağlık profesyoneline danışınız.*
"""
        return report

def run_orchestrator(input_text: str):
    # 1. Vision Scanner
    vision_data = Agents.vision_scanner(text_input=input_text)
    
    # 2. RAG Specialist
    rag_data = Agents.rag_specialist(vision_data.get("ilac_ismi", ""), vision_data.get("etken_madde", ""))
    
    # 3. Safety Auditor
    safety_data = Agents.safety_auditor(rag_data, vision_data.get("ilac_ismi", ""))
    
    # 4. Corporate Analyst
    corporate_data = Agents.corporate_analyst(rag_data, vision_data.get("ilac_ismi", ""))
    
    # 5. Report Synthesizer & Master Orchestrator
    final_report = Agents.report_synthesizer(vision_data, rag_data, safety_data, corporate_data)
    
    return final_report
