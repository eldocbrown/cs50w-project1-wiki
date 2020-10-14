from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
import random as rdm
from . import util
from . import lang_util

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
    mdContent = util.get_entry(entry)
    if mdContent is not None:
        content = lang_util.markdownToHtml(mdContent)
        title = entry
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render_message(request, "Article not found", f"Wiki does not have an article with this exact name. Please search for {entry} in Wiki to check for alternative titles or spellings.")



def random(request):
    entries = util.list_entries()
    # Entries found in directory
    if len(entries) > 0:
        # Select random entry from Entries
        entry = rdm.choice(entries)
        return redirect('encyclopedia:entry', entry=entry)
    # No entries found in directory
    else:
        return render_message(request, "Warning", "No articles found in the article repository")

class NewPageForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'page_title'})
        )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Markdown Syntax Page Content', 'class': 'page_content'})
        )

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            # Try to get page
            if util.get_entry(title) is None:
                # Page does NOT exists
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                # Redirect to the new page just created
                return redirect('encyclopedia:entry', entry=title)
            else:
                # Page already exists
                return render_message(request, "Error", "Article already exists, please try to edit instead.")
        else:
            # Form is NOT valid
            return render_message(request, "Error", "There was an error validating data. Please try again.")

    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

class EditPageForm(forms.Form):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': 'page_content'})
        )

def editpage(request, entry):
    if request.method == "POST":
        """
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            # Try to get page
            if util.get_entry(title) is None:
                # Page does NOT exists
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                # Redirect to the new page just created
                return redirect('encyclopedia:entry', entry=title)
            else:
                # Page already exists
                return render(request, "encyclopedia/entry.html", {
                    "title": "Error",
                    "content": "Article already exists, please try to edit instead."
                })
        else:
            # Form is NOT valid
            return render(request, "encyclopedia/entry.html", {
                "title": "Error",
                "content": "There was an error validating data. Please try again."
            })
        """
        bla = entry
    elif request.method == "GET":
        #Try to get entry
        mdContent = util.get_entry(entry)
        if mdContent is not None:
            content = mdContent
            title = entry
            form = EditPageForm(initial={'content': content})
            return render(request, "encyclopedia/editpage.html", {
                "page_title": title,
                "form": form
            })
        else:
            return render_message(request, "Article not found", f"Wiki does not have an article with this exact name. Please search for {entry} in Wiki to check for alternative titles or spellings.")

def message(request):
    return render(request, "encyclopedia/message.html")

# Aux functions
def render_message(request, title, message):
    return render(request, "encyclopedia/message.html", {
        "title": title,
        "message": message
    })

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
