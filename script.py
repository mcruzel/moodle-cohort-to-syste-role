# Maxime Cruzel
# Role system assign
# V 1.2, 2023, February
# This script :
# 1) Read users from a specific system cohort (cohortid)
# 2) Affect those users to a specific role (roleid, contextid)
# 3) (optionnal because can be easily removed) Apply some rules to users from the specific cohort

import time
import requests
import json
import re

cohortid = 0 # cohort members of the cohort whose members will be added to the system role
roleid = 0 # the id of the role which you want to add members from the aimed cohort
userid = 0 # doesn't matter
contextid = 0 # use 1 for system-wide roles

global url_moodle
url_moodle = ""

def request_ws(ws, param_request):
    login = ""
    password = ""
    time.sleep(0.05)
    request = url_moodle+"webservice/rest/simpleserver.php?wsusername="+str(login)+"&wspassword="+str(password)+"&moodlewsrestformat=json&wsfunction="+ws+param_request
    webservice_reponse_content = requests.get(request)
    webservice_reponse_content_py = json.loads(webservice_reponse_content.text)
    return webservice_reponse_content_py

def request_ws_post(ws, param_request):
    login = ""
    password = ""
    time.sleep(0.05)
    request = url_moodle+"webservice/rest/simpleserver.php?wsusername="+str(login)+"&wspassword="+str(password)+"&moodlewsrestformat=json&wsfunction="+ws+param_request
    return requests.post(request)

# Import users id from a system cohort
def import_userid():
    global webservice_reponse_content_py_tableau
    ws = "core_cohort_get_cohort_members"
    param_request = "&cohortids[0]="+str(cohortid)
    webservice_userid_response_content = request_ws(ws, param_request)
    
    webservice_reponse_content_py_tableau =  []
    
    for element in webservice_userid_response_content:
        webservice_reponse_content_py_tableau = element['userids']
        
    print(webservice_reponse_content_py_tableau)
    return len(webservice_reponse_content_py_tableau)

# Role assign to cohort members
def assign_members_to_role(total_count):
    count = 1
    for i in webservice_reponse_content_py_tableau:
        userid = i
        ws = "core_role_assign_roles"
        param_request = "&assignments[0][roleid]="+str(roleid)+"&assignments[0][userid]="+str(userid)+"&assignments[0][contextid]="+str(contextid)
        data = request_ws_post(ws, param_request)
        rules_on_name(userid)
        print(f"{count}/{total_count} for userid = {userid} -> {data}")
        count += 1

# apply domestic rules on teachers/ADM usernames
def rules_on_name(userid):
    ws = "core_user_get_users"
    param_request = "&criteria[0][key]=id&criteria[0][value]="+str(userid)
    data = request_ws(ws, param_request)

    firstname = data['users'][0]['firstname']
    # eliminate, by regex, the number in firstname's homonyms
    pattern = r'[0-9]'
    firstname = re.split(pattern, firstname)[0]
    lastname = data['users'][0]['lastname']
    firstnameC = firstname.capitalize()
    lastnameC = lastname.upper()
    ws = "core_user_update_users"
    param_request = "&users[0][id]="+str(userid)+"&users[0][firstname]="+firstnameC+"&users[0][lastname]="+lastnameC
    data = request_ws(ws, param_request)

def main():
    total_count = import_userid()
    assign_members_to_role(total_count)
    print("Travail terminé")

main()
