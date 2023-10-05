from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown

from . import util
from . import models
from django import forms

#Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
#The view should get the content of the encyclopedia entry by calling the appropriate util function.
#If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
#If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.




def title(request, title):
    if title not in util.list_entries():
        error = HttpResponse("Page not found.")
        return error
    content = Markdown().convert(util.get_entry(title))
    return render(request, "../templates/encyclopedia/title.html", {"title": title, "content": content})

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
       
        if query:
            print("text:", query)
            return title(request, query) 
        else:
            print("No input provided.")
    return HttpResponse("Search results page")


def index(request):
    return render(request, "../templates/encyclopedia/index.html", {
        "entries": util.list_entries()
    })

