import cv2
from datetime import date
from supabase import create_client

SUPABASE_URL = "https://pzfjuwkkymnjuptoxjyf.supabase.co"
SUPABASE_KEY = "sb_publishable_6fghcBjuwEfcwR8ux5ujTg_nUDuTl53"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

user_id = input("User ID paste karo: ")

cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print("📷 Face verify ho raha hai...")

face_found = False
for _ in range(20):
    ret, frame = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 1:
        face_found = True
        break

cam.release()

if not face_found:
    print("❌ Face nahi mila, attendance cancel")
    exit()

supabase.table("attendance").insert({
    "user_id": user_id,
    "date": str(date.today()),
    "status": "Present"
}).execute()

print("✅ Attendance marked")
