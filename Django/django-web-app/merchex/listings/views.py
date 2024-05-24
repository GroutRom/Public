from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Band, Ad
from listings.forms import ContactUsForm, BandForm, AdForm
from django.core.mail import send_mail
from django.shortcuts import redirect


def band_list(request) :
	bands = Band.objects.all()
	return render(request, 'listings/band_list.html', {'bands': bands})

def about(request) :
	return render(request, 'listings/about.html')

def ad_list(request) :
	ads = Ad.objects.all()
	return render(request,'listings/ad_list.html', {'ads' : ads})

def contact(request) :
	if request.method == 'POST' :
		form = ContactUsForm(request.POST)

		if form.is_valid() :
			send_mail(subject=f'Message from {form.cleaned_data["nom"] or "anonyme"} via MerchEx Contact Us form',
				message=form.cleaned_data['message'],
				from_email=form.cleaned_data['email'],
				recipient_list=['admin@merchex.xyz'],
			)
			return redirect('email-sent')

	else :
		form = ContactUsForm()
	return render(request, 'listings/contact.html', {'form':form})

def band_detail(request, id):
	band = Band.objects.get(id=id)
	return render(request, 'listings/band_detail.html', {'band':band})

def band_create(request):
	if request.method == 'POST' :
		form = BandForm(request.POST)
		if form.is_valid() :
			band = form.save()
			return redirect('band-detail', band.id)
	else :
		form = BandForm()
	return render(request, 'listings/band_create.html', {'form':form})

def band_update(request, id):
	band = Band.objects.get(id=id)
	
	if request.method == 'POST' :
		form = BandForm(request.POST, instance=band)
		if form.is_valid():
			form.save()
			return redirect('band-detail', band.id)
	else :
		form = BandForm(instance=band)

	return render(request, 'listings/band_update.html', {'form':form})

def band_delete(request, id):
	band = Band.objects.get(id=id)

	if request.method == 'POST' :
		band.delete()
		return redirect('band-list')

	return render(request, 'listings/band_delete.html', {'band':band})

def ad_detail(request, id):
	ad = Ad.objects.get(id=id)
	return render(request, 'listings/ad_detail.html', {'ad':ad})

def ad_create(request):
	if request.method == 'POST' :
		form = AdForm(request.POST)
		if form.is_valid:
			ad = form.save()
			return redirect('ad-detail', ad.id)
	else :
		form = AdForm()
		return render(request, 'listings/ad_create.html', {'form' : form})

def ad_update(request, id):
	ad = Ad.objects.get(id=id)

	if request.method == 'POST' :
		form = AdForm(request.POST, instance=ad)
		if form.is_valid():
			form.save()
			return redirect('ad-detail', ad.id)
	else :
		form = AdForm(instance=ad)

	return render(request, 'listings/ad_update.html', {'form':form})

def ad_delete(request, id):
	ad = Ad.objects.get(id=id)

	if request.method == 'POST' :
		ad.delete()
		return redirect('ad-list')

	return render(request, 'listings/ad_delete.html', {'ad':ad})
def email_sent(request):
	return render(request, 'listings/email_sent.html')