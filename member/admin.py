from django.contrib import admin
from .models import *

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "member_id",
        "username",
        "role",
        "community",
        "gender",
        "dob",
        "age",
        "member_id",
        "profile_picture",
        "citizen_copy",
    ]

admin.site.register(Member, MemberAdmin)

class CommunityAdmin(admin.ModelAdmin):
    list_display = [
        "community_name",
        # "get_community_heads",
    ]

    # def get_community_heads(self, obj):
    #     return ", ".join([user.get_full_name() for user in obj.community_head.all()])
    
    # get_community_heads.short_description = "Community Heads"

admin.site.register(Community, CommunityAdmin)
