# Maxime Cruzel
# Role system assign
# V 1.0, 2022, July

import requests
import json

token_ws_cohort_reading = "xxxxxx"
token_ws_role_assign = "xxxxx"
url_moodle = "https://xxx"
cohortid = 0 # cohort members of the cohort whose members will be added to the system role
roleid = 0 # the id of the role which you want to add members from the aimed cohort
userid = 0 # doesn't matter
contextid = 1 # use 1 for system-wide roles




# Import users id from a system cohort
def import_userid():
    global webservice_reponse_content_py_tableau
    webservice_userid_response_content = url_moodle+"/webservice/rest/server.php?wstoken="+token_ws_cohort_reading+"&wsfunction=core_cohort_get_cohort_members&moodlewsrestformat=json&cohortids[0]="+str(cohortid)
    webservice_reponse_content = requests.get(webservice_userid_response_content)
    webservice_reponse_content_py = json.loads(webservice_reponse_content.text)
    webservice_reponse_content_py_tableau =  []
    
    for i in webservice_reponse_content_py:
        webservice_reponse_content_py_tableau = i['userids']
        
    print(webservice_reponse_content_py_tableau)

# Role assign to cohort members
def assign_members_to_role():
    for i in webservice_reponse_content_py_tableau:
        userid = i
        webservice_role_assign = url_moodle+"/webservice/rest/server.php?wstoken="+token_ws_role_assign+"&wsfunction=core_role_assign_roles&moodlewsrestformat=json&assignments[0][roleid]="+str(roleid)+"&assignments[0][userid]="+str(userid)+"&assignments[0][contextid]="+str(contextid)
        print(webservice_role_assign)
        webservice_role_assign_post = requests.post(webservice_role_assign)
    print("Travail terminé")    
        
import_userid()
assign_members_to_role()
