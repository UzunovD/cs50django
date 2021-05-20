import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown

from encyclopedia import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def get_entry(request, title: str):
    content = None
    if title not in util.list_entries():
        content = f'ERROR! Requested page {title} not found'
    return util.forwarding(request, title, content)


def search(request):
    if 'query' in request.GET:
        query = request.GET['query']
        if query in util.list_entries():
            return util.forwarding(request, query)
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": [entry for entry in util.list_entries() if entry.lower().count(query.lower())],
                "query": query
            })


def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        if 'edit' not in request.META['HTTP_REFERER'] and title in util.list_entries():
            return render(request, 'encyclopedia/error.html', {
                'title': title,
            })
        util.save_form_to_entry(request)
        return HttpResponseRedirect(title)
    return render(request, "encyclopedia/create.html", {
        "form": util.CreateEntryForm(),
    })


def edit(request, title):
    content = util.get_entry(title)
    data = {'title': title,
            'content': content,
            }
    return render(request, "encyclopedia/create.html", {
        "form": util.CreateEntryForm(data),
    })


def random_page(request):
    title = random.choice(util.list_entries())
    return get_entry(request, title)
