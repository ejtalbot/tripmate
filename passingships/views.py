from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.contrib.auth.models import User
from .models import UserProfile, Itinerary
from .forms import UserProfileForm, ItineraryForm
from django.views.generic.detail import DetailView

def home(request):
    context = RequestContext(request, {
        'request': request,
        'user': request.user })
    return render_to_response('passingships/home.html', context_instance = context)


def editprofile(request):
    puser = UserProfile.objects.get(user = request.user)
    if request.POST:
        form = UserProfileForm(request.POST, instance = puser)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect('/passingships/')
    form = UserProfileForm(instance = puser, initial = {
        'age': puser.age,
        'home_country': puser.home_country,
        'home_city': puser.home_city })
    print(puser.id)
    args = { }
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'passingships/profileupdate.html', args)


def newitinerary(request):
    if request.POST:
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit = False)
            itinerary.owner = request.user
            itinerary.save()
            return HttpResponseRedirect('/passingships/')
    form = ItineraryForm()
    args = { }
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'passingships/newitinerary.html', args)


def edititinerary(request, pk):
    itinerary = get_object_or_404(Itinerary, pk = pk)
    if request.POST:
        form = ItineraryForm(request.POST, instance = itinerary)
        if form.is_valid():
            itinerary = form.save(commit = False)
            itinerary.owner = request.user
            itinerary.save()
            return HttpResponseRedirect(reverse('passingships:detail', args = (request.user.id,)))
    form = ItineraryForm(instance = itinerary)
    args = { }
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'passingships/newitinerary.html', args)


class DetailView(DetailView):
    context_object_name = 'user'
    model = User
    template_name = 'passingships/detail.html'
    
    def get_queryset(self):
        return User.objects.prefetch_related('itineraries').all()
