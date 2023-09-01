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
        self.headers = {
            "Content-Type": "application/json"
        }


    def data_callback(self, params):
        """
        :Comment: Checks if Caller has active CallBack request or not
        :param: caller: {ANUMBER}
        :param: api_url: Sinch Contact Pro API URL: https://FQDN:PORT/RI
        :param: resource_cb: Callbacks API resource: /cmi/callbacks
        :param: api_uid: username that has access to callbacks resource
        :param: api_pwd: password of the username that has access to callbacks resource
        :return: If Callback exists, returns "lastResult. If not, then returns False
        """

        # Parameters that have been passed from the IVR block schemes customstate element
        caller = params.get("caller", None)
        api_url = params.get("api_url", None)
        resource_cb = params.get("resource_cb", None)
        api_uid = params.get("api_uid", None)
        api_pwd = params.get("api_pwd", None)

        # No number was given. Probably hidden number
        if not caller:
            return 'ERROR'
        # Make API call
        req_cmi = requests.get(f"{api_url}{resource_cb}?customerNumber={caller}",
                            headers=self.headers,
                            auth=(api_uid,
                                    api_pwd))
        
        res_cmi = req_cmi.json()

        # Return the response to IVR Block scheme to process it further
        if res_cmi:
            return res_cmi
        else:
            return False
