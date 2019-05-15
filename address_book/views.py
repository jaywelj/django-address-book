from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.template import Context, loader

import csv, logging


from .models import ContactPerson
from .forms import RegisterForm, ContactPersonForm


def contact_person_list(request):
	contact_persons = ContactPerson.objects.all()
	template = "address_book/contact_person_list.html"
	context = {"contact_persons": contact_persons}

	return render(request, template, context)

def contact_person_add(request):
	if request.method == "POST":
		form = ContactPersonForm(request.POST)

		if form.is_valid():
			new_contact_person = form.save(commit=False)
			new_contact_person.user = request.user
			new_contact_person.save()

			return redirect("contact_person_list")
	else:
		form = ContactPersonForm()

	template = "address_book/contact_person_add.html"
	context = {"form": form}

	return render(request, template, context)

def contact_person_edit(request, pk):
	contact_person = get_object_or_404(ContactPerson, pk=pk)
	if request.method == "POST":
		form = ContactPersonForm(request.POST, instance=contact_person)

		if form.is_valid():
			form.save()

			return redirect("contact_person_list")
	else:
		form = ContactPersonForm(instance=contact_person)

	template = "address_book/contact_person_add.html"
	context = {"form": form}

	return render(request, template, context)

def contact_person_delete(request, pk):
	contact_person = get_object_or_404(ContactPerson, pk=pk)
	if request.method == "POST":
		contact_person.delete()

		return redirect("contact_person_list")

	template = "address_book/contact_person_delete.html"
	context = {"contact_person": contact_person}

	return render(request, template, context)	

def contact_person_import(request):
	if request.method == "POST":
		try:
			csv_file = request.FILES["csv_file"]
			if not csv_file.name.endswith('.csv'):
				messages.error(request,'File is not CSV type')
				# return redirect("contact_person_import")
			#if file is too large, return
			if csv_file.multiple_chunks():
				# messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
				return redirect("contact_person_import")

			file_data = csv_file.read().decode("utf-8")		

			lines = file_data.split("\n")
			#loop over the lines and save them in db. If error , store as string and then display
			for line in lines:						
				fields = line.split(",")
				header1 = fields[0]
				header2 = fields[1]
				header3 = fields[2]
				header4 = fields[3]
				break
			del lines[0]

			for line in lines:						
				fields = line.split(",")
				data_dict = {}
				data_dict[header1] = fields[0]
				data_dict[header2] = fields[1]
				data_dict[header3] = fields[2]
				data_dict[header4[:-1]] = fields[3]
				print(data_dict)

				try:
					form = ContactPersonForm(data_dict)
					if form.is_valid():
						form = form.save(commit=False)
						form.user = request.user	
						form.save()				
													
				except Exception as e:
					logging.getLogger("error_logger").error(repr(e))					
					pass

		except Exception as e:
			print("error")
			pass
		
		return redirect("contact_person_list")	

	template = "address_book/contact_person_import.html"
	return render(request, template)
		

def contact_person_export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow([
	    	"first_name", 
	    	"last_name", 
	    	"contact_number",
	    	"address",
	    ])
    contact_persons = ContactPerson.objects.filter(user=request.user)
    for contact_person in contact_persons:
	    writer.writerow([
	    	contact_person.first_name, 
	    	contact_person.last_name, 
	    	contact_person.contact_number,
	    	contact_person.address,
	    ])

    return response


def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(
				username=form.cleaned_data["username"],
				password=form.cleaned_data["password1"],
			)
			login(request, new_user)

			return redirect("contact_person_list")
	else:
		form = RegisterForm()

	template = "registration/register.html"
	context = {"form": form}

	return render(request, template, context)

