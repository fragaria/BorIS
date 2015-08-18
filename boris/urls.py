from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static

from boris.reporting import admin as reporting


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

    (r'^services/', include('boris.services.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)