from django.shortcuts import render

#JC - Home page view
def home_page_view(request):
    return render(request, "pages/home_page.html", {})