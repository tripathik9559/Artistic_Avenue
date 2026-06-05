# 🎨 Artistic Avenue

A **full-stack art marketplace and community platform** built with Django — connecting artists and art lovers through a beautiful, feature-rich web experience.

## 🌐 Live Demo
**[https://artistic-avenue.onrender.com](https://artistic-avenue.onrender.com)**

| Role | Login URL | Demo Credentials |
|------|-----------|-----------------|
| User | `/user_login/` | Phone: `9999900002` · Password: `demo@user` |
| Artist | `/artist_login/` | Phone: `9999900001` · Password: `demo@artist` |
| Admin | `/portal/` | ID: `admin001` · Password: `admin123` |

---

## ✨ Features

### 👤 For Users (Art Buyers)
- Register & login with phone number
- Browse the **Gallery** — all artworks from all artists
- Visit the **Shop** — buy artworks listed for sale
- Place orders with payment screenshot upload
- **Chat directly** with artists
- Track order history & status
- Submit queries/contact form
- Watch art **tutorial videos** & download **PDF study materials**

### 🎨 For Artists
- Register with art category (Painting, Sculpture, etc.)
- Personal **Artist Dashboard** — view uploaded art & orders
- Upload artworks with image, price, description & sale toggle
- **Mark art as For Sale / Not For Sale**
- Reply to user messages
- Add & manage **Events** (exhibitions, workshops)
- View all incoming orders

### 🛡️ For Admin (Portal)
- Secure admin portal with ID + password
- View all **Users, Artists, Artworks, Orders, Queries**
- Manage order status (Pending → Confirmed → Delivered)
- Upload **tutorial videos** (YouTube links) by category
- Upload **PDF study materials** by category
- Add platform-wide Events

---

## 🏗️ Project Structure

```
Artistic_Avenue/
├── manage.py
├── requirements.txt
├── Procfile
├── build.sh
│
├── Artistic_Avenue/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── aa_app/                   # Main application
    ├── models.py             # Artist, User, Portal, Art, Order, Chat, Event, Video, Pdf, Query
    ├── views.py              # All views — user, artist, admin, shared
    ├── urls.py               # All URL routes
    ├── admin.py
    ├── migrations/           # Database migrations
    ├── static/
    │   ├── css/style.css
    │   └── images/           # Logo, favicon, backgrounds
    └── templates/
        ├── html/             # Public pages (home, gallery, shop, events)
        ├── user/             # User portal templates
        ├── artist/           # Artist portal templates
        ├── portal/           # Admin portal templates
        └── common/           # Shared partials
```

---

## 👥 User Roles & URLs

| Role | Key URLs |
|------|----------|
| Public | `/` `/gallery/` `/shop/` `/artists/` `/events/` `/tutorials/` |
| User | `/user_login/` `/user_register/` `/user_orders/` `/user_chats/` |
| Artist | `/artist_login/` `/artist_register/` `/artist_home/` `/upload/` `/add_event/` |
| Admin | `/portal/` `/portal_home/` `/portal_orders/` `/uploadmats/` |

---

## 🛒 Order Flow

```
User browses Shop → Clicks Buy → Billing page →
Uploads payment screenshot → Order created →
Artist sees order → Admin updates status → User tracks order
```

---

## 🗃️ Database Models

| Model | Description |
|-------|-------------|
| `Artist` | Artist profile — name, phone, email, category, photo |
| `User` | Buyer profile — name, phone, email, photo |
| `Portal` | Admin account |
| `Art` | Artwork — title, description, price, image, for-sale flag, sold flag |
| `Order` | Purchase record — user, art, payment proof, status |
| `Chat` | Messages between user and artist |
| `Event` | Exhibitions and workshops with date, venue, image |
| `Video` | Tutorial videos (YouTube links) with category |
| `Pdf` | Study material PDFs with category |
| `Query` | Contact form submissions |

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/tripathik9559/Artistic_Avenue.git
cd Artistic_Avenue

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## ☁️ Deployment (Render + Neon)

### Tech Used for Production
| Layer | Technology |
|-------|-----------|
| Hosting | [Render](https://render.com) |
| Database | [Neon](https://neon.tech) — PostgreSQL |
| Static Files | WhiteNoise |
| Server | Gunicorn |

### Environment Variables (Render)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `False` in production |
| `PYTHON_VERSION` | `3.11.0` |

### Build & Start Commands

```
Build:  chmod +x build.sh && ./build.sh
Start:  gunicorn Artistic_Avenue.wsgi:application
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2 |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (local) / PostgreSQL via Neon (production) |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Hosting | Render |

---

## 📸 Pages Overview

- **Home** — Featured artists and artworks
- **Gallery** — All artworks in one place
- **Shop** — Artworks available for purchase
- **Artists** — Browse all registered artists
- **Events** — Upcoming art exhibitions & workshops
- **Tutorials** — Video tutorials and PDF materials for artists
- **Chat** — Direct messaging between users and artists

---

## 📝 License
Built for educational purposes. © Artistic Avenue.
