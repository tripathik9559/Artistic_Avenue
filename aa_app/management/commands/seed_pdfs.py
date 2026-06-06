import os
from django.core.management.base import BaseCommand
from django.conf import settings
from aa_app.models import Pdf

# Map known filenames to friendly names, category, description
# Add your own PDFs here if you add more files later
PDF_METADATA = {
    'A-Beginners-Guide-to-Acrylics-Will-Kemp-Art-School.pdf': {
        'name': "Beginner's Guide to Acrylics",
        'category': 'Painting',
        'desc': 'A complete beginner-friendly guide to acrylic painting by Will Kemp Art School.',
    },
    'A-Beginners-Guide-to-Acrylics-Will-Kemp-Art-School_X2AkDIg.pdf': {
        'name': "Beginner's Guide to Acrylics (v2)",
        'category': 'Painting',
        'desc': 'A complete beginner-friendly guide to acrylic painting by Will Kemp Art School.',
    },
    'Handbook_of_Drawing_-_handbookofdrawing.pdf': {
        'name': 'Handbook of Drawing',
        'category': 'Drawing',
        'desc': 'A comprehensive handbook covering fundamental drawing techniques and principles.',
    },
}


class Command(BaseCommand):
    help = 'Seeds Pdf records from existing files in media/PDFs/ folder'

    def handle(self, *args, **kwargs):
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'PDFs')

        if not os.path.exists(pdf_dir):
            self.stdout.write(self.style.WARNING(f'PDFs folder not found at: {pdf_dir}'))
            return

        files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

        if not files:
            self.stdout.write(self.style.WARNING('No PDF files found in media/PDFs/'))
            return

        created_count = 0
        skipped_count = 0

        for filename in files:
            relative_path = f'PDFs/{filename}'

            # Skip if record already exists
            if Pdf.objects.filter(link=relative_path).exists():
                self.stdout.write(f'  Skipping (already exists): {filename}')
                skipped_count += 1
                continue

            # Use metadata if defined, else auto-generate
            meta = PDF_METADATA.get(filename, {})
            name = meta.get('name', filename.replace('_', ' ').replace('-', ' ').replace('.pdf', '').title()[:32])
            category = meta.get('category', 'General')
            desc = meta.get('desc', '')

            Pdf.objects.create(
                name=name[:32],
                category=category,
                desc=desc,
                link=relative_path,
            )
            self.stdout.write(self.style.SUCCESS(f'  Created record: {name}'))
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone! Created: {created_count}, Skipped: {skipped_count}'
            )
        )