# OYSUygulama

Bu proje, PyQt5 kullanılarak yapılmış basit bir öğrenci yönetim sistemidir.

## Özellikler
- Öğrenci ekleme (isim, yaş, not)
- Notu 50 ve üzeri olan öğrencileri listeleme
- Öğrenci arama
- Tablo üzerinde öğrenci bilgilerini gösterme
- Hatalı tekrar kayıt durumunda uyarı mesajı

## Kullanım
- `btn_ekle`: Yeni öğrenci ekler
- `btn_guncelle`: Checkbox işaretliyse geçen öğrencileri gösterir
- `btn_arama`: İsim ile arama yapar

## Gereksinimler
- Python 3.x
- PyQt5 kütüphanesi (`pip install PyQt5`)

## Çalıştırma
python OYSUygulama.py

## Bilinen Hatalar

- İsim kısmına numara girilebilir; bunun hata olup olmadığına emin değilim.
- Not girişinde sayı dışında değer girilirse hata yakalama yapılmamıştır.
- Arama sadece tam eşleşme ile çalışıyor, kısmi arama desteklenmiyor.
- GUI tasarımı çok basit, kullanıcı deneyimi geliştirilebilir.
