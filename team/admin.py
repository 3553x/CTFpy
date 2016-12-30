from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import TeamMember, Team

#create part to assign teams
class TeamInLine(admin.StackedInline):
    model = TeamMember
    can_delete = False

#add teams to user manager
class UserAdmin(BaseUserAdmin):
    inlines = (TeamInLine, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Team)
