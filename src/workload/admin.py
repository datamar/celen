from django.contrib import admin
from workload.models import *

admin.site.register([Mission, Document, Implication])