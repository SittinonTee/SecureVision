from ultralytics import YOLO
import cv2
import time
import numpy as np
import os
import requests

import requests


from linebot import LineBotApi
from linebot.models import FlexSendMessage
from linebot.exceptions import LineBotApiError



def noti_img(image_url, timestamp):
    return FlexSendMessage(
        alt_text="ภาพจากกล้อง - ยืนยันตัวตน",
        contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "ตรวจพบบุคคลที่ไม่รู้จัก",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ff5551",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"คุณต้องการยืนยันหรือไม่? เวลา {timestamp}",
                        "size": "sm",
                        "color": "#aaaaaa",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#00C300",
                        "action": {
                            "type": "message",
                            "label": "✅ ยืนยัน",
                            "text": "ยืนยัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "message",
                            "label": "❌ ปฏิเสธ",
                            "text": "ปฏิเสธ"
                        }
                    }
                ]
            }
        }
    )





def getcamara(image_url, timestamp):
    return FlexSendMessage(
        alt_text="ภาพจากกล้อง - ยืนยันตัวตน",
        contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {  
                        "gravity": "center",
                        "align": "center",
                        "type": "text",
                        "text": "ภาพจากกล้อง ณ บัจจุบันของคุณ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#03a9f4",
                        "wrap": True
                    },
                    # {
                    #     "type": "text",
                    #     "text": f"คุณต้องการยืนยันหรือไม่? เวลา {timestamp}",
                    #     "size": "sm",
                    #     "color": "#aaaaaa",
                    #     "wrap": True,
                    #     "margin": "md"
                    # }
                ]
            },
        }
    )






# --------------------------------------------server---------------------------------------------------
def get_checkcamara():
    try:
        r = requests.get("http://localhost:8000/get_checkcamara")
        result = r.json().get("value", False)
        print(f"Read checkcamara from API: {result}")
        return result
    except Exception as e:
        print(f"ไม่สามารถเรียกใช้ get_checkcamara: {e}")
        return False

def set_checkcamara(value):
    try:
        r = requests.post("http://localhost:8000/set_checkcamara", json={"value": value})
        print(f"Set checkcamara to {value}, response: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"ไม่สามารถเรียกใช้ set_checkcamara: {e}")
        return False

def get_cooldown():
    try:
        r = requests.get("http://localhost:8000/get_cooldown")
        return r.json().get("cooldown", 10)
    except Exception as e:
        print(f"ไม่สามารถเรียกใช้ get_cooldown: {e}")
        return 10


def set_cooldown(value):
    try:
        r = requests.post("http://localhost:8000/set_cooldown", json={"value": value})
        print(f"Set cooldown to {value}, response: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"ไม่สามารถเรียกใช้ set_cooldown: {e}")
        return False

# --------------------------------------------line---------------------------------------------------


CHANNEL_ACCESS_TOKEN = '/UkzHH4da+E2/6RoWZCV3R9c5GyheB9P65Tm9gkoUjxArkW9d43UA41/XbNKqJYQTNQziWDLhbyXq8XVZYuoqdp8zds3fXyTDjIYYLbFDHfYHQ8DvZqU4z8p7jJ4xO2l1anZoPRRLXYQ+MinJh4IfwdB04t89/1O/w1cDnyilFU='
USER_ID = 'U8a55643a4198089d5179aa112a66c360'
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)


IMAGE_URL = 'https://487c-171-7-51-117.ngrok-free.app/imgs/'


# if not os.path.exists("imgs"):
#     os.makedirs("imgs")
#     print("สร้างโฟลเดอร์ imgs สำเร็จ")


def send_line_message(user_id, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    payload = {
        'to': user_id,
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    
    try:
        response = requests.post(LINE_API_URL, headers=headers, json=payload)
        # print(f"ส่งข้อความไปที่ LINE: {message}")
        # print(f"Status code: {response.status_code}, Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการส่งข้อความไปยัง LINE: {e}")
        return False

def send_line_image(user_id, original_content_url, preview_image_url):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    payload = {
        'to': user_id,
        'messages': [{
            'type': 'image',
            'originalContentUrl': original_content_url,
            'previewImageUrl': preview_image_url
        }]
    }
    
    try:
        response = requests.post(LINE_API_URL, headers=headers, json=payload)
        # print(f"ส่งภาพไปยัง LINE: {original_content_url}")
        # print(f"Status code: {response.status_code}, Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการส่งรูปภาพไปยัง LINE: {e}")
        return False

# -------------------------------------------model---------------------------------------------------
# model = YOLO('best111.pt')
model = YOLO('model.pt')
cap = cv2.VideoCapture(0)



confidenceclass = {
    'Au': 0.40,  
    'Gun': 0.30,
    'Tee': 0.80,
    'knife': 0.30,
    'default': 0.75
}


color_dict = {
    'Au': (0, 255, 0),
    'Gun': (255, 0, 0),
    'Tee': (0, 0, 255),
    'knife': (255, 255, 0),
    'Unknown': (128, 128, 128)
}


cv2.namedWindow('Controls')
cv2.createTrackbar('Min Conf', 'Controls', 50, 100, lambda x: None)


start_time = None
unknown_notification_sent = False
last_notification_time = 0

while True:
    checkcamara = get_checkcamara()
    notification_cooldown = get_cooldown() 

    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถอ่านเฟรมจากกล้องได้")
        break
    

    # min_conf = cv2.getTrackbarPos('Min Conf', 'Controls') / 100
    # results = model(frame, conf=min_conf)

    results = model(frame)
    annotated_frame = frame.copy()
    

    checkperson = False
    

    found_gun = False
    found_knife = False
    found_unknown = False

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        
    
        class_conf = confidenceclass.get(class_name, confidenceclass['default'])
        
        # if confidence > class_conf:
        #     display_name = class_name
        #     checkperson = True 
        # else:
        #     display_name = "Unknown"
        

        if confidence > class_conf:
            display_name = class_name
            checkperson = True 
            
            if display_name == "Gun":
                found_gun = True
            elif display_name == "knife":
                found_knife = True
        else:
            display_name = "Unknown"
            found_unknown = True
        
    

        color = color_dict.get(display_name, (128, 128, 128))
        

        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
        label = f"{display_name} {confidence:.2f}"
        

        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(annotated_frame, (x1, y1-text_height-10), (x1+text_width, y1), color, -1)
        cv2.putText(annotated_frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    current_time = time.time()
    

    # if len(results[0].boxes) > 0 and not checkperson or display_name == "Gun" or display_name == "knife":
    if (len(results[0].boxes) > 0 and not checkperson) or found_gun or found_knife:
        if start_time is None:
            start_time = current_time
        elif (current_time - start_time >= 3) and not unknown_notification_sent:

            if current_time - last_notification_time > notification_cooldown:
                unknown_notification_sent = True
                last_notification_time = current_time
                set_cooldown(10)

                
                timestamp = int(time.time())
                filename = f"unknown_{timestamp}.jpg"
                filepath = f"imgs/{filename}"
                cv2.imwrite(filepath, frame)


                image_url = f"{IMAGE_URL}{filename}"
                # if send_line_image(USER_ID, image_url, image_url):
                #     message = f""" พบบุคคลที่ไม่รู้จัก (Unknown)
                #     เวลา {time.strftime('%H:%M:%S', time.localtime())}
                #     กรุณายืนยัน
                #     cooldown: {notification_cooldown} 
                #     """
                    
                #     if send_line_message(USER_ID, message):
                    
                timestamp = time.strftime('%H:%M:%S', time.localtime())
                flex_message = noti_img(image_url, timestamp)
                line_bot_api.push_message(USER_ID, flex_message) 

                # send_line_message(USER_ID, f"cooldown: {notification_cooldown}")
                set_checkcamara(False)
                       

    else:
        start_time = None
        unknown_notification_sent = False


    if checkcamara:
        timestamp = int(time.time())
        filename = f"camera_check_{timestamp}.jpg"
        filepath = f"imgs/{filename}"
        cv2.imwrite(filepath, frame)

        image_url = f"{IMAGE_URL}{filename}"
        timestamp = time.strftime('%H:%M:%S', time.localtime())
        flex_message = getcamara(image_url, timestamp)
        line_bot_api.push_message(USER_ID, flex_message)
        # send_line_message(USER_ID, f"cooldown: {notification_cooldown}")
        set_checkcamara(False)

        # if send_line_image(USER_ID, image_url, image_url):
        #     message = f"""รายงานภาพจากกล้อง
        #     เวลา {time.strftime('%H:%M:%S', time.localtime())}"""
        #     send_line_message(USER_ID, message)

       

 # --------------------------------------------display---------------------------------------------------

    cv2.imshow("Face Detection", annotated_frame)
    # cv2.imshow("Controls", np.zeros((100, 500), dtype=np.uint8))

# --------------------------------------------line---------------------------------------------------
    key = cv2.waitKey(1)
    if key == ord('q'): 
        break
    elif key == ord('t'):
        try:
            timestamp = int(time.time())
            filename = f"test_{timestamp}.jpg"
            filepath = f"imgs/{filename}"
            cv2.imwrite(filepath, frame)

            image_url = f"{IMAGE_URL}{filename}"
            
            if send_line_image(USER_ID, image_url, image_url):
                message = f""" ทดสอบการส่งภาพ
                เวลา {time.strftime('%H:%M:%S', time.localtime())}
                Cooldown: {notification_cooldown} วินาที
                checkcamara: {checkcamara}
                """
                send_line_message(USER_ID, message)
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการทดสอบส่งภาพ: {e}")

cap.release()
cv2.destroyAllWindows()