import requests
from bs4 import BeautifulSoup
import time
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# توکن ربات تلگرام خود را در اینجا قرار دهید
telegram_token = "6394164960:AAENGcqk-OM5yT3DxUjN4p_pmwJrH_Xxi_4"

# آیدی گروه یا کانال تلگرام خود را در اینجا قرار دهید
telegram_chat_id = "4023405223"

# URL مورد نظر را در اینجا قرار دهید
divar_url = "https://divar.ir/s/tehran-province/car/peugeot/pars"

# تابع برای ارسال پیام به تلگرام
def send_to_telegram(message):
    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id=telegram_chat_id, text=message)

# تابع برای دریافت اطلاعات آگهی
def get_ad_info(ad_url):
    response = requests.get(ad_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("h1", class_="kt-titl-a75eb")
        description = soup.find("p", class_="kt-desc-6e63c")
        image = soup.find("img", class_="kt-image-7cf97")["src"]
        return {
            "title": title.text if title else "عنوان نامشخص",
            "description": description.text if description else "توضیحات نامشخص",
            "image": image if image else ""
        }
    else:
        return None

# تابع اصلی برای پردازش آگهی‌ها
def process_ads():
    response = requests.get(divar_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        ads = soup.find_all("a", class_="kt-list-item-d69b1")
        
        for ad in ads:
            ad_url = ad["href"]
            ad_info = get_ad_info(ad_url)
            if ad_info:
                message = f"**{ad_info['title']}**\n{ad_info['description']}\n[Link]({ad_url})"
                caption = "autoazad.online"
                send_to_telegram(message)
                send_to_telegram(caption)
                time.sleep(2)
    else:
        send_to_telegram("مشکلی در دریافت اطلاعات از دیوار به وجود آمد!")

# شروع اجرای برنامه
if __name__ == "__main__":
    process_ads()
