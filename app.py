from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from info import getAll

import os

# ----------------- ค่าที่คุณต้องเปลี่ยน -----------------
# แทนที่ด้วย Channel Access Token ของคุณ
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN") 
LINE_CHANNEL_SECRET = os.environ.get("LINE_SECRET")
# ----------------------------------------------------

app = Flask(__name__)

# สร้าง Object สำหรับการเชื่อมต่อกับ LINE API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Endpoint ที่ LINE จะส่งข้อความมาหา (Webhook URL)
@app.route("/callback", methods=['POST'])
def callback():
    # ดึงค่า X-Line-Signature header เพื่อตรวจสอบความถูกต้อง
    signature = request.headers.get('X-Line-Signature')
    
    # ดึงข้อมูล Request Body
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # จัดการ Event
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/secret.")
        abort(400)

    return 'OK'

# จัดการกับข้อความที่เป็นประเภท Text (ตัวอักษร)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text # ข้อความที่ผู้ใช้พิมพ์มา
    
    # 💡 Logic การตอบกลับ:
    if "สวัสดี" in user_message:
        reply_text = "สวัสดีครับ! บอทรับทราบข้อความของคุณแล้ว"
    elif "now" in user_message:
        # สามารถเรียกใช้ฟังก์ชันดึงข้อมูลทองคำจาก Investing.com ที่คุณทำไว้ก่อนหน้ามาใส่ตรงนี้ได้
        reply_text = getAll()
    else:
        reply_text = f"คุณพูดว่า: '{user_message}'"
        
    # ส่งข้อความตอบกลับ
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

