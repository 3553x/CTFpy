from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import TeamMember, Team
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {'base':'base.html', 'user':request.user}
    currentUser = request.user
    team = Team.objects.filter(teammember__member=currentUser)
    if (team.exists()):
        otherTeamMembers = User.objects.filter(teammember__team=team.get())
        context['TeamMembers'] = otherTeamMembers
    return render(request, 'team/index.html', context)

