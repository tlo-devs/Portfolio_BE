from django.contrib import admin


class SiteAdmin(admin.AdminSite):
    site_header = "DomePortfolio Administration"
    index_title = "DomePortfolio Administration"
    site_title = "Administration"
