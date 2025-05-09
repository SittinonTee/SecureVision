from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import requests
from linebot.models import TextSendMessage, LocationSendMessage

from playsound import playsound
import threading


from linebot import LineBotApi
from linebot.models import FlexSendMessage
from linebot.exceptions import LineBotApiError



cooldown = 10
checkcamara = False
app = Flask(__name__)
CORS(app)





def notipolice():
             return FlexSendMessage(
                    alt_text="ข้อมูลสถานีตำรวจภูธรปากคลองรังสิต",
                    contents={
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://pakklongrangsit.pathumthani.police.go.th/wp-content/uploads/2024/02/2017-12-05.jpg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "สถานีตำรวจภูธรปากคลองรังสิต",
                                    "weight": "bold",
                                    "size": "lg",
                                    "wrap": True
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "ที่อยู่",
                                                    "color": "#aaaaaa",
                                                    "size": "sm",
                                                    "flex": 1
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "1/3 ถ.ติวานนท์ ซ.วัดเทียนถวาย ต.บ้านใหม่ อ.เมืองปทุมธานี จ.ปทุมธานี 12000",
                                                    "wrap": True,
                                                    "color": "#666666",
                                                    "size": "sm",
                                                    "flex": 5
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "โทร",
                                                    "color": "#aaaaaa",
                                                    "size": "sm",
                                                    "flex": 1
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "02-501-2298",
                                                    "wrap": True,
                                                    "color": "#666666",
                                                    "size": "sm",
                                                    "flex": 5
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "เปิดแผนที่",
                                        "uri": "https://maps.app.goo.gl/kqWS3i5a79WPvFaA6?g_st=com.google.maps.preview.copy"
                                    }
                                }
                            ],
                            "flex": 0
                        }
                    }
                )






# -------------------------------------------------------------------------------------------
CHANNEL_ACCESS_TOKEN = '/UkzHH4da+E2/6RoWZCV3R9c5GyheB9P65Tm9gkoUjxArkW9d43UA41/XbNKqJYQTNQziWDLhbyXq8XVZYuoqdp8zds3fXyTDjIYYLbFDHfYHQ8DvZqU4z8p7jJ4xO2l1anZoPRRLXYQ+MinJh4IfwdB04t89/1O/w1cDnyilFU='
USER_ID = 'U8a55643a4198089d5179aa112a66c360'


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def reply_to_line(reply_token, message_text):
    url = 'https://api.line.me/v2/bot/message/reply' 
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    body = {
        'replyToken': reply_token,
        'messages': [{
            'type': 'text',
            'text': str(message_text)
        }]
    }
    response = requests.post(url, headers=headers, json=body)
    print(f"LINE API response: {response.status_code} - {response.text}")
    return response.status_code == 200


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Received webhook: {data}")

    events = data.get('events', [])
    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_message = event['message']['text'].lower()
            reply_token = event['replyToken']
            reply_text = None

            if "เสียงแจ้งเตือน" in user_message:
                for _ in range(3):
                    threading.Thread(target=playsound, args=("alert.mp3",)).start()
                reply_text = "ระบบได้เปิดเสียงแจ้งเตือนให้คุณแล้ว"
            elif "ยืนยัน" in user_message:
                global cooldown
                cooldown = 30
                messages = [
                    TextSendMessage(text="ยืนยันบุคคลในภาพ"),
                    TextSendMessage(text=f"เราจะไม่แจ้งเตือนอีกเป็นเวลา {cooldown} นาที")
                ]
                line_bot_api.reply_message(reply_token, messages)



            elif "ติดต่อเจ้าหน้าที่" in user_message:
                flex_message = notipolice()

                line_bot_api.push_message(USER_ID, flex_message)

            elif "ปฏิเสธ" in user_message:
                reply_text = "⚠️ระบบได้รับการปฏิเสธตัวตนแล้ว กรุณาติดต่อเจ้าหน้าที่..."

                flex_message = notipolice()
                line_bot_api.push_message(USER_ID, flex_message)
          


            elif "ขอดูภาพจากกล้อง" in user_message or "กล้อง" in user_message:
                global checkcamara
                checkcamara = True
                reply_text = "กำลังส่งภาพจากกล้องให้คุณ"
     

            else:
                reply_text = f"คุณพิมพ์ว่า: {user_message}"

            if reply_text:
                reply_to_line(reply_token, reply_text)

    return jsonify({'status': 'ok'}), 200
# -------------------------------------------------------------------------------------------



@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/imgs/<path:filename>')
def serve_image(filename):
    return send_from_directory('imgs', filename)



@app.route('/set_cooldown', methods=['POST'])
def set_cooldown():
    global cooldown
    data = request.get_json()
    cooldown = data.get("value", 10)
    # print(f"Set cooldown to {cooldown}")
    return jsonify({"cooldown": cooldown})

@app.route('/get_cooldown', methods=['GET'])
def get_cooldown():
    return jsonify({"cooldown": cooldown})

@app.route('/set_checkcamara', methods=['POST'])
def set_checkcamara():
    global checkcamara
    data = request.get_json()
    checkcamara = data.get("value", False)
    # print(f"Set checkcamara to {checkcamara}")
    return jsonify({"value": checkcamara})

@app.route('/get_checkcamara', methods=['GET'])
def get_checkcamara():
    # print(f"Get checkcamara: {checkcamara}")
    return jsonify({"value": checkcamara})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)