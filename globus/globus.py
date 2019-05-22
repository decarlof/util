import globus_sdk
import time
from globus_lib import *

CLIENT_ID = "8235a963-59a6-4354-9724-d330025b199d"

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow(refresh_tokens=True)

print('Please go to this URL and login: {0}'.format(client.oauth2_get_authorize_url()))

get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

# let's get stuff for the Globus Transfer service
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
# the refresh token and access token, often abbr. as RT and AT
transfer_rt = globus_transfer_data['refresh_token']
transfer_at = globus_transfer_data['access_token']
expires_at_s = globus_transfer_data['expires_at_seconds']

# Now we've got the data we need, but what do we do?
# That "GlobusAuthorizer" from before is about to come to the rescue
authorizer = globus_sdk.RefreshTokenAuthorizer(transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)
# and try using `tc` to make TransferClient calls. Everything should just
# work -- for days and days, months and months, even years
tc = globus_sdk.TransferClient(authorizer=authorizer)
ac = globus_sdk.AuthClient(authorizer=authorizer)
# high level interface; provides iterators for list responses
# while(not time.sleep(5)):
#     print("My Endpoints:")
#     for ep in tc.endpoint_search(filter_scope="my-endpoints"):
#         print("[{}] {}".format(ep["id"], ep["display_name"]))

print("Endpoints shared with me:")
for ep in tc.endpoint_search(filter_scope="shared-with-me"):
    print("[{}] {}".format(ep["id"], ep["display_name"]))

petrel_id = u'e133a81a-6d04-11e5-ba46-22000b92c6ec'

rdp(ac, tc, petrel_id, '/2-BM/', '2020-06', 'decarlof@gmail.com')
