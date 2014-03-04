from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.contrib.auth.models import User
from django.utils.html import conditional_escape as esc


# Create your models here.

class Farina(models.Model):
    nom = models.CharField(max_length=15)
    preu = models.FloatField()
    stock = models.FloatField()
    up_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('farina_list')

class Extra(models.Model):
    nom = models.CharField(max_length=15)
    preu = models.FloatField()
    text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.nom

class Varietat_pa(models.Model):
    nom = models.CharField(max_length=15)
    preu = models.FloatField()
    preu_mig = models.FloatField()
    farina = models.ForeignKey(Farina, related_name="varietats_pa")
    q_farina = models.FloatField() #Quantitat de Farina
    q_aigua = models.FloatField()
    q_massamare = models.FloatField()
    q_llevatfresc = models.FloatField()
    q_sal = models.FloatField()
    extra = models.ForeignKey(Extra, blank=True, null=True)
    q_extra = models.FloatField(blank=True, null=True)
#    varfor = models.ForeignKey(Varinforn)

    def __unicode__(self):
        return self.nom

    def get_farina(self):
        return self.farina


class Client(models.Model):
    nom = models.CharField(max_length=15)
    acumulatiu = models.BooleanField()

    def __unicode__(self):
        return self.nom

    def get_comandes(self):
        return self.comandes.all()

    def get_absolute_url(self):
        return reverse('client_list')

class Status(models.Model):
    acant = models.BooleanField()
    paula = models.BooleanField()
    sergi = models.BooleanField()

    def __unicode__(self):
        if self.acant==True and self.sergi==True and self.paula==True:
            return "TANCAT"
        else:
            return "OBERT"

    def get_status(self):
        if self.acant==True and self.sergi==True and self.paula==True:
            return 1
        else:
            return 0

    def get_absolute_url(self):
        return reverse('fornada_detail')


class Fornada(models.Model):
    nom = models.CharField(max_length=15)
    data = models.DateField()
    marge_error = models.IntegerField()
    status = models.ForeignKey(Status, null=True, blank=True)
    referent = models.ForeignKey('self', null=True, blank=True)
    varietat_pas = models.ManyToManyField(Varietat_pa)
    observacions = models.TextField(blank='True')

    def __unicode__(self):
        return "%s %s" % (self.nom, self.data)


    def get_status(self):
        return self.status.get_status()

    def get_recomandes(self):
        # if self.referent.comandes.all()
        s = self.referent
        for g in s.get_comandes():
            t = Comanda.objects.create(client=g.client,fornada_id=self.id)
            for r in g.get_incomandes():
                Incomanda.objects.create(comanda = t, de_mig = r.de_mig, after_reparto = r.after_reparto,
                                         no_cobrat = r.no_cobrat, no_entregat = r.no_entregat, num_pans = r.num_pans,
                                         tipus_pa = r.tipus_pa, troc = r.troc)

    def create_varforns(self):
        j = self.varietat_pas.all()
        for s in j:
            Varinforn.objects.create(forn=self, var=s)
            # d = Varietat_pa.objects.get(pk=s.pk)
            # f = Varinforn()
            # f.forn = self
            # f.save()
            # f.var.add(d)


    def get_absolute_url(self):
        return reverse('fornada_detail', kwargs={'pk': self.pk})

    def despesa(self):
        a = 0
        for d in self.get_despeses():
            a = a + d.valor
        return a

    def ingres(self):
        x = 0
        for i in self.get_comandes():
            for s in i.get_incomandes_pasta():
                x = x + ( s.preu() )
        return x

    def benefici(self):
        return self.ingres() - self.despesa()

    def ingres_latent(self):
        x = 0
        for i in self.get_comandes():
            for s in i.get_incomandes_esp():
                x = x + ( s.preu() )
        return x

    def get_comandes(self):
        return self.comandes.all()

    def get_despeses(self):
        return self.despeses.all()

    def get_varietats_pa(self):
        return self.varinforn_set.all()
        #return self.varietats_pa.all()




class Comanda(models.Model):
    client = models.ForeignKey(Client, related_name="comandes")
    fornada = models.ForeignKey(Fornada, related_name="comandes")

    def __unicode__(self):
        return "%s %s" % (self.client, self.fornada)

    def get_incomandes(self):
        return self.incomandes.all()

    def get_incomandes_mat(self):
        return self.incomandes.filter(after_reparto__exact = "")

    def get_incomandes_pasta(self):
        return self.incomandes.filter(no_entregat__exact = "", no_cobrat__exact = "")

    def get_incomandes_deute_client(self):
        return self.incomandes.filter(no_cobrat__exact = "X")

    def get_incomandes_esp(self):
        return self.incomandes.filter(no_entregat__exact = "", no_cobrat__exact = "X")

class Varinforn(models.Model):
    var = models.ForeignKey(Varietat_pa)
    forn = models.ForeignKey(Fornada)
    #related_name='varsinforn')
    #forn = Fornada()
    #var = Varietat_pa()

    def get_nom(self):
        # for i in self.var.all():
            return self.var.nom

    def get_farina(self):
        # for i in self.var.all():
            return self.var.farina.nom

    def get_llavors(self):
            return self.var.extra.nom

    def get_mitjos(self):
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == True:
                        f = f + i.num_pans
        return f

    def get_totalllavors(self):
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == False:
                        f = f + (i.num_pans*i.tipus_pa.q_extra)
                    else:
                        f = f + (i.num_pans*i.tipus_pa.q_extra/2)

        return f + f*self.forn.marge_error/100


    def get_totalfarina(self):
    #     pk = self.kwargs['pk']
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == False:
                        f = f + (i.num_pans*i.tipus_pa.q_farina)
                    else:
                        f = f + (i.num_pans*i.tipus_pa.q_farina/2)

        return f + f*self.forn.marge_error/100

    def get_totalAiguaxVarietat(self):
        #pk = self.kwargs['pk']
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == False:
                        f = f + (i.num_pans*i.tipus_pa.q_aigua)
                    else:
                        f = f + (i.num_pans*i.tipus_pa.q_aigua/2)
        return f + f*self.forn.marge_error/100

    def get_totalMassamarexVarietat(self):
        #pk = self.kwargs['pk']
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == False:
                        f = f + (i.num_pans*i.tipus_pa.q_massamare)
                    else:
                        f = f + (i.num_pans*i.tipus_pa.q_massamare/2)

        return f + f*self.forn.marge_error/100

    def get_totalLlevatfrescxVarietat(self):
        #pk = self.kwargs['pk']
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == False:
                        f = f + (i.num_pans*i.tipus_pa.q_llevatfresc)
                    else:
                        f = f + (i.num_pans*i.tipus_pa.q_llevatfresc/2)
        return f + f*self.forn.marge_error/100

    def get_totalSalxVarietat(self):
        # f = 0
        # for i in self.get_incomandes():
        #     f = f + i.num_pans*self.q_sal
        # return f
        f = 0
        for j in Comanda.objects.filter(fornada__id__exact=self.forn.id):
            for i in j.get_incomandes_mat():
                if i.tipus_pa == self.var:
                    if i.de_mig == False:
                        f = f + (i.num_pans*i.tipus_pa.q_llevatfresc)
                    else:
                        f = f + (i.num_pans*i.tipus_pa.q_llevatfresc/2)
        return f + f*self.forn.marge_error/100




class Troc(models.Model):
    preu = models.FloatField()
    detall = models.TextField()

    def __unicode__(self):
        return "%s" % self.detall

class Incomanda(models.Model):
    tipus_pa = models.ForeignKey(Varietat_pa, related_name="incomandes")
    de_mig = models.BooleanField(blank=True)
    num_pans = models.IntegerField()
    troc = models.ForeignKey(Troc, related_name="incomandes", null=True, blank=True)
    comanda = models.ForeignKey(Comanda, related_name="incomandes")
    after_reparto = models.BooleanField(blank=True)
    no_entregat = models.BooleanField(blank=True)
    no_cobrat = models.BooleanField(blank=True)

    # def get_absolute_url(self):
    #     return ('fornada_detail', (), {'pk':self.get_fornada()})
    def __unicode__(self):
        return "%s %s" % (self.num_pans, self.tipus_pa)

    def preu(self):
        if not self.de_mig:
            return self.num_pans * self.tipus_pa.preu
        else:
            return self.num_pans * self.tipus_pa.preu_mig

class Proveidor(models.Model):
    nom = models.CharField(max_length=15)

    def __unicode__(self):
        return self.nom

class Despesa(models.Model):
    nom = models.CharField(max_length=15)
    valor = models.FloatField()
    fornada = models.ForeignKey(Fornada, null=True, blank=True, related_name="despeses")
    proveidor = models.ForeignKey(Proveidor, max_length=15, null=True, blank=True)
    data = models.DateField()
    cancelat = models.BooleanField()
    observacions = models.TextField(blank='True')
    responsable = models.ForeignKey(User)

    def __unicode__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('despesa_detail', kwargs={'pk': self.pk})

class Finances(models.Model):
    saldo = models.FloatField()

    def get_saldo(self):
        c = self.saldo
        for f in Fornada.objects.all(): #aqui s'ha de corregir que les despes incloses en fornades no siguin
            if f.get_status() == 1:
                c = c + f.benefici()            # sumades dues vegades, i qe les fornades futures no es sumin
        for d in Despesa.objects.filter(cancelat__exact = True):
            if not d.fornada:
                c = c - d.valor
        return c

    def get_vdeutes(self):
        c = 0
        for d in Despesa.objects.filter(cancelat__exact = False):
            c = c + d.valor
        self.deute = c
        return self.deute

    def get_saldoreal(self):
        d = self.get_saldo()
        c = self.get_vdeutes()
        return d-c

class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % workout.get_absolute_url())
                    body.append(esc(workout.nom))
                    # if workout.status.nom == 'OBERT':
                    #     body.append(esc(workout.status))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')



    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.data.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s"><div style="width:100px;height:70px" class="boxed" >%s</div></td>' % (cssclass, body)


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    # Extra attributes
    bio = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user




def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)