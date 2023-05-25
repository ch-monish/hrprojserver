#windowsAD ip
from datetime import datetime, date,timedelta
import traceback
from ldap3 import Connection,SUBTREE
from decouple import config
import logging



logger = logging.getLogger(__name__)
# def sendAccountCreationEmail():
#     try:
#         from candidate.models.selected_Candidates_Model import Selected_Candidates
#         from DepartmentInfo.models import DepartmentInformation

#         selectedcandidates = Selected_Candidates.objects.filter(DateOfJoining = date.today()+timedelta(days=7), 
#                                                                 IsOfferAccepted = True, HRCID = None,EmployeeID = None)
#         hrdepartmentInformation = DepartmentInformation.objects.filter(Department = "Belcan US HR").first()

#         # if hrdepartmentInformation is not None:
#         if hrdepartmentInformation is not None:
#             for selectedcandidate in selectedcandidates:
#                 # send email to US HR for acoount creation 
#                 BHUserName =  request.data["BH_User_Name"]       
#                 BHuser = User.objects.get(username=BHUserName)
#                 subject = 'Action: Job Post- '+jobpost1.JobCode+' awaiting for approval'
#                 context = {
#                     'jobcode': jobpost1.JobCode,
#                     'hiringmanager' : jobpost1.LastName+", "+jobpost1.FirstName,
#                     'url' : settings.APP_URL,
#                     'approvername' : BHuser.last_name+", "+BHuser.first_name
#                 }
#                 body = EmailUtils.getEmailBody('Account_Creation_template.html', context)
#                 logger.info(body)
#                 logger.info(subject)
#                 logger.info(BHuser.email)
#                 logger.info(jobpost1.Email)
            
#                 EmailUtils.sendEmail(subject, body, [BHuser.email], [jobpost1.Email])

        
        

#     except Exception as e:
#         logger.info("Account creation email request failed "+str(e)  )

def ManageADUsers():
    try:
        from ManageAdUsers.models import AdUsers
        from ManageAdUsers.serializers import AdUsersSerializer
        from django.contrib.auth.models import User, Group
        dbarr=AdUsersSerializer(AdUsers.objects.all(),many=True).data

        adusersarr=[]
        aduserssamacnames=[]
        con=Connection(config("LDAPIP"),config("LDAPUSER"),password=config("LDAPUSERPASS"),auto_bind=True)
        logger.info(con.result['description'])
        total_entries = 0
        con.search(search_base = 'OU=India,DC=belcan,DC=com',
        search_scope = SUBTREE,
        search_filter = '(memberOf=CN=Belcan India,OU=Security Groups,OU=India,DC=belcan,DC=com)',
        # search_filter = '(objectClass=user)',
            attributes = ['sAMAccountName','cn','givenName','sn','mail','employeeNumber','distinguishedName'])
        total_entries += len(con.response)
        logger.info(total_entries)
        for entry in con.response:
            # logger.info(entry['dn'], entry['attributes'])
            adusersarr.append( entry['attributes'])
            aduserssamacnames.append( entry['attributes']['sAMAccountName'])

        logger.info(adusersarr)

        for i in adusersarr:
            # logger.info(i)
            aduser=AdUsers.objects.filter(UserName=i['sAMAccountName']).first()
            if aduser is  None:
                temp= i
                #create new row code
                user_serializer = AdUsersSerializer(data={"UserName":temp["sAMAccountName"],"FirstName":temp["givenName"],"LastName":temp["sn"],  "Email":temp["mail"] , "Active":True  })
                if user_serializer.is_valid():
                    user_serializer.save()
        
        results =AdUsers.objects.exclude(UserName__in=aduserssamacnames)
        logger.info(results)
        for i in results:
            AdUsers.objects.filter(UserName=i.UserName).update(Active=False)
            User.objects.filter(username=i.UserName).update(is_active=False)

        logger.info("running a job with scheduler//////////////")


    except Exception as e:
        logger.info("Aduser sync Schedular failed "+str(e)  )
        logger.error(traceback.format_exc())