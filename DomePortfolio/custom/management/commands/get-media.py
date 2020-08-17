from django.core.management import BaseCommand
from django.conf import settings
from urllib import request
from pathlib import Path
import zipfile
from ._utils import write_file, indent
import os


class Command(BaseCommand):
    help = "Automatically downloads static files for django-crispy-forms"

    def handle(self, *args, **options):
        template_pack = getattr(
            settings,
            "CRISPY_TEMPLATE_PACK",
            "bootstrap4"
        )

        # Download the files to the media directory
        download_files = {
            "bootstrap4": "https://github.com/twbs/bootstrap/releases/download/v4.5.0/bootstrap-4.5.0-dist.zip",
            "bootstrap3": "https://github.com/twbs/bootstrap/releases/download/v3.4.0/bootstrap-3.4.0-dist.zip",
            "bootstrap": "https://getbootstrap.com/2.3.2/assets/bootstrap.zip",
        }
        try:
            download = download_files[template_pack]
        except KeyError:
            self.stdout.write(
                "The specified template pack is not supported by the auto downloader."
            )
        else:
            MEDIA = Path(settings.BASE_DIR) / "media"
            download_path = MEDIA / f"{template_pack}.zip"
            request.urlretrieve(
                download, download_path
            )
            with zipfile.ZipFile(download_path, "r") as zipf:
                zipf.extractall(MEDIA)
            download_path.unlink()
            bootstrap_dir = MEDIA / [fn for fn in os.listdir(MEDIA) if "bootstrap" in fn][0]
            if bootstrap_dir.is_dir():
                bootstrap_dir.rename(MEDIA / template_pack)

            # Generate templates safe for use with crispy-forms
            # 
            stylesheets = (
                       "<link rel='stylesheet' href='{% static " +
                       f"'{template_pack}/css/Bootstrap.css'" +
                       "%}'>",
                       "<script src='{% static " +
                       "'jquery/jquery.min.js'" +
                       "%}'></script>",
                       "<script src='{% static " +
                       f"'{template_pack}/js/Bootstrap.js'" +
                       "%}'></script>",
            )

            # Generate base.html file with the correct files included
            write_file(
                Path(settings.BASE_DIR) / "templates",
                "base.html",
                (
                    "<!doctype html>",
                    "<html lang='en'>",
                    "<head>",
                    indent(1, "<meta charset='UTF-8'>"),
                    indent(1, "<meta name='viewport' content='width=device-width, user-scalable=no, "
                              "initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0'>"),
                    indent(1, "<meta http-equiv='X-UA-Compatible' content='ie=edge'>"),
                    indent(1, "<title>{% block title %}{% endblock title %}</title>"),
                    indent(1, "{% load static %}"),
                    *[indent(1, line) for line in stylesheets],
                    indent(1, "{% block extrahead %}{% endblock extrahead %}"),
                    "</head>",
                    "<body>",
                    "{% block content %}",
                    "{% endblock content %}",
                    "</body>",
                    "</html>"
                )
            )

            # Generate standalone styles.html file for use in admin
            write_file(
                Path(settings.BASE_DIR) / "templates" / "crispy",
                "styles.html",
                (
                    "{% load static %}",
                    *stylesheets,
                )
            )

            # 
