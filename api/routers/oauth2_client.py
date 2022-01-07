import os
import requests
from requests_oauthlib import OAuth2Session
from pydantic import HttpUrl
from fastapi.responses import RedirectResponse
from api.models.jd_response import JDResponse
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from fastapi import Request, APIRouter
router = APIRouter()

# TODO: use Pydantic Settings for "config/settings mgmt"? Config / Settings classes
client_id = os.environ['JD_OAUTH_CLIENT']
client_secret = os.environ['JD_OAUTH_SECRET']
redirect_uri = os.environ['JD_CLIENT_REDIRECT_URI']
oauth_well_known_url = os.environ['JD_WELL_KNOWN_URL']
jd_headers = os.environ['JD_HEADERS']
jd_api_catalog_uri = os.environ['JD_API_CATALOG_URI']


# use HATEOS or hardcode to env url?
# JD_WELL_KNOWN_URL
# Query the ./well-known OAuth URL and parse out the authorization URL, the token grant URL, and the available scopes
# TODO: I Want this to happen on app startup "syncronously" rather than for every request
# should i even spin up a Fast API without?
# in the past i used an async helper for node-config to manage this and get the envirionment vars set 
# await?
well_known_response = requests.get(oauth_well_known_url)
well_known_info = well_known_response.json()

JD_AUTHORIZATION_URL: HttpUrl = well_known_info['authorization_endpoint']
JD_TOKEN_GRANT_URL: HttpUrl = well_known_info['token_endpoint']
JD_AVAILABLE_SCOPES = str(' ').join(well_known_info['scopes_supported'])


print('Well Known Authorization URL - ' + JD_AUTHORIZATION_URL)
print('Well Known Token Grant URL - ' + JD_TOKEN_GRANT_URL)
print('Available Scopes - ' + JD_AVAILABLE_SCOPES)

#authorization_base_url = 'https://github.com/login/oauth/authorize'
# use HATEOS or hardcode?
#token_url = 'https://github.com/login/oauth/access_token'

SCOPES_TO_REQUEST = {'offline_access', 'ag1', 'eq1', 'files'}

# authorization_request, state = oauth2_session.authorization_url(AUTHORIZATION_URL, STATE)
# print("Click on the following link to present the user with sign in form where they authenticate and approve access to your application.")
# print(authorization_request)

# TODO: routes in diff files? 
# TODO: async?
@router.get("/jdlogin")
def login(request: Request):
    SCOPES_TO_REQUEST = {'offline_access', 'ag1', 'eq1', 'files'}
    jd_oauth2_session = OAuth2Session(client_id,  redirect_uri=redirect_uri, scope=SCOPES_TO_REQUEST)
    authorization_url, state = jd_oauth2_session.authorization_url(JD_AUTHORIZATION_URL)

    # OAuth2 (rfc6749) - Cross-Site Request Forgery
    # https://datatracker.ietf.org/doc/html/rfc6749#section-10.12
    request.session.update({'oauth_state': state})
    
    return RedirectResponse(authorization_url)
    

# TODO: async?
@router.get("/jdcallback")
def callback(request: Request):
    # OAuth2 (rfc6749) - Cross-Site Request Forgery
    # https://datatracker.ietf.org/doc/html/rfc6749#section-10.12
    jd_oauth2_session = OAuth2Session(client_id, state=request.session['oauth_state'], redirect_uri=redirect_uri)

    token_response = jd_oauth2_session.fetch_token(JD_TOKEN_GRANT_URL, client_secret=client_secret,
                               authorization_response=str(request.url))
    # TODO: persist token with username ....
    #access_token = token_response['access_token']
    #refresh_token = token_response['refresh_token']
    #access_token_expiration = token_response['expires_in']
    
    # TODO: move to Pydantic settings/config
    MYJOHNDEERE_V3_JSON_HEADERS = { 'Accept': 'application/vnd.deere.axiom.v3+json',
                                'Content-Type': 'application/vnd.deere.axiom.v3+json'}
    # use HATEOAS again to pick a url and plug in here
    api_catalog_response: requests.Response = jd_oauth2_session.get(jd_api_catalog_uri, headers=MYJOHNDEERE_V3_JSON_HEADERS) 

    assert(200 == api_catalog_response.status_code)
    resp = JDResponse.parse_raw(api_catalog_response.content)
    
    api_somevalidhateoaslink_response: requests.Response = jd_oauth2_session.get(resp.links[0].uri, headers=MYJOHNDEERE_V3_JSON_HEADERS) 
    return api_somevalidhateoaslink_response.json()

