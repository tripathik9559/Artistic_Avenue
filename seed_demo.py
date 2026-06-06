"""
Seed script — creates demo accounts + demo data.
Run:  python manage.py shell -c "exec(open('seed_demo.py').read())"
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Artistic_Avenue.settings')
django.setup()

from aa_app.models import Artist, User, Portal, Art, Order

# ── Demo Portal / Admin ───────────────────────────────────────────────────────
if not Portal.objects.filter(pid='admin001').exists():
    Portal.objects.create(pid='admin001', password='admin123', name='Admin')
    print("✓ Admin created  →  ID: admin001 | PW: admin123")
else:
    print("  Admin already exists")

if not Portal.objects.filter(pid='admin123').exists():
    Portal.objects.create(pid='admin123', password='Admin@2024', name='Admin2')

# ── Demo Artist ───────────────────────────────────────────────────────────────
demo_artist, created = Artist.objects.get_or_create(
    phone='9999900001',
    defaults=dict(
        name='Demo Artist',
        password='demo@artist',
        email='demo.artist@artisticavenue.com',
        category='Abstract',
        bio='A passionate abstract artist exploring colour, form and emotion through canvas.',
        pic='demo_artists/su.jpeg',
    )
)
if created:
    print("✓ Demo Artist created  →  9999900001 / demo@artist")
else:
    print("  Demo Artist already exists")

# ── Demo User ─────────────────────────────────────────────────────────────────
demo_user, created = User.objects.get_or_create(
    phone='9999900002',
    defaults=dict(
        name='Demo User',
        password='demo@user',
        email='demo.user@artisticavenue.com',
        pic='',
    )
)
if created:
    print("✓ Demo User created  →  9999900002 / demo@user")
else:
    print("  Demo User already exists")

# ── Demo Artworks — DELETE old ones and recreate with correct static paths ────
DEMO_NAMES = ['Crimson Dreams','Ocean Whispers','Urban Rhythm','Silent Forest','Golden Hour','Mind Mirror']

# Delete existing demo artworks (they have wrong Arts/ paths)
deleted = Art.objects.filter(name__in=DEMO_NAMES, artist=demo_artist).delete()
print(f"  Deleted {deleted[0]} old demo artworks")

demo_arts_data = [
    dict(name='Crimson Dreams',  art_type='Abstract',      price='12500', forsale=True,  sold=False, desc='A bold abstract piece in deep crimson and gold.',    pic='demo_arts/abs.avif'),
    dict(name='Ocean Whispers',  art_type='Surrealism',    price='18000', forsale=True,  sold=False, desc='Surrealist seascape in soft blues and greens.',       pic='demo_arts/b.avif'),
    dict(name='Urban Rhythm',    art_type='Abstract',      price='9500',  forsale=True,  sold=False, desc='Chaos and beauty of urban landscapes in paint.',      pic='demo_arts/abs.avif'),
    dict(name='Silent Forest',   art_type='Landscape',     price='22000', forsale=True,  sold=False, desc='Quiet woodland scene with light and shadow.',         pic='demo_arts/z.jpg'),
    dict(name='Golden Hour',     art_type='Impressionism', price='15000', forsale=True,  sold=False, desc='Warm impressionist sunset with rich texture.',        pic='demo_arts/ala.jpg'),
    dict(name='Mind Mirror',     art_type='Surrealism',    price='27500', forsale=False, sold=False, desc='Personal surrealist work — not for sale.',           pic='demo_arts/2921.jpg'),
]
for ad in demo_arts_data:
    Art.objects.create(artist=demo_artist, **ad)
print(f"✓ {len(demo_arts_data)} demo artworks created with correct static paths")

print("\nDone! Credentials:")
print("  Artist → 9999900001 / demo@artist")
print("  User   → 9999900002 / demo@user")
print("  Admin  → admin001 / admin123")
