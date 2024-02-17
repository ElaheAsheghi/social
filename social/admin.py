from django.contrib import admin
from .models import User, Post, AdminMessage
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail


# Actions


#Action For Deactive Post
def make_deactivation(modeladmin, request, queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request, f'{result} posts were banned.')

make_deactivation.short_description = "Deactive"



#Action For Sending Post ActiveStatus To User
def send_active(modeladmin, request, queryset):
    subject = "post status"
    for obj in queryset:
        if obj.active:
            status = 'active'
        else:
            status = 'deactive'
        message = f"status:\t{status}\npost:\n{obj.description}"
        result = send_mail(subject, message, 'socialwebproject2024@gmail.com', [obj.author.email], fail_silently=False)
    modeladmin.message_user(request, f'{result} emails have send.')


# Register your models here.


#User
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets= UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields':('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )


#Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'description']
    ordering = ['created']
    list_filter = ['created', 'author', 'description']
    search_fields = ['description']
    raw_id_fields = ['author']
    date_hierarchy = 'created'
    # prepopulated_fields = {"slug":['description']}
    list_display_links = ['description']
    # inlines = [ImageInline, CommentInline]
    actions = [make_deactivation, send_active]


#AdminMessage
@admin.register(AdminMessage)
class AdminMessage(admin.ModelAdmin):
    list_display = ['subject', 'user', 'date']
    search_fields = ['subject', 'message']