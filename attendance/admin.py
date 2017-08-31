from django.contrib import admin
from .models import Batch, Event, PreClaim, Claim, Department, Student

# Register your models here.
def js_approve(modeladmin, request, queryset):
    queryset.update(js_approve = True)
js_approve.short_description = 'Joint Sec Approves'

@admin.register(PreClaim)
class PreClaimAdmin(admin.ModelAdmin):
    exclude = ('dean_approved','students')
    list_display = ('event','dean_approved')
    actions = (js_approve,)

admin.site.register(Batch)
admin.site.register(Event)
admin.site.register(Department)
#admin.site.register(Student)

admin.site.site_header = "KMC Office"
admin.site.title = "KMC Office"
admin.site.index_title = ""