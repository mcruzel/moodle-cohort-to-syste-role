# Maxime Cruzel
# Role system assign
# V 1.1, 2022, November
# This script :
# 1) Read users from a specific system cohort (cohortid)
# 2) Affect those users to a specific role (roleid, contextid)
# 3) (optionnal because can be easily removed) Apply some rules to users from the specific cohort

import requests
import json
import re

login = ""
password = ""
cohortid = 0 # cohort members of the cohort whose members will be added to the system role
roleid = 0 # the id of the role which you want to add members from the aimed cohort
userid = 0 # doesn't matter
contextid = 0 # use 1 for system-wide roles

url_moodle = ""


# Import users id from a system cohort
def import_userid():
    global webservice_reponse_content_py_tableau
    ws = "core_cohort_get_cohort_members"
    param_request = "&cohortids[0]="+str(cohortid)
    webservice_userid_response_content = url_moodle+"webservice/rest/simpleserver.php?wsusername="+str(login)+"&wspassword="+str(password)+"&moodlewsrestformat=json&wsfunction="+ws+param_request
    webservice_reponse_content = requests.get(webservice_userid_response_content)
    webservice_reponse_content_py = json.loads(webservice_reponse_content.text)
    webservice_reponse_content_py_tableau =  []
    
    for i in webservice_reponse_content_py:
        webservice_reponse_content_py_tableau = i['userids']
        
    print(webservice_reponse_content_py_tableau)
    return len(webservice_reponse_content_py_tableau)

# Role assign to cohort members
def assign_members_to_role(total_count):
    count = 1
    for i in webservice_reponse_content_py_tableau:
        userid = i
        ws = "core_role_assign_roles"
        param_request = "&assignments[0][roleid]="+str(roleid)+"&assignments[0][userid]="+str(userid)+"&assignments[0][contextid]="+str(contextid)
        webservice_role_assign = url_moodle+"webservice/rest/simpleserver.php?wsusername="+str(login)+"&wspassword="+str(password)+"&moodlewsrestformat=json&wsfunction="+ws+param_request
        webservice_role_assign_post = requests.post(webservice_role_assign)
        print(f"{count}/{total_count} -> {webservice_role_assign_post}")
        count += 1
        
        rules_on_name(userid) # can be deleted

# apply rules on teachers/ADM usernames
def rules_on_name(userid):
    ws = "core_user_get_users"
    param_request = "&criteria[0][key]=id&criteria[0][value]="+str(userid)
    webservice_request = url_moodle+"webservice/rest/simpleserver.php?wsusername="+str(login)+"&wspassword="+str(password)+"&moodlewsrestformat=json&wsfunction="+ws+param_request
    webservice_reponse_content = requests.get(webservice_request)
    webservice_reponse_content_py = json.loads(webservice_reponse_content.text)
    firstname = webservice_reponse_content_py['users'][0]['firstname']
    # eliminer, par regex, le numéro dans le prénom des homonymes
    pattern = r'[0-9]'
    firstname = re.split(pattern, firstname)[0]
    lastname = webservice_reponse_content_py['users'][0]['lastname']
    firstnameC = firstname.capitalize()
    lastnameC = lastname.upper()
    ws = "core_user_update_users"
    param_request = "&users[0][id]="+str(userid)+"&users[0][firstname]="+firstnameC+"&users[0][lastname]="+lastnameC
    webservice_request = url_moodle+"webservice/rest/simpleserver.php?wsusername="+str(login)+"&wspassword="+str(password)+"&moodlewsrestformat=json&wsfunction="+ws+param_request
    webservice_reponse_content = requests.get(webservice_request)
    
    
total_count = import_userid()
assign_members_to_role(total_count)

print("Travail terminé")
