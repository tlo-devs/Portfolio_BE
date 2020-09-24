from django.db import migrations
from ..models import AboutSection, AboutParagraph, VitaParagraph, HomeSection
from typing import Tuple


def save_paragraph(paragraphs: Tuple, model, parent):
    for i, paragraph in enumerate(paragraphs):
        paragraph: dict
        paragraph["parent"] = parent
        paragraph["order_field"] = i + 1
        item = model(**paragraph)
        item.save()


def add_default_about(apps, schema_editor):
    about = AboutSection.objects.create(
        img=None,
    )
    about.save()

    # AboutParagraphs
    a_paragraphs = (
        {"title": "Hauptberuf", "text": "Videoeditor / Fotograf"},
        {
            "title": "Zahlreiche Erfahrungen als",
            "text": "Kameramann, Lichtassistent, Cutter"
        }
    )
    save_paragraph(a_paragraphs, AboutParagraph, about)

    # VitaParagraphs
    v_paragraphs = (
        {"year": 2018, "text": "Ausbildung als Mediengestalter Bild und Ton"},
        {"year": 2018, "text": "Studium Maschinenbau"},
        {"year": 2017, "text": "Abitur (Brandenburg)"},
        {"year": 2014, "text": "FSJ als Krankenpfleger"},
    )
    save_paragraph(v_paragraphs, VitaParagraph, about)


def add_default_home(*args):
    home = HomeSection.objects.create()
    home.save()


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_about),
        migrations.RunPython(add_default_home),
    ]
