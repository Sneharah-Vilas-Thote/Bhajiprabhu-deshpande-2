import cv2
import uuid
import time
import os
from supabase import create_client, Client

# ---------- SUPABASE ----------
SUPABASE_URL = "https://pzfjuwkkymnjuptoxjyf.supabase.co"

# ⚠️ IMPORTANT:
# Hackathon ke liye SERVICE ROLE KEY use karo (dashboard → settings → API)
SUPABASE_KEY = "sb_secret_3FrHKhxshK33PfyCvqmEZw_o9C0iaPx"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- INPUT ----------
email = input("User Email paste karo: ").strip().lower()

if "@" not in email:
    print("❌ Invalid email")
    exit()

# filename safe banane ke liye
safe_email = email.replace("@", "_").replace(".", "_")

# ---------- CAMERA ----------
cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print("📷 Camera ON — ek hi face dikhao...")

face_img = None
start_time = time.time()

while time.time() - start_time < 8:
    ret, frame = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 1:
        x, y, w, h = faces[0]
        face_img = frame[y:y+h, x:x+w]
        break

    elif len(faces) > 1:
        print("⚠ Only ONE face allowed")

cam.release()

if face_img is None:
    print("❌ Face detect nahi hua")
    exit()

# ---------- SAVE IMAGE ----------
filename = f"{safe_email}_{uuid.uuid4()}.jpg"
cv2.imwrite(filename, face_img)

# ---------- UPLOAD TO STORAGE ----------
try:
    with open(filename, "rb") as f:
        supabase.storage.from_("faces").upload(
            path=filename,
            file=f,
            file_options={"content-type": "image/jpeg"}
        )
except Exception as e:
    print("❌ Storage upload failed:", e)
    os.remove(filename)
    exit()

# ---------- DB INSERT ----------
try:
    supabase.table("face_data").insert({
        "Email": email,          # TEXT column
        "encoding": filename,    # image name / future encoding
        "image_path": filename
    }).execute()
except Exception as e:
    print("❌ DB insert failed:", e)
    exit()

print("✅ Face registered successfully 🚀")
