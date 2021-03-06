# from django.shortcuts import render, render_to_response
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from django.conf import settings

from cal.models import Event, PGroup, Faction, Slot, Entry
from cal.serializers import EventSerializer, FactionSerializer, SlotSerializer
from cal.serializers import PGroupSerializer, EntrySerializer
from rest_framework import viewsets
from cal.permissions import IsOwnerOrReadOnly
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from django.core.urlresolvers import reverse, reverse_lazy


# API Views
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events
    """
    queryset = Event.objects.all().order_by('datetime')
    serializer_class = EventSerializer

    def update(self, request, *args, **kwargs):
        self.methods = ('put', )
        self.permission_classes = (IsOwnerOrReadOnly, )
        return super(self.__class__, self).update(request, *args, **kwargs)


class PGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Player groups
    """
    queryset = PGroup.objects.all().order_by('name')
    serializer_class = PGroupSerializer


class FactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for factions
    """
    queryset = Faction.objects.all().order_by('event', 'name')
    serializer_class = FactionSerializer


class SlotViewSet(viewsets.ModelViewSet):
    """
    API endpoint for slots
    """
    queryset = Slot.objects.all().order_by('faction', 'name')
    serializer_class = SlotSerializer


class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for entries
    """
    queryset = Entry.objects.all().order_by('faction', 'slot')
    serializer_class = EntrySerializer


#
# ---- Generic Django Views
#
class EventListView(ListView):
    queryset = Event.objects.filter(datetime__gte=timezone.now())
    context_object_name = 'events'


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_can_signup'] = self.object.user_can_sign_up(self.request.user)
        return context

    # def attrs(self):
    #     # for attr, value in self._meta.get_fields():
    #     for attr, value in self.__dict__.iteritems():
    #         yield attr, value


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    fields = []
    login_url = settings.LOGIN_REDIRECT_URL

    def get_success_url(self):
        return reverse('cal:event-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        form.instance.user = self.request.user
        faction_id = self.kwargs.get('faction_id')
        slot_id = self.kwargs.get('slot_id')
        if faction_id:
            form.instance.faction = Faction.objects.get(id=faction_id)
        elif slot_id:
            slot = Slot.objects.get(id=slot_id)
            form.instance.slot = slot
            form.instance.faction = Faction.objects.get(id=slot.faction.id)
        return super(EntryCreateView, self).form_valid(form)


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    login_url = settings.LOGIN_REDIRECT_URL

    def get_success_url(self):
        return reverse('cal:event-detail', kwargs={'pk': self.object.faction.event.pk})

    def test_func(self, user):
        return self.get_object().user == user

    def no_permissions_fail(self, request=None):
        return redirect(reverse_lazy('cal:event-details', kwargs={'pk': self.get_object().faction.event.pk}))
