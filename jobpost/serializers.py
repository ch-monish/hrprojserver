from datetime import datetime
from rest_framework import serializers
from ManageCustomer.models import Customer
from ManageExperienceLevel.models import Experience
from ManageIndustry.models import Industry
from ManageLocation.models import Location
from jobpost.models.jobpostactionmodel import JobPostActionModel
from jobpost.models.jobpostapprovalmodel import JobPostApproval

from jobpost.models.jobpostmodel import JobPost
from jobpost.models.jobpostuserrolesmodel import JobPostUserRolesModel
from managebusinessunit.models import BusinessUnit
from managecompany.models import Company
from manageserviceline.models import ServiceLine
from managestages.models import Stage
from django.db.models import Max
from django.contrib.auth.models import User
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1

class  JobPostDetailsGridSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(read_only=True, source="Stage.StageDesc")
    industry_name = serializers.CharField(read_only=True, source="Industry.IndustryName")
    company_name = serializers.CharField(read_only=True, source="Company.CompanyName")
    businessunit_name = serializers.CharField(read_only=True, source="BusinessUnit.BusinessUnitName")
    serviceline_name = serializers.CharField(read_only=True, source="ServiceLine.ServiceLineName")
    customer_name = serializers.CharField(read_only=True, source="Customer.CustomerName")
    location_name = serializers.CharField(read_only=True, source="Location.LocationName")  
    experience_Level = serializers.CharField(read_only=True, source="ExperianceLevel.ExperienceLevel")
    approversDetails = serializers.SerializerMethodField()  
    experiencerange =  serializers.SerializerMethodField()  

    def get_experiencerange(self, jobpost1):
        return str(jobpost1.MinimumExperiance)+"-"+str(jobpost1.MaximumExperiance)+" Years"

    def get_approversDetails(self, jobpost1):
        qs = JobPostApproval.objects.filter(jobpost=jobpost1)
        serializer = JobPostApprovalSerializer(instance=qs, many=True)
        return serializer.data    

    class Meta:
        model = JobPost
        fields = "__all__"


class  JobPostActionGridSerializer(serializers.ModelSerializer):
    jobpost = JobPostDetailsGridSerializer(read_only=True) 

    class Meta:
        model = JobPostApproval
        fields = "__all__"
        

class  JobPostDetailsPostSerializer(serializers.ModelSerializer):    
    # stage_name = serializers.CharField(read_only=True, source="Stage.StageDesc")
    # Stage_id = serializers.IntegerField()
    

    Company = serializers.IntegerField()
    BusinessUnit = serializers.IntegerField()
    ServiceLine = serializers.IntegerField()
    Customer = serializers.IntegerField()
    Location = serializers.IntegerField()
    # ExperianceLevel = serializers.IntegerField()
    Industry = serializers.IntegerField()
    BH_User_Name = serializers.CharField()
    HR_User_Name = serializers.CharField()
    strOnboardingDate = serializers.CharField()


    def validate(self, data):
        missing_fields = [f for f in self.Meta.required_fields if f not in data]

        if missing_fields:
            mf = ", ".join(missing_fields)
            raise serializers.ValidationError(Messages1.JP_miss_fields)

        return data

    def create(self, validated_data):
        stage_name = Constants1.STAGE_JP_BHA
        serviceline = ServiceLine.objects.filter(ServiceLineId=validated_data["ServiceLine"]).first()
        customer = Customer.objects.filter(CustomerId=validated_data["Customer"]).first()
        stage = Stage.objects.filter(StageName=stage_name).first()
        industry = Industry.objects.filter(IndustryId=validated_data["Industry"]).first()
        company = Company.objects.filter(CompanyId=validated_data["Company"]).first()
        businessUnit = BusinessUnit.objects.filter(BusinessUnitId=validated_data["BusinessUnit"]).first()
        location = Location.objects.filter(LocationId=validated_data["Location"]).first()
        # experience = Experience.objects.filter(ExperienceLevelId=validated_data["ExperianceLevel"]).first()
        user = User.objects.get(username=validated_data["UserName"])
        max =  JobPost.objects.all().aggregate(Max('JobPostId'))
        count = JobPost.objects.count()
        # print(max11)
        # aggregate(Max('JobPostId'))
        # if max['JobPostId__max'] is None:
        #     maxvalue = 1
        # else:    
        #     maxvalue =  max['JobPostId__max']+1 
        maxvaluepad = str(count+1).zfill(5)
        if businessUnit and customer :
            jobcode =  businessUnit.Acronym+"-"+customer.Acronym+"-"+maxvaluepad
        else:
            jobcode= None
        CreatedOn = datetime.now()
        # ModifiedBy = None
        ModifiedOn = None
        # validated_data["serviceline"] = serviceline
        # validated_data["customer"] = customer
        # validated_data["Stage"] = stage
        # validated_data["Company"] = company
        # validated_data["BusinessUnit"] = businessUnit
        # validated_data["Location"] = location
        # validated_data["ExperianceLevel"] = experience
                        
        jobpost = JobPost.objects.create(
            JobCode = jobcode,
            UserName =  validated_data["UserName"],
            FirstName = user.first_name,
            LastName = user.last_name,
            Email = user.email,
            Stage = stage,
            Industry = industry,
            Company = company,
            BusinessUnit = businessUnit,
            ServiceLine = serviceline,
            Customer = customer,
            Location = location,
            MinimumExperiance=validated_data["MinimumExperiance"],
            MaximumExperiance=validated_data["MaximumExperiance"],
            MaximumCTC=validated_data["MaximumCTC"],
            EmploymentType = validated_data["EmploymentType"],
            Duration = validated_data["Duration"],
            JobTitle =validated_data["JobTitle"],
            JobDesc =validated_data["JobDesc"],
            NoOfPositions = validated_data["NoOfPositions"],
            # ExperianceLevel = experience,
            Qualification = validated_data["Qualification"],
            OnBoardingDate = validated_data["strOnboardingDate"],
            POReference = validated_data["POReference"],
            CreatedBy = validated_data["UserName"],
            CreatedOn = CreatedOn,
            ModifiedBy = None,
            ModifiedOn = ModifiedOn
        )
        return jobpost

    def update(self, instance, validated_data):
        stage_name = Constants1.STAGE_JP_BHA
        serviceline = ServiceLine.objects.filter(ServiceLineId=validated_data["ServiceLine"]).first()
        customer = Customer.objects.filter(CustomerId=validated_data["Customer"]).first()
        stage = Stage.objects.filter(StageName=stage_name).first()
        industry = Industry.objects.filter(IndustryId=validated_data["Industry"]).first()
        company = Company.objects.filter(CompanyId=validated_data["Company"]).first()
        businessUnit = BusinessUnit.objects.filter(BusinessUnitId=validated_data["BusinessUnit"]).first()
        location = Location.objects.filter(LocationId=validated_data["Location"]).first()
        # experience = Experience.objects.filter(ExperienceLevelId=validated_data["ExperianceLevel"]).first()
        user = User.objects.get(username=validated_data["UserName"])

        substr = instance.JobCode.split("-")[2]
        if businessUnit and customer :
            jobcode =  businessUnit.Acronym+"-"+customer.Acronym+"-"+substr
        else:
            jobcode= None

        instance.JobCode = jobcode
        instance.JobTitle=validated_data.get('JobTitle', instance.JobTitle) 
        instance.ServiceLine = serviceline
        instance.BusinessUnit = businessUnit
        instance.Customer = customer
        instance.Location = location
        instance.EmploymentType =validated_data.get('EmploymentType', instance.EmploymentType)
        instance.Duration =validated_data.get('Duration', instance.Duration)
        instance.JobDesc =validated_data.get('JobDesc', instance.JobDesc)
        instance.NoOfPositions =validated_data.get('NoOfPositions', instance.NoOfPositions)
        # instance.ExperianceLevel = experience
        instance.Qualification = validated_data.get('Qualification', instance.Qualification) 
        instance.OnBoardingDate =validated_data.get('strOnboardingDate', instance.OnBoardingDate)
        instance.POReference = validated_data.get('POReference', instance.POReference)
        instance.ModifiedBy=validated_data.get('ModifiedBy', instance.ModifiedBy)
        instance.ModifiedOn =datetime.now()
        instance.MinimumExperiance=validated_data.get("MinimumExperiance",instance.MinimumExperiance)
        instance.MaximumExperiance=validated_data.get("MaximumExperiance",instance.MaximumExperiance)
        instance.MaximumCTC=validated_data.get("MaximumCTC",instance.MaximumCTC)
        instance.Industry = industry
        instance.Company = company
        instance.Stage = stage
        instance.save()
        return instance
    class Meta:
        model = JobPost
        fields = [
            "UserName",
            # "FirstName",
            # "LastName",
            # "Email",
            "EmploymentType",
            "Duration",
            "JobTitle",
            "JobDesc",
            "NoOfPositions",
            "Qualification",
            "strOnboardingDate",
            "POReference",
            # "Stage",
            # "Company",
            # "BusinessUnit",
            # "ServiceLine",
            # "Customer",
            # "Location",
            # "ExperianceLevel",
            #"Stage_id",
            "Industry",
            "Company",
            "BusinessUnit", 
            "ServiceLine" ,
            "Customer" ,
            "Location" ,
            "MinimumExperiance",
            "MaximumExperiance",
            "MaximumCTC",
            # "ExperianceLevel" ,     
            # "CreatedBy",
            # "ModifiedBy",
            "BH_User_Name",
            "HR_User_Name",
            "ModifiedBy"
        ]
        required_fields = fields


class  JobPostApprovalSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(read_only=True, source="role.name")


    class Meta:
        model = JobPostApproval
        fields = "__all__"

class  JobPostActionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPostActionModel
        fields = "__all__"

class  JobPostUserRolesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPostUserRolesModel
        fields = ["RoleName","UserName", "FullName"]
        