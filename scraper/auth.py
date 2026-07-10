import codecs 
import requests

from config.settings import CMS_BASE_URL
from config.settings import CMS_VERSION
from config.settings import USER_AGENT

class AuthenticationManager:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent" : USER_AGENT,
                "Accept" : "application/json",
                "Origin": "https://www.sgx.com",
                "Referer": "https://www.sgx.com/",
            }
        )

        self._token = None

# as there are 3 responsibluty 
    # 1. fetch qr
    # 2. decode rot13
    # 3. return token , nothing more so 
     
    def _fetch_qr_validator(self):

        params = {
            "queryId" : f"{CMS_VERSION}:we_chat_qr_validator"
        }

        response = self.session.get(CMS_BASE_URL, params = params, timeout = 20)
        
        response.raise_for_status()
        return response.json()["data"]["qrValidator"]


# has one job of : ENCODE -> DECODE
    def _decode_rot13(self, encoded): 
        return codecs.decode(encoded, "rot_13")


# SMART CACHE  : if you have a token , dont fetch . if you dont have token , fetch it, decode store and return 
# prevents uncecessarry CMS calls

    def get_token(self):
        if self._token is None:

            qr = self._fetch_qr_validator()
            self._token = self._decode_rot13(qr)

        return self._token
    
    
    def refresh_tokens(self):
        self._token = None
        return self.get_token()

