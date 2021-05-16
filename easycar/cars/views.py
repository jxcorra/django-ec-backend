# Create your views here.
from django.db.models import Count
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from cars.models import Make, Model, Car


class ListMakeView(ListView):
    model = Make
    template_name = 'make_list.html'

    def get_queryset(self):
        order_criteria = self.request.GET.get('order')

        if not order_criteria:
            return super(ListMakeView, self).get_queryset()

        return self.model.objects.annotate(models_count=Count('models')).order_by('models_count')


class CreateMakeView(CreateView):
    model = Make
    template_name = 'make_add.html'
    fields = ('name',)

    def get_success_url(self):
        return reverse('makes-list')


class ListModelView(ListView):
    template_name = 'model_list.html'

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')

        return Model.objects.filter(make__id=make_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListModelView, self).get_context_data(object_list=object_list, kwargs=kwargs)
        context['make_id'] = self.kwargs.get('make_id')

        return context


class ListCarView(ListView):
    template_name = 'car_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListCarView, self).get_context_data(object_list=object_list, **kwargs)
        context['make_id'] = self.kwargs.get('make_id')
        context['model_id'] = self.kwargs.get('model_id')

        return context

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')

        return Car.objects.filter(model__id=model_id)


class CarDetailsView(UpdateView):
    model = Car
    fields = ('owner', 'model', 'vin', 'year', 'image',)
    template_name = 'car_form.html'

    def get_object(self, queryset=None):
        return Car.objects.get(pk=self.kwargs.get('car_id'))

    def get_success_url(self):
        return reverse('car-details', kwargs={'car_id': self.kwargs.get('car_id')})


list_make_view = ListMakeView.as_view()
create_make_view = CreateMakeView.as_view()
list_model_view = ListModelView.as_view()
list_car_view = ListCarView.as_view()
car_details_view = CarDetailsView.as_view()
