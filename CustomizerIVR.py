# coding=latin-1

import requests
import json
import VER
import datetime
VER.VER(__file__,
"""
Filename:    CustomizerIVR.py
Description: IVR Customizer:
             Check for active callbacks in the contact center
             Create a new callback to the queue
""",
"1.0.0.0")

from Env        import *
from ICustomize import *
from IVRUtil    import *
from ADO        import *

class CustomizerIVR(ICustomize):

    # NOTE: Keep name, Filename and class name identical.

    # ========================================================================

    def __init__(self, AppConf):
        # Call the base class constructor
        ICustomize.__init__(self, AppConf)


    def data_callback(self, params):
        """
        :comment: Checks if Caller has active CallBack request or not
        :param: caller: {ANUMBER}
        :param: api_url: Sinch Contact Pro API URL: https://FQDN:PORT/RI
        :param: resource_cb: Callbacks API resource: /cmi/callbacks
        :param: api_uid: username that has access to callbacks resource
        :param: api_pwd: password of the username that has access to callbacks resource
        :return: If Callback exists, returns "lastResult. If not, then returns False
        """

        # Parameters that have been passed from the IVR Block schemes customstate element
        caller = params.get("caller", None)
        api_url = params.get("api_url", None)
        resource_cb = params.get("resource_cb", None)
        api_uid = params.get("api_uid", None)
        api_pwd = params.get("api_pwd", None)

        # No number was given. Probably hidden number
        if not caller:
            return 'ERROR'
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Make API call
        req_cmi = requests.get(f"{api_url}{resource_cb}?customerNumber={caller}",
                               headers=headers,
                               auth=(api_uid,
                                     api_pwd))
        
        res_cmi = req_cmi.json()

        # Return the response to IVR Block scheme to process it further
        if res_cmi:
            return res_cmi[0]
        else:
            return False
        
    
    def create_callback(self, params):
        """
        :comment: Creates a callback for the caller
        :param: caller: {ANUMBER}
        :param: api_url: Sinch Contact Pro API URL: https://FQDN:PORT/RI
        :param: resource_cb: Callbacks API resource: /cmi/callbacks
        :param: api_uid: username that has access to callbacks resource
        :param: api_pwd: password of the username that has access to callbacks resource
        :param: queue_number_cb: Callback queue number
        :return: Returns the created Callback ID

        """

        # Parameters that have been passed from the IVR Block schemes customstate element
        caller = params.get("caller", None)
        api_url = params.get("api_url", None)
        resource_cb = params.get("resource_cb", None)
        api_uid = params.get("api_uid", None)
        api_pwd = params.get("api_pwd", None)
        queue_number_cb = params.get("queue_number_cb", None)

        # No number was given. Probably hidden number
        if not caller:
            return 'ERROR'
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Assemble JSON for API
        callback_json = {
            "customerNumber": f"{caller}",
            "callbackQueueNumber": f"{queue_number_cb}",
            "notes": "Callback created from IVR"
        }

        callback_json = json.dumps(callback_json)

        req_cmi = requests.post(f"{api_url}{resource_cb}?customerNumber={caller}",
                                headers=headers,
                                data=callback_json,
                                auth=(api_uid,
                                      api_pwd))
        
        res_cmi = req_cmi.text
        
        if "Callback queue not found" in res_cmi:
            return ["ERROR", res_cmi]
        else:
            return res_cmi
