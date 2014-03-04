from django.contrib import admin
from .models import Fornada, Comanda, Client, Farina, Varietat_pa, Despesa, Incomanda, Troc, Varinforn, Finances, Proveidor
from .models import Status, Extra
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile
# Register your models here.
class FornadaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Fornada, FornadaAdmin)

class ComandaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comanda, ComandaAdmin)

class ProveidorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Proveidor, ProveidorAdmin)

class ExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(Extra, ExtraAdmin)

class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)

class FinancesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Finances, FinancesAdmin)

class VarinfornAdmin(admin.ModelAdmin):
    pass
admin.site.register(Varinforn, VarinfornAdmin)

class FarinaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Farina, FarinaAdmin)

class Varietat_paAdmin(admin.ModelAdmin):
    pass
admin.site.register(Varietat_pa, Varietat_paAdmin)

class DespesaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Despesa, DespesaAdmin)

class IncomandaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Incomanda, IncomandaAdmin)

class TrocAdmin(admin.ModelAdmin):
    pass
admin.site.register(Troc, TrocAdmin)

class StatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Status, StatusAdmin)