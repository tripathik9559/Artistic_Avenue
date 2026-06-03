# Artistic Avenue 🎨

A full-stack Django-based art marketplace platform where artists can showcase and sell their artwork, users can explore and purchase paintings, and administrators manage the platform through a dedicated portal.

---

## ✨ Features

### 👤 User Features

* User registration and login
* Browse artworks and artist profiles
* Purchase paintings and artworks
* Manage personal account

### 🎨 Artist Features

* Artist registration and login
* Upload and manage artworks
* Showcase artist profile
* Track artwork listings

### 🛠️ Admin Features

* Dedicated admin portal
* Manage artists and users
* Monitor platform activities
* Manage artwork listings

---

## 🏗️ Tech Stack

| Category        | Technology            |
| --------------- | --------------------- |
| Backend         | Python, Django        |
| Frontend        | HTML, CSS, JavaScript |
| Database        | SQLite                |
| Media Handling  | Pillow                |
| Version Control | Git & GitHub          |

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Artistic_Avenue.git
cd Artistic_Avenue
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install django pillow
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Start Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

---

## 🔑 Access Information

### Admin Portal

```text
URL: /portal/
```

Default credentials may vary depending on local database configuration.

---

## 📁 Project Structure

```text
Artistic_Avenue/
│
├── Artistic_Avenue/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── aa_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
├── media/
├── db.sqlite3
├── manage.py
└── README.md
```

---

## 🎯 Project Purpose

Artistic Avenue was developed as a full-stack web application to provide a platform where artists can digitally showcase their work and connect with potential buyers through an easy-to-use marketplace.

---

## 📸 Screenshots

Add screenshots here after deployment:

* Home Page
* Artwork Gallery
* Artist Dashboard
* Admin Portal
* User Dashboard

---

## 👨‍💻 Author

Kartikey Kumar Tripathi

GitHub: https://github.com/tripathik9559

LinkedIn: https://www.linkedin.com/in/kartikey-kumar-tripathi-92912b29b
