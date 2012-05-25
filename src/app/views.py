from __future__ import division

import json
import math
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import generic as views

from .forms import PlanningFeedForm
from db.models import PlanningFeedModel


class PlanningFeedView (views.View):
    def instance_to_dict(self, feed):
        return {
            'publisher': feed.publisher,
            'source_url': feed.source_url,
            'description': feed.description
        }

    def get_feeds_data(self):
        page = int(self.request.GET.get('page', 1))
        perpage = 20  # The number of feeds per page
        begin = ((page - 1) * perpage)  # The index of the first feed on page
        end = (page * perpage)  # The index of the first feed on next page

        feeds = PlanningFeedModel.objects.all()[begin:end]
        results = [self.instance_to_dict(feed) for feed in feeds]
        num_feeds = PlanningFeedModel.objects.all().count()

        data = {
            'results': results,
            'count': num_feeds,
            'page': page
        }

        # Set up pagination.  Only include prev/next link if you're not on the
        # first/last page.
        num_pages = math.ceil(num_feeds / perpage)

        base_uri = self.request.build_absolute_uri(self.request.path)
        if page > 1:
            data['prev'] = base_uri + '?page=' + str(page - 1)
        if num_feeds > (page * perpage):
            data['next'] = base_uri + '?page=' + str(page + 1)

        return data

    def get(self, request):
        # GET: Get a list of planning feeds, JSON formatted.
        feeds_data = self.get_feeds_data()
        return self.render_GET_response(feeds_data)

    def post(self, request):
        # POST: Add a feed to the list, if it doesn't already exist.
        feed_data = request.POST or json.loads(request.body.encode(request.encoding))

        # Check the data.
        form = PlanningFeedForm(feed_data)
        if form.is_valid():
            try:
                instance = PlanningFeedModel.objects.get(source_url=feed_data['source_url'])
                for attr, value in feed_data.items():
                    setattr(instance, attr, value)
                instance.save()
                data = self.instance_to_dict(instance)
                return self.do_success_response(data, 200)

            except PlanningFeedModel.DoesNotExist:
                data = self.instance_to_dict(form.save())
                return self.do_success_response(data, 201)

        else:
            return self.do_error_response(form, 400)


class HomeView (PlanningFeedView):
    # GET: Get a form for adding a new feed.
    def render_GET_response(self, data):
        if self.request.is_ajax():
            return HttpResponse(json.dumps(data))
        else:
            return self.render_form_response(PlanningFeedForm(), data)

    def do_success_response(self, data, status_code):
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps({'data': data}),
                status=status_code,
                mimetype='application/json')
        else:
            messages.success(
                self.request, 'Feed at {0} successfully {1}'.format(
                    data['source_url'],
                    'created' if status_code == 201 else 'updated'))
            return HttpResponseRedirect(reverse('home'))

    def do_error_response(self, form, status_code):
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps({'errors': form.errors}),
                status=status_code,
                mimetype='application/json')
        else:
            feeds_data = self.get_feeds_data()
            return self.render_form_response(form, feeds_data)

    def render_form_response(self, form, context=None):
        context = context or {}
        context['form'] = form
        return render_to_response('index.html', context, context_instance=RequestContext(self.request))


class PlanningFeedApiView (PlanningFeedView):
    def render_GET_response(self, data):
        return HttpResponse(json.dumps(data))

    def do_success_response(self, data, status_code):
        return HttpResponse(
            json.dumps({'data': data}),
            status=status_code,
            mimetype='application/json')

    def do_error_response(self, form, status_code):
        return HttpResponse(
            json.dumps({'errors': form.errors}),
            status=status_code,
            mimetype='application/json')
