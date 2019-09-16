from django.conf.urls import url
from django.views.generic import TemplateView

from geonode.urls import *

urlpatterns += [
    url(r'^geonode_risks/', include('geonode_risks.urls', namespace='risks')),
]

urlpatterns = [ 
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
] + urlpatterns
