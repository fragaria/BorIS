from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from boris.reporting import admin as reporting
from boris.impact import admin as impact


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


admin.autodiscover()

urlpatterns = [
    # Django grappelli
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^reporting/towns/', include(reporting.towns.urls)),
    url(r'^reporting/services/', include(reporting.services.urls)),
    url(r'^reporting/clients/', include(reporting.clients.urls)),
    url(r'^reporting/yearly/', include(reporting.yearly.urls)),
    url(r'^reporting/hygiene/', include(reporting.hygiene.urls)),
    url(r'^reporting/govcouncil/', include(reporting.govcouncil.urls)),

    url(r'^impact/impact/', include(impact.impact.urls)),

    url(r'^services/', include('boris.services.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^doc/', include('django.contrib.admindocs.urls')),

    url(r'^media/(?P<path>.*)$', protected_serve, {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    url(r'^', include(admin.site.urls)),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
