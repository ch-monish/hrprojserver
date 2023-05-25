import os
import zipfile
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from HRproj.settings import MEDIA_ROOT, MEDIA_URL

class zipallfiles(ModelViewSet):
    @action(detail=True,methods=["post"])
    def create_zip(self,request,format=None):
        
        try:
            Selected_Candidateob=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()

            # folder_path=r'C:\Users\dkanagala\Desktop\HrProjServer\Hrportalserver\media\SHS-ADL-00007\ANS-ADL-00007-01'
            folder_path=os.path.join(MEDIA_ROOT,str(Selected_Candidateob.candidate.Jobpost.JobCode),str(Selected_Candidateob.candidate.CandidateCode))
            # Set the file name and extension of the zip file
            zip_filename = os.path.basename(folder_path) + '.zip'
            # Create a new zip file
            zip_file = zipfile.ZipFile(zip_filename, 'w')
            # Iterate over the files in the folder and add them to the zip file
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if root.split("\\")[-1] not in ["Form16"]:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, folder_path))
            # Close the zip file
            zip_file.close()
            # Create an HttpResponse object with the zip file as content
            response = HttpResponse(open(zip_filename, 'rb'), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=' + zip_filename
            return response
        except Exception as e:
             return  Response(e,status=status.HTTP_400_BAD_REQUEST)
