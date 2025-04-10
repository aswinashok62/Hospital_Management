from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.sites import AdminSite
from .models import Category, Blogs, Comments

# Customizing Django Admin Site Titles
class MyAdminSite(AdminSite):
    site_header = "Hospital Admin Panel"
    site_title = "Hospital Admin"
    index_title = "Welcome to Hospital Admin Panel"

admin.site = MyAdminSite()

# Register models
admin.site.register(Category)
admin.site.register(Comments)

# Custom Admin Panel Styling
class CustomAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('doctors/css/admin_custom.css',)
        }

# Apply the custom styling to the Blogs model
admin.site.register(Blogs, CustomAdmin)
