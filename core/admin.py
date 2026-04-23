from django.contrib import admin
from .models import Director, Service, Project, ClientAccount, ContactMessage, CompanyInfo

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_range', 'order']
    list_editable = ['order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'is_featured', 'order']
    list_editable = ['order', 'is_featured']

@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'phone', 'created_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_editable = ['is_read']

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one company info instance
        if self.model.objects.exists():
            return False
        return True