from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', 
        {'new_item_text': request.POST.get('item_text', '')})
