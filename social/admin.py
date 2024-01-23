from django.contrib import admin
from .models import User, Post
from django.contrib.auth.admin import UserAdmin

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