from django.contrib import admin

from enem_calculator_api.core.models import User, Ambition, Simulation

admin.site.register(User)
admin.site.register(Ambition)
admin.site.register(Simulation)
