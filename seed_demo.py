"""
Seed script — creates demo accounts + demo data.
Run:  python manage.py shell < seed_demo.py
  or: python seed_demo.py   (from project root with DJANGO_SETTINGS_MODULE set)
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Artistic_Avenue.settings')
django.setup()

from aa_app.models import Artist, User, Portal, Art, Order, Event, Video, Pdf

# ── Demo Portal / Admin ───────────────────────────────────────────────────────
if not Portal.objects.filter(pid='admin123').exists():
    Portal.objects.create(pid='admin123', password='Admin@2024', name='Admin')
    print("✓ Admin account created  →  ID: admin123 | PW: Admin@2024")
else:
    print("  Admin already exists")

# ── Demo Artist Account ───────────────────────────────────────────────────────
demo_artist, created = Artist.objects.get_or_create(
    phone='9999900001',
    defaults=dict(
        name='Demo Artist',
        password='demo@artist',
        email='demo.artist@artisticavenue.com',
        category='Abstract',
        bio='A passionate abstract artist exploring colour, form and emotion through canvas. Available for commissions.',
        pic='Artists/su.jpeg',
    )
)
if created:
    print("✓ Demo Artist created     →  Phone: 9999900001 | PW: demo@artist")
else:
    print("  Demo Artist already exists")

# ── Demo User Account ─────────────────────────────────────────────────────────
demo_user, created = User.objects.get_or_create(
    phone='9999900002',
    defaults=dict(
        name='Demo User',
        password='demo@user',
        email='demo.user@artisticavenue.com',
        pic='Users/pexels-moose-photos-170195-1036623.jpg',
    )
)
if created:
    print("✓ Demo User created       →  Phone: 9999900002 | PW: demo@user")
else:
    print("  Demo User already exists")

# ── Demo Artworks for Demo Artist ────────────────────────────────────────────
demo_arts_data = [
    dict(name='Crimson Dreams', art_type='Abstract',    price='12500', forsale=True,  sold=False, desc='A bold abstract piece in deep crimson and gold, exploring dreams and ambition.',          pic='Arts/abs.avif'),
    dict(name='Ocean Whispers', art_type='Surrealism',  price='18000', forsale=True,  sold=False, desc='Surrealist seascape merging reality and imagination in soft blues and greens.',           pic='Arts/b.avif'),
    dict(name='Urban Rhythm',   art_type='Abstract',    price='9500',  forsale=True,  sold=False, desc='Inspired by city life — the chaos and beauty of urban landscapes captured in paint.',    pic='Arts/abs.avif'),
    dict(name='Silent Forest',  art_type='Landscape',   price='22000', forsale=True,  sold=False, desc='Quiet woodland scene painted with meticulous attention to light and shadow.',            pic='Arts/z.jpg'),
    dict(name='Golden Hour',    art_type='Impressionism',price='15000',forsale=True,  sold=False, desc='Warm impressionist sunset study, rich with texture and atmospheric light.',              pic='Arts/ala.jpg'),
    dict(name='Mind Mirror',    art_type='Surrealism',  price='27500', forsale=False, sold=False, desc='A deeply personal surrealist work — not for sale, part of the permanent collection.',   pic='Arts/2921.jpg'),
]
created_count = 0
for ad in demo_arts_data:
    if not Art.objects.filter(name=ad['name'], artist=demo_artist).exists():
        Art.objects.create(artist=demo_artist, **ad)
        created_count += 1
print(f"✓ {created_count} demo artworks created for Demo Artist")

# ── Demo Order ────────────────────────────────────────────────────────────────
# pick an already-sold art for the demo order so shop is clean
sold_art = Art.objects.filter(sold=True).first()
if sold_art and not Order.objects.filter(user=demo_user, art=sold_art).exists():
    Order.objects.create(user=demo_user, art=sold_art, payment='', status='Confirmed')
    print("✓ Demo order created")

print("\nAll done! Demo credentials:")
print("  Artist  →  Phone: 9999900001  Password: demo@artist")
print("  User    →  Phone: 9999900002  Password: demo@user")
print("  Admin   →  ID: admin123        Password: Admin@2024  (not shown on login page)")
