from django.http import HttpResponse
import datetime
import logging
logger = logging.getLogger(__name__)

def homepage(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Hello Neha :)</h1>")