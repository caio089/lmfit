from django.shortcuts import render

def loja(request):
    return render(request, "loja/loja.html")  # 👉 importante: incluir "pag1/"
