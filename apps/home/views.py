# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import render
from django.views import View
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.table_view.forms import HILsForm


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class HilManager(View):

    @staticmethod
    def get(request):
        form = HILsForm()
        return render(request, 'home/p_forms.html', {
            'form': form,
            'form_title': str(HILsForm())
        })

    @staticmethod
    def post(request):
        form = HILsForm(request.POST)
        note = str()
        if form.is_valid():
            form.save()
            note = 'success'
        else:
            note = 'Form is not valid'
        return render(request, 'home/p_forms.html', {
            'form': form,
            'form_title': str(HILsForm()),
            'note': note
        })
