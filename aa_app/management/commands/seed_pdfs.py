import os
from django.core.management.base import BaseCommand
from django.conf import settings
from aa_app.models import Pdf, Video, Portal

PDF_METADATA = {
    'A-Beginners-Guide-to-Acrylics-Will-Kemp-Art-School.pdf': {
        'name': "Beginner's Guide to Acrylics",
        'category': 'Painting',
        'desc': 'A complete beginner-friendly guide to acrylic painting by Will Kemp Art School.',
    },
    'A-Beginners-Guide-to-Acrylics-Will-Kemp-Art-School_X2AkDIg.pdf': {
        'name': "Beginner's Guide to Acrylics",
        'category': 'Painting',
        'desc': 'A complete beginner-friendly guide to acrylic painting by Will Kemp Art School.',
    },
    'Handbook_of_Drawing_-_handbookofdrawing.pdf': {
        'name': 'Handbook of Drawing',
        'category': 'Drawing',
        'desc': 'A comprehensive handbook covering fundamental drawing techniques and principles.',
    },
}

VIDEO_DATA = [
    {'name': 'Portrait Tutorial', 'link': 'GH3_NUbRpCY', 'category': 'Portrait',       'desc': ''},
    {'name': 'Demo',              'link': 'G6aUE2OQWZs', 'category': 'General',         'desc': ''},
    {'name': 'Pencil Drawing',    'link': 'W9pTY2AEUp4', 'category': 'Pencil Drawing',  'desc': ''},
    {'name': 'Canvas Painting',   'link': '7whhcFfz51Q', 'category': 'Water Painting',  'desc': ''},
    {'name': 'Water Painting',    'link': '5dXFqVnkCdA', 'category': 'Painting',        'desc': ''},
]

PORTAL_DATA = [
    {'name': 'Admin', 'pid': '1',        'password': '1'},
    {'name': 'Admin', 'pid': 'admin123', 'password': 'mypassword'},
]


class Command(BaseCommand):
    help = 'Seeds Portal, Video, and Pdf records'

    def handle(self, *args, **kwargs):

        # ── Portal ──────────────────────────────────────────────
        self.stdout.write('\n--- Seeding Portal ---')
        for p in PORTAL_DATA:
            if Portal.objects.filter(pid=p['pid']).exists():
                self.stdout.write(f"  Skipping (exists): {p['pid']}")
            else:
                Portal.objects.create(**p)
                self.stdout.write(self.style.SUCCESS(f"  Created portal: {p['pid']}"))

        # ── Videos ──────────────────────────────────────────────
        self.stdout.write('\n--- Seeding Videos ---')
        for v in VIDEO_DATA:
            if Video.objects.filter(link=v['link']).exists():
                self.stdout.write(f"  Skipping (exists): {v['name']}")
            else:
                Video.objects.create(**v)
                self.stdout.write(self.style.SUCCESS(f"  Created video: {v['name']}"))

        # ── PDFs ────────────────────────────────────────────────
        self.stdout.write('\n--- Seeding PDFs ---')
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'PDFs')
        if os.path.exists(pdf_dir):
            for filename in os.listdir(pdf_dir):
                if not filename.endswith('.pdf'):
                    continue
                relative_path = f'PDFs/{filename}'
                if Pdf.objects.filter(link=relative_path).exists():
                    self.stdout.write(f'  Skipping (exists): {filename}')
                    continue
                meta = PDF_METADATA.get(filename, {})
                name = meta.get('name', filename.replace('_', ' ').replace('-', ' ').replace('.pdf', '').title()[:32])
                Pdf.objects.create(
                    name=name[:32],
                    category=meta.get('category', 'General'),
                    desc=meta.get('desc', ''),
                    link=relative_path,
                )
                self.stdout.write(self.style.SUCCESS(f'  Created PDF: {name}'))

        self.stdout.write(self.style.SUCCESS('\nAll done!'))