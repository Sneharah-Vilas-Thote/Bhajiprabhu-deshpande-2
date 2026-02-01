import cv2
import uuid
from supabase import create_client

# ---------- SUPABASE ----------
SUPABASE_URL = "https://pzfjuwkkymnjuptoxjyf.supabase.co"
SUPABASE_KEY = "sb_publishable_6fghcBjuwEfcwR8ux5ujTg_nUDuTl53"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

email = input("User Email paste karo: ")

# ---------- CAMERA ----------
cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print("📷 Face register ho raha hai...")

face_img = None
for _ in range(20):
    ret, frame = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 1:
        x, y, w, h = faces[0]
        face_img = frame[y:y+h, x:x+w]
        break

cam.release()

if face_img is None:
    print("❌ Face detect nahi hua")
    exit()

# ---------- SAVE IMAGE ----------
safe_email = email.replace("@", "_").replace(".", "_")
filename = f"{safe_email}_{uuid.uuid4()}.jpg"
cv2.imwrite(filename, face_img)

# ---------- UPLOAD TO STORAGE ----------
supabase.storage.from_("faces").upload(
    filename,
    open(filename, "rb"),
    {"content-type": "image/jpeg"}
)

# ---------- DB ENTRY ----------
supabase.table("face_data").insert({
    "Email": email,           # TEXT column
    "encoding": filename,
    "image_path": filename
}).execute()

print("✅ Face registered successfully")
