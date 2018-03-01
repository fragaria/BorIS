from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from boris.reporting import admin as reporting


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


admin.autodiscover()

urlpatterns = patterns('',
    # Django grappelli
    (r'^grappelli/', include('grappelli.urls')),

    (r'^reporting/towns/', include(reporting.towns.urls)),
    (r'^reporting/services/', include(reporting.services.urls)),
    (r'^reporting/clients/', include(reporting.clients.urls)),
    (r'^reporting/yearly/', include(reporting.yearly.urls)),
    (r'^reporting/hygiene/', include(reporting.hygiene.urls)),
    (r'^reporting/govcouncil/', include(reporting.govcouncil.urls)),
    (r'^reporting/impact/', include(reporting.impact.urls)),

    (r'^services/', include('boris.services.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^doc/', include('django.contrib.admindocs.urls')),

    url(r'^media/(?P<path>.*)$', protected_serve, {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
     url(r'^', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)