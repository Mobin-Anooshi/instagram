from django.contrib import admin
from .models import UserMessage, SaveMessage,Post,Vote,Relations,UserRequest
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','created',)
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug':('caption',)}
    
    
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display=('user','post')
    raw_id_fields = ('post','user')
    


class SaveMessageInline(admin.TabularInline):
    model = SaveMessage
    raw_id_fields = ('post',)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    inlines = (SaveMessageInline,)

@admin.register(Relations)
class RelationsAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user')
    
@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user')