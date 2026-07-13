# 💊 Pharma-Guard AI

Pharma-Guard AI, ilaç içeriklerini inceleyerek olası yan etkileri, kullanım amaçlarını ve firma bilgilerini denetleyen **Çoklu Ajan (Multi-Agent)** yapısına sahip akıllı bir yapay zeka denetçisidir. Groq altyapısındaki güçlü Llama-4 modelleri ile çalışır. 

## 🚀 Özellikler

- **Görsel/Metinsel Analiz:** İlaç isimlerini veya fotoğraflarındaki metinleri algılar.
- **RAG Teknolojisi:** Sağlık bakanlığı veya FDA onaylı PDF prospektüslerinden semantik arama yaparak bilgileri teyit eder.
- **Güvenlik Denetçisi:** İlacın yan etkilerini analiz eder ve hamilelik, tansiyon, kalp rahatsızlığı gibi riskli durumlar için "KIRMIZI ALARM" üretir.
- **İndirilebilir PDF Raporu:** Elde edilen tüm detaylı veriyi profesyonel bir PDF formatında cihazınıza indirmenizi sağlar.

## 🛠️ Kurulum

1. **Depoyu klonlayın:**
```bash
git clone https://github.com/yazilimciadam044-design/Yapay-Zeka-Destekli-Ak-ll-la-Denet-isi.git
cd Yapay-Zeka-Destekli-Ak-ll-la-Denet-isi
```

2. **Gereksinimleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Çevre Değişkenlerini (API) ayarlayın:**
- `.env.example` dosyasının adını `.env` olarak değiştirin.
- Groq Console üzerinden aldığınız API anahtarını `GROQ_API_KEY` alanına yapıştırın.

## 🏃‍♂️ Çalıştırma

Projenin arayüzünü (Streamlit) ayağa kaldırmak için terminalde şu komutu çalıştırın:

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak açılan sayfada testlerinizi gerçekleştirebilirsiniz.

## 📁 Veritabanına PDF (Prospektüs) Ekleme
Projeyi çalıştırdığınızda otomatik olarak `data/corpus` adında bir klasör oluşur. Bu klasörün içine test etmek istediğiniz ilaçların PDF formatındaki prospektüslerini atarak RAG sisteminin bu ilaçları tanımasını sağlayabilirsiniz.

---
*Uyarı: Bu uygulama eğitim ve asistan amaçlıdır. Nihai tıbbi kararlarınızda daima uzman bir hekime veya eczacıya danışınız.*
