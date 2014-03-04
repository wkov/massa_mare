from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required as auth
from gestio.views import FornadaDetailView, MonthArchiveView, ComandaCreateView, ClientCreateView, ClientDetailView
from gestio.views import ComandaDeleteView, FornadaDeleteView, IncomandaCreateView, FornadaCreateView
from gestio.views import DespesaCreateView, DespesaListView, FarinaListView, FarinaUpdateView, StatusUpdateView
from gestio.views import IncomandaDeleteView, IncomandaUpdateView, UserProfileDetailView, UserProfileEditView
from gestio.views import FornadaUpdateView, StatusUpdateView, ClientListView, DespesaUpdateView, DespesaDetailView
from gestio.views import IncomandaListView, ClientUpdateView

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    url(r'^$', "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name='ini'),
    url(r'^calendar/$', 'gestio.views.calendar_init', name='home'),
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login",
        name="logout"),

    # url(r"^calendar/", ),

    url(r"^accounts/", include("registration.backends.simple.urls")),
    url(r"	^users/(?P<slug>\w+)/$", UserProfileDetailView.as_view(),
        name="profile"),
    url(r"edit_profile/$", auth(UserProfileEditView.as_view())),
    url(r"^fornada/(?P<pk>\d+)$", FornadaDetailView.as_view(),
        name="fornada_detail"),
    url(r"^despesa/update/(?P<pk>\d+)$", DespesaUpdateView.as_view(),
        name="despesa_update"),
    url(r"^despesa/(?P<pk>\d+)$", DespesaDetailView.as_view(),
        name="despesa_detail"),
    url(r"^fornada/delete/(?P<pk>\d+)/$", FornadaDeleteView.as_view(),
        name="fornada_delete"),                                                                     # url(r'^blog/', include('blog.urls')),
    # url(r"^fornada/(?P<suppk>\d+)/comanda/update/(?P<pk>\d+)/$", ComandaUpdateView.as_view(),
    #     name="comanda_update"),
    url(r"^fornada/(?P<suppk>\d+)/comanda/delete/(?P<pk>\d+)/$", ComandaDeleteView.as_view(),
        name="comanda_delete"),
    url(r"^fornada/(?P<pk>\d+)/comanda/create/$", ComandaCreateView.as_view(),
        name="comanda_create"),
    url(r"^fornada/(?P<supk>\d+)/status/update/(?P<pk>\d+)/$", StatusUpdateView.as_view(),
        name="status_update"),
    url(r"^fornada/(?P<suppk>\d+)/comanda/(?P<supk>\d+)/incomanda/delete/(?P<pk>\d+)/$", IncomandaDeleteView.as_view(),
        name="incomanda_delete"),
    url(r"^fornada/(?P<suppk>\d+)/comanda/(?P<supk>\d+)/incomanda/update/(?P<pk>\d+)/$", IncomandaUpdateView.as_view(),
        name="incomanda_update"),
    url(r"^fornada/(?P<supk>\d+)/comanda/(?P<pk>\d+)/incomanda/create/$", IncomandaCreateView.as_view(),
        name="incomanda_create"),
    url(r"^fornada/create/$", FornadaCreateView.as_view(),
        name="fornada_create"),
    url(r"^fornada/update/(?P<pk>\d+)/$", FornadaUpdateView.as_view(),
        name="fornada_update"),
    url(r"^economia/$", 'gestio.views.economia',
        name="economia"),
    # Example: /2012/08/
    url(r'^(?P<pYear>\d{4})/(?P<pMonth>\d+)/$',
        'gestio.views.calendar',
        #MonthArchiveView.as_view(month_format='%m'),
        name="archive_month"),
    url(r'^despeses/(?P<pYear>\d{4})/(?P<pMonth>\d+)/$', 'gestio.views.despeses_calendar',
        name="despeses"),
    url(r'^despeses/$', 'gestio.views.despeses_calendar_init',
        name="despeses"),
    url(r"^despesa/create/$", DespesaCreateView.as_view(),
        name="despesa_create"),
    url(r"^despesa/deutes/$", DespesaListView.as_view(),
        name="despesa_list"),
    url(r"^clients/deutes/$", IncomandaListView.as_view(),
        name="incomanda_list"),
    url(r"^farines/$", FarinaListView.as_view(),
        name="farina_list"),
    url(r"^clients/$", ClientListView.as_view(),
        name="client_list"),
    url(r"^farines/update/(?P<pk>\d+)/$", FarinaUpdateView.as_view(),
        name="farina_update"),
    url(r"^client/create/$", ClientCreateView.as_view(),
        name="client_create"),
    url(r"^client/(?P<pk>\d+)/$", ClientDetailView.as_view(),
        name="client_detail"),
    url(r"^client/update/(?P<pk>\d+)/$", ClientUpdateView.as_view(),
        name="client_update"),
)

#               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
#
# urlpatterns += staticfiles_urlpatterns()