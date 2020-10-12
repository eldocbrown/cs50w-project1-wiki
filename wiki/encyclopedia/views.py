from django.shortcuts import render

from . import util

# Remove
from django.http import HttpResponse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    #Try to get entry
    content = util.get_entry(entry)
    if content is not None:
        title = entry
    else:
        title = "Article not found"
        content = f"Wiki does not have an article with this exact name. Please search for {entry} in Wiki to check for alternative titles or spellings."

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })
