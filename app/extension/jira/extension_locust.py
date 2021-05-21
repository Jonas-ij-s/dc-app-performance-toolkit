import re
import json
from locustio.common_utils import init_logger, jira_measure, JSON_HEADERS
logger = init_logger(app_type='jira')

@jira_measure("locust_app_specific_action")
def app_specific_action(locust):   
    def app_specific_action_add_absence():
        # FETCH ACTUAL API
        body = {"summary":"Test No 3","user":"admin","reportedBy":"admin","startDate":1621728000000,"endDate":1622246400000,"type":"Holiday","message":"holidays","date":1621619927000}
        auth_user = ('admin', 'admin') # <--------- MAKE AN ADMIN REST CALL
        headers = {'Content-Type': 'application/json'}
        url = f'/rest/ijsuap/1.0/addUserAvailability'
        r = locust.post(url, json=body, auth=auth_user, headers=headers, catch_response=True)
        content = r.content.decode('utf-8')
        assert 'Success' in content
    def app_specific_action_check_absence():
        r = locust.get('/rest/ijsuap/1.0/checkAbsence?userName=admin&context=profile&date=1621620376000&_=1621620376373', catch_response=True)  # call app-specific GET endpoint
        content = r.content.decode('utf-8')   # decode response content

        if 'ijs_uap_status' not in content:
            logger.error(f"'ijs_uap_status' was not found in {content}")
        assert 'ijs_uap_status' in content  # assert specific string in response content
    # INVOKE ALL CUSTOM ACTIONS
    app_specific_action_add_absence()
    app_specific_action_check_absence()
    # RESET SESSION USER BACK, UNLESS WE DO THAT WE GET STRANGE 
    # "ADMIN STILL LOGGED IN" ERRORS IN OTHER LOCUST ACTIONS
    # WE DO THAT WITH THIS DUMMY CALL:
    locust.get(f"/secure/BrowseProjects.jspa?selectedCategory=archived", catch_response=True, auth=(locust.session_data_storage["username"], "password"))
