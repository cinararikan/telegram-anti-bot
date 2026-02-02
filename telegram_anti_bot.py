#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Kanal Anti-Bot Sistemi
Sahte bot abonelerini otomatik tespit edip temizler
"""

import logging
from datetime import datetime, timedelta
from collections import deque
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes
from telegram.error import TelegramError
import asyncio

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== AYARLAR ====================
BOT_TOKEN = "8456368517:AAExTQES9yRFW6UawjAgKcpT69AkkKq92OA"
CHANNEL_ID = -1003685950110  # Kanalınızın ID'si (negatif sayı olacak)
ADMIN_USER_ID = 5670703958  # Sizin Telegram kullanıcı ID'niz (bildirim için)

# Saldırı tespit ayarları
THRESHOLD_TIME_SECONDS = 60  # Kontrol süresi (saniye) - 1 dakika
THRESHOLD_COUNT = 10  # Bu sürede kaç kişi gelirse saldırı sayılsın
CLEANUP_WINDOW_MINUTES = 2  # Kaç dakika geriye gidip temizlesin

# Normal moda dönüş ayarları
NORMAL_MODE_THRESHOLD = 10  # Dakikada bu sayının altı = normal mod
ATTACK_MODE_COOLDOWN = 120  # Saldırı bitince kaç saniye beklesin (2 dakika)

# ==================== GLOBAL DEĞİŞKENLER ====================
recent_joins = deque()  # Son katılımları tutar: (user_id, username, timestamp)
attack_mode = False  # Şu an saldırı modu aktif mi?
attack_start_time = None  # Saldırı ne zaman başladı
total_banned_in_attack = 0  # Bu saldırıda kaç kişi banlandı


def is_attack_detected():
    """
    Son THRESHOLD_TIME_SECONDS içinde THRESHOLD_COUNT'tan fazla katılım var mı kontrol et
    """
    now = datetime.now()
    cutoff_time = now - timedelta(seconds=THRESHOLD_TIME_SECONDS)
    
    # Son X saniyedeki katılımları say
    recent_count = sum(1 for _, _, join_time in recent_joins if join_time > cutoff_time)
    
    return recent_count >= THRESHOLD_COUNT


async def send_admin_notification(context: ContextTypes.DEFAULT_TYPE, message: str):
    """
    Admin'e bildirim gönder
    """
    try:
        await context.bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=f"🚨 *KANAL KORUMA BOT*\n\n{message}",
            parse_mode='Markdown'
        )
        logger.info(f"Admin bildirimi gönderildi: {message}")
    except Exception as e:
        logger.error(f"Admin bildirimi gönderilemedi: {e}")


async def ban_user(context: ContextTypes.DEFAULT_TYPE, user_id: int, username: str):
    """
    Kullanıcıyı kanaldan banla
    """
    try:
        await context.bot.ban_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )
        logger.info(f"✅ Banlandi: {username} (ID: {user_id})")
        return True
    except TelegramError as e:
        logger.error(f"❌ Ban hatası {username}: {e}")
        return False


async def cleanup_recent_joins(context: ContextTypes.DEFAULT_TYPE):
    """
    Son CLEANUP_WINDOW_MINUTES dakikadaki tüm katılımları banla
    """
    global total_banned_in_attack
    
    now = datetime.now()
    cutoff_time = now - timedelta(minutes=CLEANUP_WINDOW_MINUTES)
    
    # Banlanacakları belirle
    to_ban = [
        (user_id, username) 
        for user_id, username, join_time in recent_joins 
        if join_time > cutoff_time
    ]
    
    banned_count = 0
    for user_id, username in to_ban:
        if await ban_user(context, user_id, username):
            banned_count += 1
            total_banned_in_attack += 1
            # Rate limiting için kısa bekleme
            await asyncio.sleep(0.05)
    
    return banned_count


async def track_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Yeni üyeleri izle ve gerekirse saldırı modunu aktive et
    """
    global attack_mode, attack_start_time, total_banned_in_attack, recent_joins
    
    try:
        # Sadece kanalımızı izle
        if update.chat_member.chat.id != CHANNEL_ID:
            return
        
        # Sadece yeni katılımları yakala
        old_status = update.chat_member.old_chat_member.status
        new_status = update.chat_member.new_chat_member.status
        
        if old_status in ["left", "kicked"] and new_status == "member":
            user = update.chat_member.new_chat_member.user
            user_id = user.id
            username = user.username or user.first_name or f"User{user_id}"
            join_time = datetime.now()
            
            # Bot'ları kaydetme
            if user.is_bot:
                logger.info(f"Bot katıldı, atlanıyor: {username}")
                return
            
            # Yeni katılımı kaydet
            recent_joins.append((user_id, username, join_time))
            
            # Eski kayıtları temizle (bellek tasarrufu)
            cutoff = datetime.now() - timedelta(minutes=CLEANUP_WINDOW_MINUTES + 1)
            recent_joins = deque([j for j in recent_joins if j[2] > cutoff])
            
            logger.info(f"📥 Yeni üye: {username} (ID: {user_id})")
            
            # Saldırı kontrolü
            if is_attack_detected():
                if not attack_mode:
                    # Saldırı modu başlat
                    attack_mode = True
                    attack_start_time = datetime.now()
                    total_banned_in_attack = 0
                    
                    logger.warning("🚨 SALDIRI TESPİT EDİLDİ! Temizlik başlıyor...")
                    await send_admin_notification(
                        context,
                        f"⚠️ *BOT SALDIRISI TESPİT EDİLDİ!*\n\n"
                        f"Son {THRESHOLD_TIME_SECONDS} saniyede {len([j for j in recent_joins if j[2] > datetime.now() - timedelta(seconds=THRESHOLD_TIME_SECONDS)])} katılım algılandı.\n"
                        f"Otomatik temizlik başlatıldı..."
                    )
                
                # Saldırı modunda - yeni katılanı hemen banla
                await ban_user(context, user_id, username)
                total_banned_in_attack += 1
            
            else:
                # Normal mod
                if attack_mode:
                    # Saldırı sona erdi
                    attack_mode = False
                    attack_duration = (datetime.now() - attack_start_time).seconds
                    
                    logger.info(f"✅ Saldırı sona erdi. Toplam {total_banned_in_attack} hesap temizlendi.")
                    await send_admin_notification(
                        context,
                        f"✅ *SALDIRI SONA ERDİ*\n\n"
                        f"📊 İstatistikler:\n"
                        f"• Süre: {attack_duration} saniye\n"
                        f"• Temizlenen hesap: *{total_banned_in_attack}*\n"
                        f"• Başlangıç: {attack_start_time.strftime('%H:%M:%S')}\n"
                        f"• Bitiş: {datetime.now().strftime('%H:%M:%S')}\n\n"
                        f"Normal mod devam ediyor."
                    )
                    total_banned_in_attack = 0
                
                logger.info(f"✅ Normal katılım: {username}")
    
    except Exception as e:
        logger.error(f"Hata oluştu: {e}", exc_info=True)


async def periodic_check(context: ContextTypes.DEFAULT_TYPE):
    """
    Periyodik kontrol - saldırı modunda olup olmadığımızı kontrol et
    """
    global attack_mode, recent_joins
    
    # Eski kayıtları temizle
    cutoff = datetime.now() - timedelta(minutes=CLEANUP_WINDOW_MINUTES + 1)
    recent_joins = deque([j for j in recent_joins if j[2] > cutoff])
    
    # Eğer saldırı modundaysak ama artık saldırı yoksa, normal moda dön
    if attack_mode and not is_attack_detected():
        # Biraz daha bekle, belki devam eder
        await asyncio.sleep(10)
        if not is_attack_detected():  # Hala yok mu?
            attack_mode = False
            logger.info("Normal moda dönüldü (periyodik kontrol)")


def main():
    """
    Bot'u başlat
    """
    logger.info("🤖 Telegram Anti-Bot Koruma Sistemi başlatılıyor...")
    logger.info(f"📺 Kanal ID: {CHANNEL_ID}")
    logger.info(f"⚙️ Ayarlar: {THRESHOLD_COUNT} katılım / {THRESHOLD_TIME_SECONDS} saniye")
    logger.info(f"🧹 Temizleme penceresi: {CLEANUP_WINDOW_MINUTES} dakika")
    
    # Application oluştur
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ChatMember güncellemelerini dinle
    application.add_handler(
        ChatMemberHandler(track_member, ChatMemberHandler.CHAT_MEMBER)
    )
    
    # Periyodik kontrol ekle (her 30 saniyede bir)
    application.job_queue.run_repeating(
        periodic_check,
        interval=30,
        first=10
    )
    
    logger.info("✅ Bot hazır ve çalışıyor! Yeni katılımlar izleniyor...")
    logger.info("Durdurmak için CTRL+C basın")
    
    # Bot'u başlat
    application.run_polling(allowed_updates=["chat_member"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot durduruldu.")
    except Exception as e:
        logger.error(f"❌ Kritik hata: {e}", exc_info=True)
