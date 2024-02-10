from django.contrib import admin
from .models import User, Post
from django.contrib.auth.admin import UserAdmin


# Actions


#Action For Deactive Post
def make_deactivation(modeladmin, request, queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request, f'{result} posts were banned.')

make_deactivation.short_description = "Deactive"



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
    actions = [make_deactivation]