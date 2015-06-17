from django.db import models
from django.contrib.auth.models import User

# Subject model containing constant subject parameters
class Patient(models.Model):
    identifier = models.CharField(max_length=200)
    icr = models.FloatField('Insulin-to-carbs Ratio')
    cf = models.FloatField('Correction Factor')
    tdi = models.FloatField('Total Daily Insulin')
    age = models.IntegerField('age')
    weight = models.IntegerField('Patient weight')
	
	# Object referenced by identifier string parameter
    def __str__(self):
        return self.identifier
	
	# Model returned as a JSON dictionary
    def as_json(self):
    	return dict(
			identifier = self.identifier,
			icr = self.icr,
			cf = self.cf,
			tdi = self.tdi,
			age = self.age,
			weight = self.weight)

# Subject model containing dynamic clinical data			
class PatientData(models.Model):
    patient = models.ForeignKey(Patient)
    data_id = models.IntegerField('ID for Database')
    time = models.TimeField('time of sample')
    date = models.DateField('Date sample sent')
    cgm_value = models.FloatField('CGM Measurement')
	# blood glucose will be added soon
    blood_glucose = models.FloatField('Blood Glucose Level')
    insulin_infusion = models.FloatField('Insulin Level From Pump')
    sr = models.FloatField('Secreted Insulin')
    insulin_feed = models.FloatField ('Insulin Feed')
    controller_gain = models.FloatField()
    mean_glucose = models.FloatField()
    glucose_derivative = models.FloatField()
    safety = models.IntegerField('Safety Condition')
    basal_insulin = models.FloatField()
	# parameters not sent yet but could be added in the future
    carbohydrates = models.IntegerField('Meal In Grams')
    calibration = models.BooleanField('Calibration Flag')    
    sensor_saturation = models.BooleanField()    
	
	# Model returned as a JSON dictionary
    def as_json(self):
        return dict(
			patient = self.patient.as_json(),
			data_id = self.data_id,
			time = str(self.time),
			date = str(self.date),
			cgm_value = self.cgm_value, 
			blood_glucose = self.blood_glucose,
			insulin_infusion = self.insulin_infusion,
			sr = self.sr,
			insulin_feed = self.insulin_feed,
			controller_gain = self.controller_gain,
			mean_glucose = self.mean_glucose,
			glucose_derivative = self.glucose_derivative,
			safety = self.safety,
			basal_insulin = self.basal_insulin,
			carbohydrates = self.carbohydrates,
			calibration = self.calibration,
			sensor_saturation = self.sensor_saturation)