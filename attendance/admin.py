from django.contrib import admin
from .models import Batch, Event, PreClaim, Claim, Department, Student
from django.contrib.admin.models import LogEntry

# Register your models here.

def js_approve(modeladmin, request, queryset):
    queryset.update(js_approved = True)
js_approve.short_description = 'Joint Sec Approves'

def dean_approve(modeladmin,request, queryset):
    queryset.update(dean_approved = True)
dean_approve.short_description = 'Dean Approves'

def sis_approve(modeladmin,request, queryset):
    queryset.update(sis_approved = True)
sis_approve.short_description = 'SIS Approves'
@admin.register(PreClaim)
class PreClaimAdmin(admin.ModelAdmin):
    exclude = ('students','dean_approved')
    list_display = ('event','dean_approved')
    actions = [dean_approve,]
    
    def get_actions(self,request):
        actions = super(PreClaimAdmin, self).get_actions(request)
        if not request.user.has_perm('attendance.preclaim_dean_approve'):
            del actions['dean_approve']
        return actions

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    exclude = ('sis_approved',)
    list_display = ('student','name','period','date','pre_claim_approved','js_approved','sis_approved')
    actions = [js_approve,sis_approve]
    search_fields = ['student__name','student__roll_no','period__department__name']
    def get_actions(self,request):
        actions = super(ClaimAdmin, self).get_actions(request)
        if not request.user.has_perm('attendance.claim_js_approve'):
            del actions['js_approve']
        if not request.user.has_perm('attendance.claim_sis_approve'):
            del actions['sis_approve']
        return actions

admin.site.register(Batch)
admin.site.register(Event)
admin.site.register(Department)
#admin.site.register(Student)

admin.site.register(LogEntry)

admin.site.site_header = "KMC Office"
admin.site.title = "KMC Office"
admin.site.index_title = ""
