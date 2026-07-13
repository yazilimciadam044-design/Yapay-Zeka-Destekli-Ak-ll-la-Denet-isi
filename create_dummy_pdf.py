import os
from utils import generate_pdf_report

def main():
    corpus_path = "data/corpus"
    if not os.path.exists(corpus_path):
        os.makedirs(corpus_path)
    
    drugs = [
        {
            "filename": "parasetamol_prospektus.pdf",
            "content": """TIBBİ ÜRÜNÜN ADI: Parasetamol 500mg Tablet
1. KLİNİK ÖZELLİKLER
1.1 Terapötik Endikasyonlar:
Hafif ve orta şiddetli ağrıların (baş ağrısı, migren, dismenore, diş ağrısı, nevralji, kas ve eklem ağrıları) semptomatik tedavisinde; ayrıca soğuk algınlığı ve grip gibi enfeksiyonlara bağlı ateşin düşürülmesinde endikedir.

1.2 Pozoloji ve Uygulama Şekli:
Yetişkinlerde her 4-6 saatte bir 1-2 tablet alınabilir. Maksimum günlük doz 4000 mg'ı aşmamalıdır. Uzun süreli ve yüksek doz kullanımı hepatotoksisite riskini artırır.

1.3 Kontrendikasyonlar:
Parasetamole veya yardımcı maddelerden herhangi birine karşı aşırı duyarlılığı olanlarda kontrendikedir. Şiddetli karaciğer yetmezliği (Child-Pugh > 9) ve aktif böbrek yetmezliği vakalarında kesinlikle kullanılmamalıdır. 

1.4 Özel Kullanım Uyarıları:
Alkolik karaciğer hastalarında dikkatli olunmalıdır. Alkol ile eş zamanlı kullanım karaciğer hasar riskini katlanarak artırır.

1.5 İstenmeyen Etkiler (Yan Etkiler):
Çok seyrek: Trombositopeni, lökopeni, pankreatit, anaflaksi, Stevens-Johnson Sendromu (ciddi cilt döküntüleri).
Yaygın: Bulantı, kusma ve dispepsi.
"""
        },
        {
            "filename": "aspirin_prospektus.pdf",
            "content": """TIBBİ ÜRÜNÜN ADI: Aspirin 100mg Enterik Kaplı Tablet (Asetilsalisilik Asit)
1. KLİNİK ÖZELLİKLER
1.1 Terapötik Endikasyonlar:
Akut miyokard enfarktüsü (kalp krizi) riskini azaltmak, iskemik inme geçiren hastalarda sekonder koruma sağlamak, anjina pektoris tedavisi ve stent takılmış hastalarda tromboz oluşumunu engellemek amacıyla antitrombotik olarak kullanılır.

1.2 Pozoloji ve Uygulama Şekli:
Doktor tavsiyesi ile günde 1 tablet (100mg) tok karnına, bol su ile yutulmalıdır. Çiğnenmemeli veya kırılmamalıdır.

1.3 Kontrendikasyonlar:
Aktif peptik ülser hastalarında, hemofili veya diğer kanama bozukluklarında kontrendikedir. Gebeliğin son trimesterinde kullanımı kalp defektlerine yol açabileceği için kesinlikle yasaktır. 16 yaş altı viral enfeksiyon (örn: suçiçeği) geçiren çocuklarda Reye Sendromu riski nedeniyle kullanılmamalıdır (KIRMIZI ALARM).

1.4 İstenmeyen Etkiler (Yan Etkiler):
Yaygın: Mide yanması, dispepsi, mide bağırsak kanamaları.
Seyrek: Kulak çınlaması (tinnitus), baş dönmesi, böbrek fonksiyonlarında bozulma ve astım krizini tetikleme (astımlı hastalarda).
"""
        },
        {
            "filename": "ibuprofen_prospektus.pdf",
            "content": """TIBBİ ÜRÜNÜN ADI: İbuprofen 400mg Film Tablet
1. KLİNİK ÖZELLİKLER
1.1 Terapötik Endikasyonlar:
Romatoid artrit, osteoartrit, ankilozan spondilit gibi romatizmal hastalıkların semptomatik tedavisinde; şiddetli diş ağrısı, kas iskelet sistemi ağrıları ve primer dismenore (adet sancısı) tedavisinde anti-inflamatuar ve analjezik olarak kullanılır.

1.2 Kontrendikasyonlar:
Daha önce ibuprofen veya diğer NSAİİ'lere karşı astım, rinit, ürtiker öyküsü olan hastalarda kontrendikedir. Gastrointestinal kanama ve perforasyon öyküsü olanlarda, şiddetli kalp yetmezliği (NYHA sınıf IV) bulunanlarda kullanılmamalıdır.

1.3 Özel Uyarılar:
Kardiyovasküler trombotik olay (kalp krizi ve inme) riskini artırabilir. Hipertansiyon (yüksek tansiyon) hastalarında kan basıncını kontrolsüz şekilde yükseltebileceğinden dikkatle izlenmelidir. Gebeliğin son 3 ayında duktus arteriozusun erken kapanmasına neden olabilir (KIRMIZI ALARM).

1.4 İstenmeyen Etkiler:
Yaygın: Mide ağrısı, mide ülseri, gastrointestinal kanama, bulantı, baş ağrısı, periferal ödem.
Çok Seyrek: Karaciğer enzimlerinde yükselme, akut böbrek yetmezliği, aseptik menenjit.
"""
        },
        {
            "filename": "ketya_prospektus.pdf",
            "content": """TIBBİ ÜRÜNÜN ADI: Ketya 150mg Uzatılmış Salımlı Tablet (Ketiapin)
1. KLİNİK ÖZELLİKLER
1.1 Terapötik Endikasyonlar:
Şizofreni tedavisi, bipolar bozukluğa eşlik eden manik ve depresif atakların tedavisi, majör depresif bozuklukta antidepresanlara ek tedavi (add-on) olarak onaylanmıştır.

1.2 Kontrendikasyonlar:
Ketiapin veya ilacın bileşimindeki maddelerden herhangi birine aşırı duyarlılığı olanlarda, HIV proteaz inhibitörleri ve azol sınıfı antifungaller (ketokonazol vb.) ile eş zamanlı kullanımda kontrendikedir.

1.3 Özel Uyarılar (Kara Kutu Uyarısı):
Antidepresan ilaçlar, çocuk ve genç yetişkinlerde (24 yaş altı) intihar düşünce ve davranışlarını (suisidalite) artırabilir (KIRMIZI ALARM). Yaşlı demans hastalarında antipsikotik kullanımı inme ve ani ölüm riskini artırır, bu grupta kullanımı onaylı değildir. İlaç, ciddi hiperglisemi (diyabet) ve metabolik sendroma yol açabilir.

1.4 İstenmeyen Etkiler:
Çok Yaygın: Şiddetli sedasyon (uyku hali), baş dönmesi, ağız kuruluğu, kilo artışı, dislipidemi (kolesterol yükselmesi).
Seyrek: Nöroleptik Malign Sendrom, tardiv diskinezi, tiroid hormon seviyelerinde düşüş.
"""
        }
    ]
    
    for drug in drugs:
        output_path = os.path.join(corpus_path, drug["filename"])
        generate_pdf_report(drug["content"], output_path)
        print(f"Örnek detaylı PDF oluşturuldu: {output_path}")

if __name__ == "__main__":
    main()
