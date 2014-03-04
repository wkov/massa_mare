from datetime import datetime, date
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ComandaForm, IncomandaForm, FornadaForm, DespesaForm, FarinaForm, UserProfileForm, StatusForm
from .models import  Fornada, Comanda, Incomanda, WorkoutCalendar, Despesa, Finances, Farina, UserProfile, Client
from .models import Status
from django.utils.safestring import mark_safe
from calendar import monthrange
from django.contrib.auth import get_user_model
# Create your views here.

class ClientCreateView(CreateView):
    model = Client

class ClientListView(ListView):
    model = Client

class ClientUpdateView(UpdateView):
    model = Client

class IncomandaListView(ListView):
    model = Incomanda
    queryset = Incomanda.objects.filter(no_cobrat=True)

class FornadaDetailView(DetailView):
    model = Fornada


class FornadaUpdateView(UpdateView):
    model = Fornada

class StatusUpdateView(UpdateView):
    model = Status

class DespesaDetailView(DetailView):
    model = Despesa

class ClientDetailView(DetailView):
    model = Client

class DespesaUpdateView(UpdateView):
    model = Despesa

def economia(request):
    finances = Finances.objects.first()

    return render(request, 'gestio/economia.html', {'Finances' : finances,})

def recomandes(request, pk):
    # pk = kwargs['pk']
    # supk = kwargs['supk']
    forn = Fornada(pk)
    # forn2 = Fornada(suts)
    forn.get_recomandes()
    # return reverse("fornada_detail", kwargs = {"pk": pk})
    # return render_to_response(request, 'gestio/fornada_detail.html, {'pk': pk,})
    # return render_to_response()
    # a = forn.get_absolute_url()
    # return a
    # return (request, 'gestio/fornada_detail.html', {'pk' : pk})
    return FornadaDetailView.as_view()(pk)








    # def get_context_data(self, **kwargs):
    #     context = super(FornadaDetailView, self).get_context_data(**kwargs)
    #     varfar = self.model.get_varietats_pa()
    #
    #     for v in varfar():
    #         #fem una llista que contingui els diferents totals per varietat de pa i la fiquem dins el context
    #         list.farina = self.get_totalfarina()
    #         list.add
    #     context["totals"]= list()
    #
    # def get_totalfarina(self):
    #     pk = self.kwargs['pk']
    #     f = 0
    #     for j in Comanda.objects.filter(fornada__id__exact=pk):
    #         for i in j.get_incomandes():
    #             f = f + (i.num_pans*i.tipus_pa.q_farina)
    #     return f
    #
    # def get_totalAiguaxVarietat(self):
    #     pk = self.kwargs['pk']
    #     f = 0
    #     for j in Comanda.objects.filter(fornada__id__exact=pk):
    #         for i in j.get_incomandes():
    #             f = f + (i.num_pans*i.tipus_pa.q_aigua)
    #     return f
    #
    # def get_totalMassamarexVarietat(self):
    #     pk = self.kwargs['pk']
    #     f = 0
    #     for j in Comanda.objects.filter(fornada__id__exact=pk):
    #         for i in j.get_incomandes():
    #             f = f + (i.num_pans*i.tipus_pa.q_massamare)
    #     return f
    #
    # def get_totalLlevatfrescxVarietat(self):
    #     pk = self.kwargs['pk']
    #     f = 0
    #     for j in Comanda.objects.filter(fornada__id__exact=pk):
    #         for i in j.get_incomandes():
    #             f = f + (i.num_pans*i.tipus_pa.q_llevatfresc)
    #     return f
    #
    # def get_totalSalxVarietat(self):
    #     f = 0
    #     for i in self.get_incomandes():
    #         f = f + i.num_pans*self.q_sal
    #     return f

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return date(1900, pMonthNumber, 1).strftime('%B')

def calendar_init(request):
    d = datetime.now()
    pYear = d.year
    pMonth = d.month

    """
    Show calendar of events for specified month and year
    """

    lYear = int(pYear)
    lMonth = int(pMonth)


    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    lContestEvents = Fornada.objects.filter(data__gte=lCalendarFromMonth, data__lte=lCalendarToMonth)
    lCalendar = WorkoutCalendar(lContestEvents).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    return render(request, 'gestio/calendar.html', {'Calendar' : mark_safe(lCalendar),
                                                       'Month' : lMonth,
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : lYear,
                                                       'PreviousMonth' : lPreviousMonth,
                                                       'PreviousMonthName' : named_month(lPreviousMonth),
                                                       'PreviousYear' : lPreviousYear,
                                                       'NextMonth' : lNextMonth,
                                                       'NextMonthName' : named_month(lNextMonth),
                                                       'NextYear' : lNextYear,
                                                       'YearBeforeThis' : lYearBeforeThis,
                                                       'YearAfterThis' : lYearAfterThis,
                                                   })

def calendar(request, pYear, pMonth):
    """
    Show calendar of events for specified month and year
    """



    lYear = int(pYear)
    lMonth = int(pMonth)


    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    lContestEvents = Fornada.objects.filter(data__gte=lCalendarFromMonth, data__lte=lCalendarToMonth)
    lCalendar = WorkoutCalendar(lContestEvents).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    return render(request, 'gestio/calendar.html', {'Calendar' : mark_safe(lCalendar),
                                                       'Month' : lMonth,
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : lYear,
                                                       'PreviousMonth' : lPreviousMonth,
                                                       'PreviousMonthName' : named_month(lPreviousMonth),
                                                       'PreviousYear' : lPreviousYear,
                                                       'NextMonth' : lNextMonth,
                                                       'NextMonthName' : named_month(lNextMonth),
                                                       'NextYear' : lNextYear,
                                                       'YearBeforeThis' : lYearBeforeThis,
                                                       'YearAfterThis' : lYearAfterThis,
                                                   })

# def calendar(request, year, month):
#   my_workouts = Fornada.objects.order_by('data').filter(
#     data__year=int(year), data__month=int(month)
#   )
#   cal = WorkoutCalendar(my_workouts).formatmonth(int(year), int(month))
#   return render_to_response('gestio/calendar.html', {'calendar': mark_safe(cal),})

# class MonthArchiveView(MonthArchiveView):
#     queryset = Fornada.objects.all()
#     date_field = "data"
#     make_object_list = True
#     allow_future = True


def despeses_calendar(request, pYear, pMonth):



    lYear = int(pYear)
    lMonth = int(pMonth)


    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    lContestEvents = Despesa.objects.filter(data__gte=lCalendarFromMonth, data__lte=lCalendarToMonth)
    lCalendar = WorkoutCalendar(lContestEvents).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1


    return render(request, 'gestio/despeses_calendar.html', {'Calendar' : mark_safe(lCalendar),
                                                       'Month' : lMonth,
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : lYear,
                                                       'PreviousMonth' : lPreviousMonth,
                                                       'PreviousMonthName' : named_month(lPreviousMonth),
                                                       'PreviousYear' : lPreviousYear,
                                                       'NextMonth' : lNextMonth,
                                                       'NextMonthName' : named_month(lNextMonth),
                                                       'NextYear' : lNextYear,
                                                       'YearBeforeThis' : lYearBeforeThis,
                                                       'YearAfterThis' : lYearAfterThis,
                                                   })

def despeses_calendar_init(request):

    d = datetime.now()
    pYear = d.year
    pMonth = d.month


    lYear = int(pYear)
    lMonth = int(pMonth)


    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    lContestEvents = Despesa.objects.filter(data__gte=lCalendarFromMonth, data__lte=lCalendarToMonth)
    lCalendar = WorkoutCalendar(lContestEvents).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    finances = Finances.objects.first()

    return render(request, 'gestio/despeses_calendar.html', {'Calendar' : mark_safe(lCalendar),
                                                             'Finances' : finances,
                                                       'Month' : lMonth,
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : lYear,
                                                       'PreviousMonth' : lPreviousMonth,
                                                       'PreviousMonthName' : named_month(lPreviousMonth),
                                                       'PreviousYear' : lPreviousYear,
                                                       'NextMonth' : lNextMonth,
                                                       'NextMonthName' : named_month(lNextMonth),
                                                       'NextYear' : lNextYear,
                                                       'YearBeforeThis' : lYearBeforeThis,
                                                       'YearAfterThis' : lYearAfterThis,
                                                   })


class ComandaCreateView(CreateView):
    model = Comanda
    form_class = ComandaForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("fornada_detail", kwargs = {"pk": pk})

    def form_valid(self, form):
        f = form.save(commit=False)
        #subamoll = get_object_or_404(Subamoll, pk=form.data['suba'])
        #f.subamoll = subamoll
        #f.submitter = self.request.user
        pk = self.kwargs['pk']
        forn = Fornada(pk=pk)
        f.fornada = forn
        f.save()
        return super(ComandaCreateView, self).form_valid(form)

# class ComandaUpdateView(UpdateView):
#     model = Comanda
#     form_class = ComandaForm
#
#     def get_success_url(self):
#         pk = self.kwargs['suppk']
#         return reverse("fornada_detail", kwargs = {"pk": pk})
#
#     def form_valid(self, form):
#         f = form.save(commit=False)
#         pk = self.kwargs['suppk']
#         f.fornada.pk = pk
#         #subamoll = get_object_or_404(Subamoll, pk=form.data['suba'])
#         #f.subamoll = subamoll
#         #f.submitter = self.request.user
#         f.save()
#         return super(ComandaUpdateView, self).form_valid(form)

class IncomandaUpdateView(UpdateView):
    model = Incomanda
    form_class = IncomandaForm

    def get_success_url(self):
        pk = self.kwargs['suppk']
        return reverse("fornada_detail", kwargs = {"pk": pk})

    def form_valid(self, form):
        f = form.save(commit=False)
        # pk = self.kwargs['suppk']
        # f.comanda.fornada.pk = pk
        f.save()
        return super(IncomandaUpdateView, self).form_valid(form)


class IncomandaDeleteView(DeleteView):
    model = Incomanda

    def get_success_url(self):
        pk = self.kwargs['suppk']
        return reverse("fornada_detail", kwargs = {"pk": pk})



class FornadaDeleteView(DeleteView):
    model = Fornada
    success_url = reverse_lazy('home')

class ComandaDeleteView(DeleteView):
    model = Comanda

    def get_success_url(self):
        pk = self.kwargs['suppk']
        return reverse("fornada_detail", kwargs = {"pk": pk})

class FornadaCreateView(CreateView):
    model = Fornada
    form = FornadaForm

    def form_valid(self, form):
        f = form.save(commit=False)
        #subamoll = get_object_or_404(Subamoll, pk=form.data['suba'])
        #f.subamoll = subamoll
        #f.submitter = self.request.user

        f.save()
        f.status = Status.objects.create(acant="", paula="", sergi="")
        if f.referent:
            f.get_recomandes()
        krape = super(FornadaCreateView, self).form_valid(form)
        f.create_varforns()
        return krape


class StatusUpdateView(UpdateView):
    model = Status
    form = StatusForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("fornada_detail", kwargs = {"pk": pk})

    def form_valid(self, form):
        f = form.save(commit=False)
        # pk = self.kwargs['suppk']
        # f.comanda.fornada.pk = pk
        f.save()
        return super(StatusUpdateView, self).form_valid(form)


class FarinaListView(ListView):
    model = Farina

    def get_context_data(self, **kwargs):
        context = super(FarinaListView, self).get_context_data(**kwargs)
        context["form"] = FarinaForm()
        return context


class FarinaUpdateView(UpdateView):
    model = Farina
    form_class = FarinaForm
    success_url = reverse_lazy('farina_list')

    def form_valid(self, form):
        f = form.save(commit=False)
        d = datetime.now()
        f.up_date = d.date()
        f.save()
        return super(FarinaUpdateView, self).form_valid(form)


class DespesaCreateView(CreateView):
    model = Despesa
    form = DespesaForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.save()
        return super(DespesaCreateView, self).form_valid(form)

class DespesaListView(ListView):
    model = Despesa
    queryset = Despesa.objects.filter(cancelat=False)

class IncomandaCreateView(CreateView):
    model = Incomanda
    form_class = IncomandaForm
    # success_url = reverse("fornada_detail", (), { pk: self.get_fornada.pk })

    # def get_context_data(self, **kwargs):
    #     context = super(IncomandaCreateView, self).get_context_data(**kwargs)
    #     fornadax = self.kwargs['fornadax']
    #     context["fornadax"] = Fornada.objects.filter()

    def get_initial(self):
        pk = self.kwargs['pk']
        c = Comanda.objects.get(pk=pk)
        return { 'comanda': c }

    # def comanda(self, request, *args, **kwargs):
    #     pk = self.kwargs['pk']
    #     c = Comanda.objects.get(pk=pk)
    #     return c
    #
    # def as_view(cls, **initkwargs):

    def get_success_url(self):
        pk = self.kwargs['supk']
        return reverse("fornada_detail", kwargs = {"pk": pk})

    def form_valid(self, form):
        f = form.save(commit=False)
        #subamoll = get_object_or_404(Subamoll, pk=form.data['suba'])
        #f.subamoll = subamoll
        #f.submitter = self.request.user
        f.save()
        if f.comanda.client.acumulatiu:
            f.no_cobrat = "X"
        return super(IncomandaCreateView, self).form_valid(form)

class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})