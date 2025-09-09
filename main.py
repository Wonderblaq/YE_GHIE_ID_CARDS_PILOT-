from PIL import Image, ImageDraw, ImageFont, ImageOps
from card_utils import add_rounded_corners, circular_crop
import pandas as pd
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

# === Load Members ===
df = pd.read_csv(r"E:\ye_ghie_members.csv.csv")

df["full_name"] = df["full_name"].str.upper()
df["gender"] = df["gender"].str.upper()
df["institution"] = ["UENR", "KNUST", "KNUST", "UMaT", "UENR"]

# Generate formatted IDs (e.g., GHIE-000001, GHIE-000002, ...)
df["formatted_id"] = [f"GHIE-{str(i).zfill(6)}" for i in range(1, len(df) + 1)]

print(df.head())

# === Positions ===
positions = {
    "full_name": (255, 168),
    "institution": (255, 250),
    "member_id": (255, 287),
    "start_date": (255, 329),
    "completion_date": (463, 329),
    "gender": (255, 208),
    "photo_path": (48, 145),
}

font_path = r"E:\Bricolage_Grotesque (1)\static\BricolageGrotesque_24pt_Condensed-Regular.ttf"
bricolage_font = ImageFont.truetype(font_path, size=21)

# === Email Config ===
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SENDER = "Admin@yeghie.com"
SMTP_USERNAME = "969923001@smtp-brevo.com"
SMTP_PASSWORD = "txFjrPwSvcWazQH5"

for idx, row in df.iterrows():
    # === Generate ID Card in memory ===
    base_image = Image.open(r"C:\Users\USER\PycharmProjects\YE_GHIE_ID_CARDS_PILOT-\base_image.jpg")
    profile = Image.open(r"C:\Users\USER\PycharmProjects\YE_GHIE_ID_CARDS_PILOT-\profile_pic.jpg")

    base_resize = base_image.resize((600, 384), Image.LANCZOS)
    base_resize_2 = add_rounded_corners(base_resize, 20)

    passport_pic_size = (186, 211)
    profile_cropped = ImageOps.fit(profile, passport_pic_size, Image.LANCZOS)

    draw = ImageDraw.Draw(base_resize_2)

    # Collect data
    member_data = {
        "name": row["full_name"],
        "email": row["email"],
        "start_date": row["start_date"],
        "comp_date": row["completion_date"],
        "gender": row["gender"],
        "member_id": row["formatted_id"],
        "institution": row["institution"],
    }

    # Draw text
    draw.text(positions["full_name"], member_data["name"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["completion_date"], member_data["comp_date"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["start_date"], member_data["start_date"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["member_id"], member_data["member_id"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["gender"], member_data["gender"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["institution"], member_data["institution"], font=bricolage_font, fill="#2d195e")

    # Paste profile
    base_resize_2.paste(profile_cropped, positions["photo_path"])

    # Save to buffer instead of file
    buffer = BytesIO()
    base_resize_2.save(buffer, format="PNG")
    buffer.seek(0)

    # === Email with Attachment ===
    recipient = row["email"]
    subject = "Your YE-GHIE ID Card"
    body = f"Hello {member_data['name']},\n\nPlease find attached your official YE-GHIE ID card.\n\nRegards,\nYE-GHIE Team"

    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach card from buffer
    part = MIMEBase("application", "octet-stream")
    part.set_payload(buffer.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={member_data['member_id']}.png")
    msg.attach(part)

    # Send mail
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER, recipient, msg.as_string())

    print(f"✅ Sent ID card to {recipient}")

print("🎉 All emails sent successfully")
