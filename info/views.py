from django.shortcuts import render
from django.views.generic.list import ListView

from .models import InfoPost

class InfoPostListView(ListView):
    model = InfoPost
    template_name = 'info/infoPost.html'
    #Expand base model to include base and user
    def get_context_data(self, **kwargs):
        context = super(InfoPostListView, self).get_context_data(**kwargs)
        context['base'] = 'base.html'
        context['user'] = self.request.user
        return context

