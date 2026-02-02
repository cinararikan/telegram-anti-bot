# 🤖 Telegram Kanal Anti-Bot Koruma Sistemi

## 📋 Özellikler

✅ **Otomatik Saldırı Tespiti:** Dakikada 20+ katılım = saldırı algılanır
✅ **Anlık Temizleme:** Saldırı anında son 2 dakikadaki tüm katılımları banlar
✅ **Akıllı Normal Mod:** Saldırı bitince otomatik normale döner
✅ **Gerçek Zamanlı Bildirim:** Size Telegram'dan bildirim gönderir
✅ **Gerçek Aboneleri Korur:** Normal hızda gelen kullanıcılara dokunmaz

---

## 🚀 KURULUM ADIMLARI

### Adım 1: Python Kurulumu Kontrolü

Terminal/CMD açın ve şunu yazın:
```bash
python --version
```

Eğer Python 3.8 veya üzeri yoksa, [buradan indirin](https://www.python.org/downloads/)

---

### Adım 2: Telegram Bot Oluşturma

1. Telegram'da **@BotFather** botunu açın
2. `/newbot` komutunu gönderin
3. Bot için bir isim verin (örn: "Kanal Koruyucu")
4. Bot için kullanıcı adı verin (örn: "kanal_koruma_bot")
5. **Bot Token'ınızı kaydedin** (örn: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

📝 **ÖNEMLİ:** Bu token'ı kimseyle paylaşmayın!

---

### Adım 3: Kanal ID'nizi Bulma

#### Yöntem 1: Bot Kullanarak (Kolay)

1. Telegram'da **@userinfobot** botunu açın
2. Kanalınıza gidin
3. Kanaldan bir mesajı @userinfobot'a forward edin
4. Bot size kanal ID'sini verecek (örn: `-1001234567890`)

#### Yöntem 2: Web Telegram Kullanarak

1. [web.telegram.org](https://web.telegram.org) açın
2. Kanalınızı açın
3. URL'e bakın: `https://web.telegram.org/k/#-1234567890`
4. Sayıyı kopyalayın ve başına `-100` ekleyin: `-1001234567890`

---

### Adım 4: Kendi Kullanıcı ID'nizi Bulma

1. Telegram'da **@userinfobot** botunu açın
2. `/start` yazın
3. Size ID'nizi verecek (örn: `123456789`)

---

### Adım 5: Bot'u Kanalınıza Admin Yapma

1. Kanalınızı açın
2. Kanal ayarlarına gidin (⚙️ simgesi)
3. **Administrators** → **Add Administrator**
4. Bot'unuzu arayın ve ekleyin
5. Bot'a şu yetkileri verin:
   - ✅ **Ban users** (Üyeleri yasakla)
   - ✅ **Delete messages** (İsteğe bağlı)

---

### Adım 6: Gerekli Paketleri Kurma

Terminal/CMD'de bot dosyasının olduğu klasöre gidin:

```bash
cd /bot/klasörünün/yolu
```

Ardından gerekli paketi kurun:

```bash
pip install -r requirements.txt
```

VEYA:

```bash
pip install python-telegram-bot==20.7
```

---

### Adım 7: Bot Ayarlarını Yapılandırma

`telegram_anti_bot.py` dosyasını bir metin editörü ile açın.

**Değiştirmeniz gereken satırlar:**

```python
# Satır 23-25
BOT_TOKEN = "BURAYA_BOT_TOKEN_YAZACAKSINIZ"  # @BotFather'dan aldığınız token
CHANNEL_ID = -1001234567890  # Kanalınızın ID'si (negatif sayı)
ADMIN_USER_ID = 123456789  # Sizin Telegram kullanıcı ID'niz
```

**Örnek:**
```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
CHANNEL_ID = -1001234567890
ADMIN_USER_ID = 987654321
```

---

### Adım 8: Bot'u Çalıştırma

Terminal/CMD'de:

```bash
python telegram_anti_bot.py
```

✅ **Başarılı ise şunu görmelisiniz:**
```
🤖 Telegram Anti-Bot Koruma Sistemi başlatılıyor...
📺 Kanal ID: -1001234567890
⚙️ Ayarlar: 20 katılım / 60 saniye
🧹 Temizleme penceresi: 2 dakika
✅ Bot hazır ve çalışıyor! Yeni katılımlar izleniyor...
```

---

## ⚙️ AYARLARI ÖZELLEŞTİRME

`telegram_anti_bot.py` dosyasında bu değerleri değiştirebilirsiniz:

```python
# Satır 28-30
THRESHOLD_TIME_SECONDS = 60  # Kontrol süresi (saniye)
THRESHOLD_COUNT = 20  # Kaç kişi gelirse saldırı sayılsın
CLEANUP_WINDOW_MINUTES = 2  # Kaç dakika geriye gidip temizlesin
```

**Örnek Senaryolar:**

- **Daha hassas:** `THRESHOLD_COUNT = 10` (Dakikada 10 kişi gelirse alarm)
- **Daha toleranslı:** `THRESHOLD_COUNT = 30` (Dakikada 30 kişi gelirse alarm)
- **Daha uzun temizlik:** `CLEANUP_WINDOW_MINUTES = 5` (Son 5 dakikayı temizle)

---

## 🎯 BOT NASIL ÇALIŞIR?

### Normal Mod (Saldırı Yok)
```
18:45:00 → 2 kişi katıldı → ✅ Normal
18:45:30 → 3 kişi katıldı → ✅ Normal
18:46:00 → 1 kişi katıldı → ✅ Normal
```

### Saldırı Modu
```
18:45:00 → 25 kişi katıldı → 🚨 ALARM! Saldırı başladı!
18:45:10 → 50 kişi katıldı → ❌ Hepsi banlaniyor...
18:45:30 → 200 kişi katıldı → ❌ Hepsi banlaniyor...
18:45:50 → 300 kişi katıldı → ❌ Hepsi banlaniyor...
18:46:00 → 2 kişi katıldı → ✅ Saldırı bitti, normal mod
```

**Size gelen bildirim:**
```
🚨 KANAL KORUMA BOT

⚠️ BOT SALDIRISI TESPİT EDİLDİ!

Son 60 saniyede 575 katılım algılandı.
Otomatik temizlik başlatıldı...

---

✅ SALDIRI SONA ERDİ

📊 İstatistikler:
• Süre: 60 saniye
• Temizlenen hesap: 575
• Başlangıç: 18:45:00
• Bitiş: 18:46:00

Normal mod devam ediyor.
```

---

## 🖥️ BOT'U ARKA PLANDA ÇALIŞTIRMA

### Windows için:

1. `start_bot.bat` dosyası oluşturun:
```batch
@echo off
python telegram_anti_bot.py
pause
```

2. Çift tıklayın

### Linux/Mac için:

```bash
nohup python telegram_anti_bot.py > bot.log 2>&1 &
```

Bot'u durdurmak için:
```bash
pkill -f telegram_anti_bot.py
```

---

## 📱 BOT'U SUNUCUDA ÇALIŞTIRMA

### Option 1: VPS/Bulut Sunucu (Önerilen)

1. Bir VPS kiralayın (DigitalOcean, AWS, Hetzner, vb.)
2. Bot dosyalarını sunucuya yükleyin
3. Screen kullanarak çalıştırın:

```bash
screen -S telegram_bot
python telegram_anti_bot.py
# CTRL+A, D tuşlarına basarak çıkın
```

Tekrar bağlanmak için:
```bash
screen -r telegram_bot
```

### Option 2: Systemd Service (Linux)

`/etc/systemd/system/telegram-bot.service` dosyası oluşturun:

```ini
[Unit]
Description=Telegram Anti-Bot Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/telegram_anti_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Servisi başlatın:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

Durumu kontrol edin:
```bash
sudo systemctl status telegram-bot
```

---

## 🔧 SORUN GİDERME

### ❌ "Telegram error: Bad Request: PEER_ID_INVALID"
**Çözüm:** Kanal ID'nizi kontrol edin. `-100` ile başlamalı.

### ❌ "Telegram error: Forbidden"
**Çözüm:** Bot'u kanalınıza admin olarak ekleyin ve "Ban users" yetkisi verin.

### ❌ "No module named 'telegram'"
**Çözüm:** `pip install python-telegram-bot` komutunu çalıştırın.

### ❌ Bot hiç bildirim göndermiyor
**Çözüm:** 
1. ADMIN_USER_ID'yi kontrol edin
2. Bot'a mesaj gönderin (@botusername)
3. `/start` yazın

### ❌ Bot gerçek kullanıcıları da banlıyor
**Çözüm:** `THRESHOLD_COUNT` değerini artırın (örn: 30 veya 50)

---

## 📊 LOG'LARI GÖRÜNTÜLEME

Bot çalışırken terminalden log'ları görebilirsiniz:

```
2025-01-29 18:45:12 - 📥 Yeni üye: user123 (ID: 123456)
2025-01-29 18:45:13 - 📥 Yeni üye: user456 (ID: 789012)
2025-01-29 18:45:15 - 🚨 SALDIRI TESPİT EDİLDİ! Temizlik başlıyor...
2025-01-29 18:45:15 - ✅ Banlandi: user123 (ID: 123456)
2025-01-29 18:45:16 - ✅ Banlandi: user456 (ID: 789012)
```

---

## 📧 DESTEK

Sorun yaşarsanız:
1. Log'ları kontrol edin
2. Ayarları tekrar gözden geçirin
3. Bot'un admin yetkilerini kontrol edin

---

## ⚠️ GÜVENLİK UYARILARI

❗ Bot token'ınızı asla paylaşmayın
❗ Bot dosyasını public GitHub'a yüklemeyin
❗ Token'ı environment variable olarak saklayın (production için)

---

## 🎉 HAZIR!

Artık bot çalışıyor ve kanalınızı koruyacak. Bot saldırılarını otomatik tespit edip temizleyecek ve size bildirim gönderecek.

İyi kullanımlar! 🚀
