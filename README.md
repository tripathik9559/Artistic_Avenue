# 🎨 Artistic Avenue

> A full-stack Django artist marketplace where artists sell original artworks and users discover and purchase unique pieces.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat-square)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square)

---

## ✨ Features

### For Users
- Browse the full artwork gallery with search & filters
- Shop available artworks filtered by style and price
- Purchase with QR-based payment + screenshot upload
- Track order status (Pending → Confirmed → Delivered)
- Chat directly with artists

### For Artists
- Artist dashboard with stats (artworks, sold count, pending orders)
- Upload artwork with category, price, description, and photo
- Manage sales orders and update status
- View chat messages from buyers
- Host and manage art events

### For Admin
- Dashboard with platform-wide statistics
- Manage all orders and update statuses
- View all users, artists, artworks, and queries
- Upload tutorial videos (YouTube) and PDF resources

### Platform-wide
- Search by artwork name, artist name, and style
- Category and price-range filters on the shop
- Responsive design (mobile-first)
- Artist profile pages with bio, gallery, and artwork stats
- Events / exhibitions listing with images
- Contact form for queries

---

## 🔑 Demo Accounts

> Use these to explore the platform without registering.

| Role   | Phone        | Password     | Notes                        |
|--------|--------------|--------------|------------------------------|
| User   | 9999900002   | demo@user    | Shown on User Login page     |
| Artist | 9999900001   | demo@artist  | Shown on Artist Login page   |
| Admin  | ID: admin123 | Admin@2024   | Not publicly displayed       |

---

## 🖼️ Project Structure

```
Artistic_Avenue/
├── Artistic_Avenue/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── aa_app/                 # Main app
│   ├── models.py           # Artist, User, Portal, Art, Order, Event, Chat…
│   ├── views.py            # All views with session auth
│   ├── urls.py             # URL routing
│   ├── templates/
│   │   ├── html/           # Public pages (home, gallery, shop, artists…)
│   │   ├── artist/         # Artist dashboard templates
│   │   ├── user/           # User dashboard templates
│   │   ├── portal/         # Admin templates
│   │   └── common/         # Shared header, footer, CSS
│   └── static/
│       ├── css/style.css
│       └── images/
├── media/                  # Uploaded files (gitignored)
├── seed_demo.py            # Demo data seeder
├── build.sh                # Render deployment script
├── requirements.txt
└── .env.example
```

---

## 🚀 Local Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Artistic_Avenue.git
cd Artistic_Avenue
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env — set SECRET_KEY, DEBUG=True for local
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Seed demo data
```bash
python seed_demo.py
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## ☁️ Deployment on Render

### Step 1 — Push to GitHub
```bash
git add .
git commit -m "Initial deploy"
git push origin main
```

### Step 2 — Create a Web Service on Render
1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repository
3. Fill in these settings:

| Field            | Value                        |
|------------------|------------------------------|
| Environment      | Python 3                     |
| Build Command    | `./build.sh`                 |
| Start Command    | `gunicorn Artistic_Avenue.wsgi:application` |
| Instance Type    | Free                         |

### Step 3 — Set Environment Variables
In Render dashboard → **Environment**:

| Key           | Value                        |
|---------------|------------------------------|
| SECRET_KEY    | (generate a random 50-char string) |
| DEBUG         | False                        |
| ALLOWED_HOSTS | your-app.onrender.com        |
| PYTHON_VERSION| 3.11.0                       |

### Step 4 — Deploy
Click **Deploy** — Render will run `build.sh` which:
1. Installs packages
2. Collects static files
3. Runs migrations
4. Seeds demo accounts

> **Note on media files:** Render's free tier has an ephemeral filesystem — uploaded images will reset on redeploy. For production, integrate [Cloudinary](https://cloudinary.com/) or [AWS S3](https://aws.amazon.com/s3/) for persistent media storage.

---

## 🗄️ Migration Commands

```bash
# Apply all migrations
python manage.py migrate

# If you change models (add new field, etc.)
python manage.py makemigrations
python manage.py migrate

# Re-seed demo data
python seed_demo.py
```

---

## ✅ Testing Checklist

- [ ] Homepage loads with carousel, stats, artist strip, artwork strip, and map
- [ ] User login works with demo credentials (Phone: 9999900002, PW: demo@user)
- [ ] Artist login works with demo credentials (Phone: 9999900001, PW: demo@artist)
- [ ] Demo fill buttons on login pages autofill and submit
- [ ] Gallery page search filters by name/artist/style
- [ ] Shop page search + category + price range filters work
- [ ] Artists page search + category filter works
- [ ] Artist profile page (click "View Art") shows bio, stats, gallery
- [ ] Shop "Buy Now" requires login, shows checkout with QR
- [ ] Order placed → status "Pending" in user orders
- [ ] Admin login (ID: admin123, PW: Admin@2024) works at /portal/
- [ ] Admin dashboard shows stats counts
- [ ] Admin can update order status (Pending/Confirmed/Delivered)
- [ ] Artist dashboard shows artwork count, sold count, pending orders
- [ ] Chat between user and artist works
- [ ] Contact form submits and appears in admin queries
- [ ] Events page loads correctly
- [ ] Static files load (logo, background, images)
- [ ] Mobile responsive navbar (hamburger menu works)

---

## 🛠️ Tech Stack

| Layer      | Technology                     |
|------------|-------------------------------|
| Backend    | Django 5.0 (Python)           |
| Frontend   | Bootstrap 5.3 + custom CSS    |
| Fonts      | Google Fonts (Pacifico, Poppins, Oswald) |
| Icons      | Font Awesome 5                |
| Database   | SQLite (dev) / PostgreSQL (prod) |
| Static     | WhiteNoise                    |
| Deployment | Render                        |

---

## 👨‍💻 Developed By

**Kartikey Kumar Tripathi** — Backend Developer  
BBDNIIT

---

*Artistic Avenue — Where Art Meets Commerce*
