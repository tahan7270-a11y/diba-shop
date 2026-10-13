from django.shortcuts import render


def ai_view(request):
    return render(request, 'ai_view/ai_view.html')