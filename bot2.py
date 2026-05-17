import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from twilio.rest import Client

TELEGRAM_BOT_TOKEN = "8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg"
TWILIO_ACCOUNT_SID = "AC93fa6ab5de0da1e3dd0de4714b6105cc"
TWILIO_AUTH_TOKEN  = "8beb0feca4d769689e03ecee7565cd13"
TWILIO_FROM_NUMBER = "+19165716526"
NEXFIELD_NUMBER    = "+19165071904"
ALLOWED_CHAT_ID = 6417548865

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def extract_phone(text):
    patterns = [r'\+1\s?\d{10}', r'\+\d{11,12}', r'\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            digits = re.sub(r'[^\d]', '', match.group())
            if len(digits) == 10:
                return f"+1{digits}"
            elif len(digits) >= 11:
                return f"+{digits}"
    return None

def make_call(to_number):
    call = twilio_client.calls.create(
        to=to_number,
        from_=TWILIO_FROM_NUMBER,
        twiml=f"<Response><Say>Please hold.</Say><Dial>{NEXFIELD_NUMBER}</Dial></Response>"
    )
    return call.sid

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return
    if ALLOWED_CHAT_ID and message.chat_id != ALLOWED_CHAT_ID:
        return
    phone = extract_phone(message.text)
    if not phone:
        return
    try:
        call_sid = make_call(phone)
        await message.reply_text(f"Calling {phone}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
