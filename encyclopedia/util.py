import re

from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown


class CreateEntryForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(widget=forms.Textarea)


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                       for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def save_form_to_entry(request):
    """
    Validates user form, extract title, content and
    call save_entry(title, content) for save entry.
    """
    form = CreateEntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        save_entry(title, content)
        return


def forwarding(request, title, content=None):
    """
    Renders entry page with given title and content.
    If content not given - retrieves content by title.
    """
    if not content:
        markdowner = Markdown()
        content = markdowner.convert(get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": content,
    })
