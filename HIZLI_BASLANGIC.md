# 🚀 HIZLI BAŞLANGIÇ (5 Dakikada Kurulum)

## 1️⃣ Bot Oluştur (1 dakika)
- Telegram'da **@BotFather** aç
- `/newbot` yaz
- İsim ver, kullanıcı adı ver
- **Token'ı kaydet** ✍️

## 2️⃣ Kanal ID'ni Bul (1 dakika)
- **@userinfobot** aç
- Kanalından bir mesaj forward et
- **ID'yi kaydet** (örn: -1001234567890) ✍️

## 3️⃣ Kendi ID'ni Bul (30 saniye)
- **@userinfobot** aç
- `/start` yaz
- **ID'ni kaydet** (örn: 123456789) ✍️

## 4️⃣ Bot'u Admin Yap (1 dakika)
- Kanalına git
- Ayarlar → Administrators → Add Administrator
- Bot'unu ekle
- ✅ **Ban users** yetkisi ver

## 5️⃣ Dosyayı Düzenle (1 dakika)
`telegram_anti_bot.py` dosyasını aç:

```python
BOT_TOKEN = "BURAYA_TOKEN"        # ← Buraya yapıştır
CHANNEL_ID = -1001234567890       # ← Buraya yapıştır  
ADMIN_USER_ID = 123456789         # ← Buraya yapıştır
```

## 6️⃣ Çalıştır (30 saniye)

### Windows:
1. `start_bot.bat` dosyasına çift tıkla

### Linux/Mac:
```bash
python3 telegram_anti_bot.py
```

## ✅ TAMAM!

Bot artık çalışıyor. Saldırı olunca size bildirim gelecek ve otomatik temizlenecek.

---

## 🧪 TEST ET

Botun çalışıp çalışmadığını test etmek için:

1. Birkaç arkadaşından kanalına katılmalarını iste
2. Aynı anda 20+ kişi katılırsa saldırı alarmı verecek
3. Normal katılımlarda bir şey yapmayacak

---

## ⚙️ İSTEĞE GÖRE DEĞİŞTİR

Daha hassas yapmak için:
```python
THRESHOLD_COUNT = 10  # Dakikada 10 kişi = alarm
```

Daha toleranslı yapmak için:
```python
THRESHOLD_COUNT = 50  # Dakikada 50 kişi = alarm
```

---

## 🆘 SORUN MU VAR?

**Bot çalışmıyor:**
- Python yüklü mü? → `python --version`
- Paket yüklü mü? → `pip install python-telegram-bot`

**Bildirim gelmiyor:**
- Admin ID doğru mu?
- Bot'a `/start` yazdın mı?

**Ban yapamıyor:**
- Bot admin mi?
- "Ban users" yetkisi var mı?

Detaylı bilgi için `KURULUM_KLAVUZU.md` dosyasını oku.
