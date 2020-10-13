from django.shortcuts import render
from django.shortcuts import redirect
from . import util
import random as rdm

def index(request):
    # If it is a POST request, assume its a Search operation
    if request.method == "POST":
        q = request.POST["q"]
        entries = []
        page_header = "No articles found"
        if len(q) > 0:
            entries = util.list_entries()
            # Entries found in directory
            if len(entries) > 0:
                # Redirect to unique coincidence
                if q in entries:
                    return redirect('encyclopedia:entry', entry=q)
                # Search for substrings
                else:
                    search = search_entries(entries, q)
                    # Entries with substrings found
                    if len(search) > 0:
                        page_header = "Search Result"
                        return render_index(request, page_header, search)
                    # No articles found
                    else:
                        page_header = "No articles found"
                        return render_index(request, page_header, [])
            # No entries found in directory
            else:
                page_header = "No articles found in the article repository"
                return render_index(request, page_header, entries)
        # Blank parameter on input
        else:
            return render_index(request, page_header, entries)

    # If it is a GET request, render All Pages
    else:
        return render_index(request, "All Pages", util.list_entries())

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

def random(request):
    entries = util.list_entries()
    # Entries found in directory
    if len(entries) > 0:
        # Select random entry from Entries
        entry = rdm.choice(entries)
        return redirect('encyclopedia:entry', entry=entry)
    # No entries found in directory
    else:
        page_header = "No articles found in the article repository"
        return render_index(request, page_header, entries)

# Aux functions
def render_index(request, page_header, entries):
    return render(request, "encyclopedia/index.html", {
        "page_header": page_header,
        "entries": entries
    })

def search_entries(entries, q):
    result = []
    for entry in entries:
        if q in entry:
            result.append(entry)
    return result
