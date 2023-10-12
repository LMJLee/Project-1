from django.shortcuts import render, redirect
import re
from django.http import HttpResponse
from markdown import Markdown
import markdownify 
import os
from . import util
from . import models
from django import forms

#Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
#The view should get the content of the encyclopedia entry by calling the appropriate util function.
#If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
#If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.


def title(request, title):
    entry_list = [entry.lower() for entry in util.list_entries()]  
    if title.lower() not in entry_list:
        return index(request)
    content = Markdown().convert(util.get_entry(title))
    return render(request, "encyclopedia/title.html", {"title": title, "content": content})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q').lower() 

        entries = [entry.lower() for entry in util.list_entries()]
      
        if query in entries:
            return title(request, query) 
        else:
            # Get a list of all files in the "entries" directory
            all_files = os.listdir("entries")

            # Filter files that contain the substring (convert query to lowercase)
            test1 = [filename for filename in all_files if query in filename.lower()]
            test = sorted(re.sub(r"\.md$", "", filename)
                for filename in test1 if filename.endswith(".md"))

            print(test)
            print(query)
            return render(request,"../templates/encyclopedia/sub.html", {"test": test})
        
      

def index(request):
    return render(request, "../templates/encyclopedia/index.html", {"entries": util.list_entries()})

def create(request):
    return render(request, "../templates/encyclopedia/create.html")


def createpage(request):
    if request.method == 'GET':
        return render(request, "../templates/encyclopedia/create.html")  # Assuming you have a template for creating a page
    
    elif request.method == 'POST':
        title = request.POST.get('page-title')
        text = request.POST.get('page-text')

        content = markdownify.markdownify(text)

        # Save the entry using your util function (assuming it returns an HttpResponse)
        result = util.save_entry(title, content)

        # Check if the save operation was successful and return an appropriate response
        if result:
            return redirect('index')   #  return an HttpResponse 
        else:
            # Handle the case where the save operation failed
            return HttpResponse("Error saving the entry")

    else:
        return redirect('index')  