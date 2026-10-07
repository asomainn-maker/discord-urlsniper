import asyncio
import aiohttp
import time

# ==========================================
# --- AYARLAR (BURAYI DÜZENLE) ---
# ==========================================
# Bot tokenin veya yüksek yetkili bir User Token (User tokenler daha hızlı olabilir ama risklidir)
TOKEN = "TOKENİNİ_BURAYA_YAZ"

# Hedef Server ID'si (URL'nin atanacağı senin serverin)
GUILD_ID = "SENİN_SERVER_IDN"

# Hedef URL'ler (Sadece son kısmı yaz: discord.gg/abc ise sadece 'abc' yaz)
# Boş bıraktıkların kontrol edilmeyecek.
TARGET_URLS = [
    "hedef1", 
    "abc", 
    "ruhsuz", 
    "",       
    "premium" 
]

# Kontrol hızı (Saniye cinsinden). Çok düşük yaparsan Discord seni banlar (Rate Limit).
# 0.1 ile 0.5 arası idealdir.
CHECK_INTERVAL = 0.2 
# ==========================================

async def check_and_claim(session, url_code):
    """Belirli bir URL'yi kontrol eder ve boşsa hemen kapar."""
    if not url_code: 
        return

  
    check_url = f"https://discord.com/api/v9/invites/{url_code}"
    claim_url = f"https://discord.com/api/v9/guilds/{GUILD_ID}/vanity-url"
    
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari<unused54> same-site"
    }

    payload = {"code": url_code}

    while True:
        try:
            
            async with session.get(check_url, headers=headers) as resp:
                if resp.status == 404:
                   
                    print(f"[!] HEDEF YAKALANDI: {url_code} | Kapma işlemi başlatılıyor...")
                    
                    async with session.patch(claim_url, headers=headers, json=payload) as claim_resp:
                        if claim_resp.status == 200:
                            print(f"✅ BAŞARILI! {url_code} artık senin serverinde!")
                            return True 
                        else:
                            print(f"❌ Başarısız: {await claim_resp.text()}")
                elif resp.status == 200:
                
                    pass 
                elif resp.status == 429:
                  
                    retry_after = (await resp.json()).get("retry_after", 1)
                    print(f"⚠️ Rate limit! {retry_after} sn bekleniyor...")
                    await asyncio.sleep(retry_after)

        except Exception as e:
            print(f"[-] Hata oluştu ({url_code}): {e}")

        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    print("🚀 WormGPT Hyper-Sniper Başlatıldı...")
    print(f"🎯 İzlenen URL Sayısı: {len([u for u in TARGET_URLS if u])}")
    print("--------------------------------------------------")

    async with aiohttp.ClientSession() as session:
       
        tasks = []
        for url in TARGET_URLS:
            if url: 
                tasks.append(check_and_claim(session, url))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Sniper durduruldu.")
