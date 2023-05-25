
import traceback
from rest_framework import status  
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from candidate.models.candidatemodel import Candidate
from candidate.serializers import CandidateDetailsGridSerializer
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
import base64
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1

logger = logging.getLogger(__name__)
class CandidateDetails(ModelViewSet):
    @action(detail=True, methods=['post'])
    def candidatedetails(self, request, format=None): 
        try:
            candidates = Candidate.objects.filter(Jobpost_id=request.data["jobpostID"])
            CandidateDetailsGrid_serializer = CandidateDetailsGridSerializer(candidates, many=True)
            logger.info(CandidateDetailsGrid_serializer.data)
            return Response(CandidateDetailsGrid_serializer.data)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return Response(e ,status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=True, methods=['post'])
    def download(self,request):
        print(request.data["Resume"])
        file_path = os.path.join( request.data["Resume"])
        print(file_path)
        # file_path=file_path.replace("/", "\\")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response=base64.b64encode(fh.read())
                # response = HttpResponse(fh.read(), content_type="application/pdf")
                # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                # return response
                # logger.info(response)
                return HttpResponse(response, content_type="text/html")
        logger.info(Messages1.FNF)
        return Response(Messages1.FNF, status=status.HTTP_404_NOT_FOUND)