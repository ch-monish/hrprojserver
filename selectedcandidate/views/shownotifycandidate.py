import base64
import os
from smtplib import SMTPResponseException
import traceback
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
from selectedcandidate.Serializers import Documentuploadserializer
from selectedcandidate.Serializers import CandidatedocumentsSerializer
from selectedcandidate.models import *
from candidate.models.selected_Candidates_Model import Selected_Candidates
from HRproj.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR
from django.http import HttpResponse, Http404
import logging

logger = logging.getLogger(__name__)
class Shownotifycandidate(ModelViewSet):
 def shownotifycandidatebutton(self,request,format=None):
    try:
        # do = CandidateDocumentsUpload.objects.filter(
        #     id=request.data["fileid"]).update(verified=request.data["verified"])
        
        alldocs=CandidateDocumentsUpload.objects.filter(selectedcandidate=request.data["selectedcandidateid"],verified="rejected")
        if alldocs.__len__()!=0:
            logger.info(True)
            return Response(True, status=status.HTTP_200_OK)

        # for i in alldocs:
        #     if i.verified=="rejected":
        #        return Response(True, status=status.HTTP_200_OK)
                
        
        logger.info(False)
        return Response(False, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error("Api error :  "+str(e))
        logger.error(traceback.format_exc())
        return Response("Api error :  "+str(e), status=status.HTTP_400_BAD_REQUEST)