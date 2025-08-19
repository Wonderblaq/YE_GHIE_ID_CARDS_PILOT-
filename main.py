from PIL import Image, ImageDraw, ImageFont, ImageOps
from card_utils import add_rounded_corners, circular_crop
# generating unique and formatted ids for members
import uuid

# Function to resize font to fit a given width
def fit_text(draw, text, font_path, max_width, max_font_size):
    font_size = max_font_size
    font = ImageFont.truetype(font_path, font_size)

    while draw.textlength(text, font=font) > max_width and font_size > 10:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)

    return font


# connecting to database
import pandas as pd


df = pd.read_csv("/Users/sarfowonder/Desktop/YE_GHIE_FOLDER/ye_ghie_members.csv")
print(df.columns)
df["full_name"] = df["full_name"].str.upper()
df["gender"] = df["gender"].str.upper()

df["institution"] = ["UENR", "KNUST", "KNUST", "UMaT", "UENR"]


# Generate formatted id for each row
# Generate formatted IDs (e.g., UENR-0001, UENR-0002, ...)
df["formatted_id"] = [f"GHIE-{str(i).zfill(6)}" for i in range(1, len(df) + 1)]
# Optionally save back to CSV
df.to_csv("members_with_ids.csv", index=False)

# Show the updated DataFrame
print(df)


# === Positions & Example Data ===
positions = {
    "full_name": (255, 168),
    "institution": (255, 250),
    "member_id": (255, 287),
    "start_date": (255, 329),
    "completion_date": (463, 329),
    "gender": (255, 208),
    "photo_path": (48, 145),
}

# Define max widths for each field
max_widths = {
    "full_name": 50,
    "institution": 50,
    "member_id": 00,
    "start_date": 80,
    "completion_date": 80,
}

# === Draw Text with Dynamic Font Sizing and add font styles ===

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"  # Change if needed
bricolage_font = ImageFont.truetype("/Users/sarfowonder/Downloads/Bricolage_Grotesque"
                                        " (1)/static/BricolageGrotesque_24pt_Condensed-Regular.ttf", size=21)
bricolage_font_2 = ImageFont.truetype("/Users/sarfowonder/Downloads/Bricolage_Grotesque (1)"
                                          "/static/BricolageGrotesque_"
                                          "36pt-Bold.ttf", size=22)
montserrat_font = ImageFont.truetype("/Users/sarfowonder/Downloads/Montserrat/static/Montserrat-Bold.ttf",
                                         size=20)


for idx, row in df.iterrows():
    # === Load Images ===
    base_image = Image.open("/Users/sarfowonder/Downloads/base_image_ye.jpg")
    profile = Image.open("/Users/sarfowonder/Downloads/joel.jpg")
    # Resize base template
    base_resize = base_image.resize((600, 384), Image.LANCZOS)
    base_resize_2 = add_rounded_corners(base_resize, 20)
    # base_resize_2.show()
    # base_resize_2.close()

    base_resize.save("base_image.jpg")
    # Crop profile picture
    passport_pic_size = (186, 211)
    profile_cropped = ImageOps.fit(profile, passport_pic_size, Image.LANCZOS)
    # profile_cropped_2 = circular_crop(profile, (186, 211), border=6, border_color=(255, 255, 255))
    profile_cropped.save("profile_pic.jpg")
    draw = ImageDraw.Draw(base_resize_2)

    # collect member info
    member_data = {"name": row["full_name"],
                   "email": row["email"],
                   "start_date": row["start_date"],
                   "comp_date": row["completion_date"],
                   "gender": row["gender"],
                   "member_id": row["formatted_id"],
                   "institution": row["institution"],
                   }

    # directly drawing on base template to fill in member detail on id card
    draw.text(positions["full_name"], member_data["name"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["completion_date"], member_data["comp_date"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["start_date"], member_data["start_date"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["member_id"], member_data["member_id"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["gender"], member_data["gender"], font=bricolage_font, fill="#2d195e")
    draw.text(positions["institution"], member_data["institution"], font=bricolage_font, fill="#2d195e")

    # === Paste Profile Picture ===
    base_resize_2.paste(profile_cropped, positions["photo_path"])

    # Show Result
    base_resize_2.show()
    base_resize_2.close()

    import os

    # Make sure the cards folder exists
    os.makedirs("cards", exist_ok=True)

    filename = f"cards/{member_data['member_id']}.png"
    base_resize.save(filename)

    print(f"✅ Saved card for {member_data['name']} → {filename}")

# Generate UUID for each row
# for _ in range(len(df)):
   # df["uuid"] = str(uuid.uuid4().hex[:10])

# import os
# from pathlib import Path

# fonts_dirs = [Path("/System/Library/Fonts"), Path("/Library/Fonts"), Path("~/Library/Fonts").expanduser()]
# for dir in fonts_dirs:
# for font in dir.glob("*.ttf"):
import smtplib
from email.mime.text import MIMEText

# Your Brevo SMTP credentials
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "wondersarfo0@gmail.com"   # the sender email you verified
SMTP_PASSWORD = "x0QjVPgc7EbN41am"     # the SMTP key from Brevo

# Email details
sender = SMTP_USERNAME
for index, row in df.iterrows():
    recipient = row["email"]
    name = row["full_name"]
    subject = "YE-GHIE ID GENERATION TEST MAIL"
    body = f"Hello {name}, this is a test email sent to you via YE-Ghie for your ID."

    # Create email
    msg = MIMEText(body, "plain")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

    print("✅ Email sent successfully!")
