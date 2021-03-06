from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .models import Document
from .forms import DocumentForm
# Create your views here.


class IndexView(FormView):
    template_name = 'web/index.html'
    form_class = DocumentForm
    success_url = 'web:tenso'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(self.get_success_url(),
                                            kwargs={'pk': form.instance.pk}))

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        tensos = Document.objects.filter(share=True).order_by('-created')[:15]
        context['tensos'] = tensos
        return context


class TensoView(TemplateView):
    template_name = 'web/result.html'
    context_object_name = 'tenso'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        url = self.request.build_absolute_uri(reverse('web:tenso', args=(pk, )))
        context = super(TensoView, self).get_context_data(**kwargs)
        try:
            tenso = Document.objects.get(pk=pk)
            context['tenso'] = tenso
            context['url'] = url
        except Document.DoesNotExist:
            raise Http404
        return context

class PrivacyView(TemplateView):
    template_name = 'web/privacy.html'
