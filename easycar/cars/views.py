from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView

from cars.models import Make, Model


class ListMakeView(ListView):
    model = Make
    template_name = 'make_list.html'


class CreateMakeView(CreateView):
    model = Make
    template_name = 'make_add.html'
    fields = ('name',)

    def get_success_url(self):
        return reverse('makes-list')


class ListModelView(ListView):
    template_name = 'make_list.html'

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        
        if make_id:
            return Model.objects.filter(make__id=make_id).all()
        else:
            return super(ListModelView, self).get_queryset()


list_make_view = ListMakeView.as_view()
create_make_view = CreateMakeView.as_view()
list_model_view = ListModelView.as_view()
