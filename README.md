**Digital ID Automation System**

This project automates the generation and distribution of digital ID cards for members. It eliminates manual work by integrating Python scripts, Firebase, and email automation to streamline the entire process.

📌 Features

**Automated ID Generation**

Creates personalized digital ID cards (PDF format) for each member.

Uses member details (name, ID, role, etc.) directly from the database.

**Email Automation**

Automatically sends ID cards as email attachments to members.

Ensures timely delivery and eliminates human error.

**Database Integration (Ongoing)**

Connected to Firebase for real-time data sync.

Fetches new members directly from Firebase (no manual export).

Updates member records after ID delivery (to prevent duplicates).

**Scalability**

Can handle hundreds of members at once.

Easily extendable for other organizations or student bodies.

****🛠️ Tech Stack****

Python (Core automation)

Firebase (Data storage & real-time updates)

SMTP / Gmail API (Email distribution)

ReportLab (PDF ID card generation)

React for Forms to generate member data 

**📂 Project Workflow**

Fetch Data with react form app 

Retrieve member details from Firebase (or CSV/Excel fallback).

Generate ID

Python script creates a digital ID card for each member.

Send Email

ID cards are emailed automatically to each member’s registered email.

Update Records (planned)

Mark member as “ID Sent” in Firebase to avoid duplicates.


**📊 Impact**

Saves hours of manual work.

Ensures every member gets their ID without delays.

Creates a foundation for scalable, automated membership systems.
**
🤝 Contributors**

Sarfo Nana Osei Wonder – Python Automation, Email Integration

Senyo Ahadzi Joel – React Form App + Firebase Setup

✨ With this system, ID distribution is no longer a manual process — it’s smart, automated, and scalable.
