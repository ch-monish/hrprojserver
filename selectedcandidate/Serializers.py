from rest_framework import serializers
from datetime import datetime
from HRproj.settings import MEDIA_ROOT, MEDIA_URL
from candidate.models.Candidate_Feedback_Model import Candidate_Feedback
from candidate.models.Feedback_Category_Model import Feedback_Category
from candidate.models.candidateapprovalmodel import CandidateApprovalModel
from candidate.models.candidatemodel import Candidate
from jobpost.models.jobpostmodel import JobPost
from managestages.models import Stage
from candidate.models.candidateactionmodel import CandidateActionModel
import os
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from candidate.models.selected_Candidates_Model import Selected_Candidates
from jobpost.serializers import JobPostDetailsGridSerializer
from selectedcandidate.models.Candidatepersonalinfo import CandidatePersonalInfo
from selectedcandidate.models.Candidatefamilydetails import CandidateFamilyDetails
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.models.Candidateemployementdetails import CandidateEmployementDetials
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
from selectedcandidate.models.Candidateinsurancedetails import CandidateInsuranceDetails
from selectedcandidate.models.Candidatebankdetails import CandidateBankDetails
from selectedcandidate.models.Candidatepfdetails import CandidatePfDetails
class candidatepersonalinfogetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatePersonalInfo
        fields="__all__"

class candidateinsurancedetailgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateInsuranceDetails
        fields="__all__"

class candidatePFdetailgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatePfDetails
        fields="__all__"

class candidatebankdetailgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateBankDetails
        fields="__all__"
class bankdetailupdaeSerializer(serializers.ModelSerializer):

    def update(self,instance,validated_data):
        print("calling update function")

        instance.Id=validated_data.get("Id",instance.Id)
        instance.BankName=validated_data.get("BankName",instance.BankName)
        instance.AccountNumber=validated_data.get("AccountNumber",instance.AccountNumber)
        instance.BranchName=validated_data.get("BranchName",instance.BranchName)
        instance.IFSCcode=validated_data.get("IFSCcode",instance.IFSCcode)
        print("after instance")
        try:
            if validated_data["BankPassbook"] is not None:
                os.remove(os.path.join(MEDIA_ROOT,str(instance.BankPassbook)))
        except:
            print("file not found")
        finally:
            if validated_data["BankPassbook"] is not None:
                instance.BankPassbook=validated_data.get("BankPassbook",instance.BankPassbook)
        instance.save()
        return instance
    class Meta:
        model = CandidateBankDetails
        fields="__all__"


class candidatefamilydetailgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateFamilyDetails
        fields="__all__"
class candidateeducationdetailgetSerializer(serializers.ModelSerializer):
    files=serializers.SerializerMethodField()
    
    def get_files(self,educationdetial):
     
        candidatedocob=CandidateDocumentsUpload.objects.filter(detailtype="Education",detailtypeId=educationdetial.id,selectedcandidate_id=educationdetial.selectedCandidateId_id)
        serializer = CandidatedocumentsSerializer(instance=candidatedocob, many=True)
        return serializer.data   
    class Meta:
        model = CandidateEducationalDetails
        fields="__all__"
class candidateemployementdetailgetSerializer(serializers.ModelSerializer):
    files=serializers.SerializerMethodField()
    
    def get_files(self,employementob):
     
        candidatedocob=CandidateDocumentsUpload.objects.filter(detailtype="Employment",detailtypeId=employementob.id,selectedcandidate_id=employementob.selectedCandidateId_id)
        serializer = CandidatedocumentsSerializer(instance=candidatedocob, many=True)
        return serializer.data 
    class Meta:
        model = CandidateEmployementDetials
        fields="__all__"
class Documentuploadserializer(serializers.ModelSerializer):
    def validate(self, data):
        print(self.context)
        return data
    def create(self, validated_data):
        # sco=Selected_Candidates.objects.filter(Selected_Candidate_ID=validated_data["selectedCandidateId"]).first()   
        for i in self.context.getlist('file'):
            CandidateDocumentsUpload.objects.create(
            # selectedCandidateId =  sco,
            selectedcandidate = validated_data["selectedcandidate"],
            detailtypeId=validated_data["detailtypeId"],
            detailtype=validated_data["detailtype"],
            file=i,
            verified=validated_data["verified"]
    
        )



    #     uploadeddoc = CandidateDocumentsUpload.objects.create(
    #         # selectedCandidateId =  sco,
    #         selectedcandidate = validated_data["selectedcandidate"],
    # detailtypeId=validated_data["detailtypeId"],
    # detailtype=validated_data["detailtype"],
    # file=validated_data["file"],
    #     )
        return "success"
    class Meta:
        model=CandidateDocumentsUpload
        fields="__all__"
class CandidatedocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CandidateDocumentsUpload
        fields="__all__"
# class selectedcandidatesemploymentserializer(serializers.ModelSerializer):
#     designation_name = serializers.CharField(read_only=True, source="designation.DesignationName")
#     band_name = serializers.CharField(read_only=True, source="band.BandName")
#     subband_name = serializers.CharField(read_only=True, source="subband.SubBandName")
#     jobpost=JobPostDetailsGridSerializer(source="candidate.Jobpost")
#     candidate=CandidateDetailsGridSerializer(source="candidate")
#     # candidate=serializers.ModelSerializer()
#     class Meta:
#         model=Selected_Candidates
#         fields="__all__"
