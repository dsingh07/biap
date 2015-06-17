from django.contrib import admin
from app1.models import Patient, PatientData

# Models registered here for use in admin page
# fieldsets returns list of parameters up for editing
# listdisplay decides of order of display
# further additions include adding a search filter and parameter by which to reference object

class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['identifier', 'icr', 'cf', 'tdi', 'age', 'weight']}),
    ]
    list_display = ('identifier', 'icr', 'cf', 'tdi', 'age', 'weight')
    list_filter = ['identifier']
    search_fields = ['identifier']
	
admin.site.register(Patient, PatientAdmin)

class PatientDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Medical Information', {'fields': ['patient', 'data_id', 'time', 'date', 'cgm_value', 'blood_glucose', 'insulin_infusion', 'sr', 'insulin_feed', 'controller_gain', 'mean_glucose', 'glucose_derivative', 'safety', 'basal_insulin', 'carbohydrates', 'calibration', 'sensor_saturation']}),
    ]
    list_display = ('patient', 'data_id', 'time', 'date', 'cgm_value', 'blood_glucose', 'insulin_infusion', 'sr', 'insulin_feed', 'controller_gain', 'mean_glucose', 'glucose_derivative', 'safety', 'basal_insulin', 'carbohydrates', 'calibration', 'sensor_saturation')
	
admin.site.register(PatientData, PatientDataAdmin)