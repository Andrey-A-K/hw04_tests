from django.views.generic.base import TemplateView


# Описать класс AboutAuthorView для страницы about/author
class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


# Описать класс AboutTechView для страницы about/tech
class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
