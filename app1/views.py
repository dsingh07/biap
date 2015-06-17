from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from app1.models import Patient, PatientData
from app1.forms import UserForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
import csv

# list of views for web application
# RequestContext contains parameters of request object (request method, login details, host etc.)

# Home page view, returns basic HTML page with request context
def home(request):
     context = RequestContext(request)
     return render_to_response('app1/home.html', context)

# Index view, returns list of 10 patients on HTML page
def index(request):
    context = RequestContext(request)
    latest_patient_list = Patient.objects.all().order_by('id')[:10]
    return render_to_response('app1/index.html', {'latest_patient_list': latest_patient_list}, context)

# Subject detail view, returns subject filtered by patient_id, server contains host and IP address to be used in HTML	
def detail(request, patient_id):
    server = request.META['HTTP_HOST']
    context = RequestContext(request, {'server': server})
    p = get_object_or_404(Patient, pk=patient_id)
    return render_to_response('app1/detail.html', {'patient': p}, context)

# Subject overview, returns 5 subjects ordered by ID and server as above	
def overview(request):
    server = request.META['HTTP_HOST']
    context = RequestContext(request, {'server': server})
    latest_patient_list = Patient.objects.all().order_by('id')[:5]
    return render_to_response('app1/overview.html', {'latest_patient_list': latest_patient_list}, context)

# View to send all data parameters for subject of patient_id to a page containing JSON data
# Data used by other pages in html for display	
def patient_data(request, patient_id):
    data_set = PatientData.objects.filter(patient__pk=patient_id)
    list = []
    for i in data_set:
     list.append(i.as_json())		
    d = json.dumps(list);
    return HttpResponse(d, content_type='application/json')

# View for displaying data log for subject with corresponding patient_id
def raw_data(request, patient_id):
    server = request.META['HTTP_HOST']
    context = RequestContext(request, {'server': server})
    q = get_object_or_404(Patient, pk=patient_id)
    return render_to_response('app1/raw_data.html', {'patient': q}, context)

# View to export data as a csv file
# Obtain all data objects for subject with corresponding patient_id and write it in separate rows to a csv file	
def csv_export(request, patient_id):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    csv_data = PatientData.objects.filter(patient__pk=patient_id).order_by('-time')
    writer = csv.writer(response)
    for i in csv_data:
     list = []
     list.append(str(i.as_json()) + "\n")
     writer.writerow(list)
    return response

######################################## WEBHOOK #####################################

# no security to enable access to view from smartphone
@csrf_exempt
def webhook(request):
    try:
        #print "--------------"
        #print "WEBHOOK"
        #print request
		# Loads data into JSON dictionary from parameter within request sent by smartphone
        dictToTest = json.loads(request.META['HTTP_JSON'])
        #print dictToTest
        #print dictToTest['patient']
		
        #if(request.POST):
        #dictToTest = {"data_id":"4", "date":"2014-06-17", "basal_insulin":"15.89","time":"10:28:00","safety":"3","sr":"0.1","insulin_feed":"0.2","glucose_derivative":"0.01","controller_gain":"20.98","mean_glucose":"9.45","patient":"1","insulin_infusion":"9.56","cgm_value":"9.54"}
        
		#defaulted values for unsent parameters
        blood_glucose_x = 0
        carbohydrates_x = 0
        calibration_x = 0
        sensor_saturation_x = 0
		#jsonontent = json.loads(dictToTest)
        #print dictToTest['time']
        pat_id = dictToTest['patient']
        gluc_val = dictToTest['cgm_value']
        p = Patient.objects.get(id=pat_id)
        # send mail in case of adverse event
        if gluc_val <= 3.5:
         send_mail('HYPOGLYCAEMIA ALERT', 'Patient '+str(pat_id)+' needs attention. CGM value too low: ' +str(gluc_val) +' mmol/l.' , 'from@example.com', ['dharmanshu07@hotmail.com'], fail_silently=False)
        if gluc_val >= 12:
         send_mail('HYPERGLYCAEMIA ALERT', 'Patient '+str(pat_id)+' needs attention. CGM value too high: ' +str(gluc_val) +' mmol/l.' , 'from@example.com', ['dharmanshu07@hotmail.com'], fail_silently=False)
        # save object
        new_obj = PatientData.objects.create(patient=p, date=dictToTest['date'], time=dictToTest['time'], mean_glucose=dictToTest['mean_glucose'], insulin_feed=dictToTest['insulin_feed'], sr=dictToTest['sr'], calibration=calibration_x, basal_insulin=dictToTest['basal_insulin'], safety=dictToTest['safety'], sensor_saturation=sensor_saturation_x, data_id=dictToTest['data_id'], glucose_derivative=dictToTest['glucose_derivative'], carbohydrates=carbohydrates_x, controller_gain=dictToTest['controller_gain'], blood_glucose=blood_glucose_x, insulin_infusion=dictToTest['insulin_infusion'], cgm_value=dictToTest['cgm_value'])
        new_obj.save()
		# confirmation of data receipt to smartphone
        return HttpResponse("Data Received")
        
    except Exception as e:
		#print "Exception:", e
     return HttpResponse("ERROR")

# Check it is a post.
# Extract parameters from request and create an object (one of those in models.py)
# Send mail if needed
# Save object.
# Return 200 - OK
   
######################################## WEBHOOK #####################################		

	
# user registration view
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            #print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
     user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'app1/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in
                return HttpResponse("Your BiAP Monitoring account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('app1/login.html', {}, context)
		
	
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')