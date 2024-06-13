# CE412Deniz Üretim Hattı Simülasyonu

Bu proje, bir üretim hattı simülasyonunu modellemek için geliştirilmiştir. Proje, çeşitli makine türleri ve ürün tiplerini içeren bir üretim hattını simüle ederek performansı değerlendirmeyi amaçlamaktadır. Simülasyon, üretim sürecinde karşılaşılan gecikmeler, bozulmalar ve tamir süreleri gibi faktörleri dikkate alır.

## İçindekiler
- [Proje Açıklaması](#proje-açıklaması)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)


## Proje Açıklaması

Bu proje, lazer kesim, montaj, boyama, kalite kontrol ve ambalajlama gibi çeşitli makine türlerini içeren bir üretim hattını simüle eder. Proje, farklı ürün tipleri (örneğin, metal çerçeveler, ahşap oyuncaklar, plastik konteynerler, elektronik modüller ve cam şişeler) için üretim süreçlerini modelleyerek performansı değerlendirir.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu Klonlayın**:
    ```bash
    git clone https://github.com/kullanici_adi/CE412Deniz.git
    cd CE412Deniz
    ```

2. **Gerekli Paketleri Yükleyin**:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

Simülasyonu çalıştırmak için `main.py` dosyasını çalıştırın. Bu dosya, hem tek ürün tipi hem de çoklu ürün tipi simülasyonlarını çalıştırır ve sonuçları raporlar.

```bash
python main.py
# CE412Deniz
