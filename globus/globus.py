import globus_lib

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'

# see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
# to create your project app_id
app_id = "8235a963-59a6-4354-9724-d330025b199d"

ac, tc = globus_lib.create_clients(app_id)

print("Endpoints shared with me:")
for ep in tc.endpoint_search(filter_scope="shared-with-me"):
    print("[{}] {}".format(ep["id"], ep["display_name"]))

# print output for the endpoint shared with me:
# [ad484910-0842-11e7-bb15-22000b9a448b] aps_32id
# [26a93324-0847-11e7-bb15-22000b9a448b] nersc_aps_32id
# [e133a81a-6d04-11e5-ba46-22000b92c6ec] petrel tomography

# picked petrel
globus_server_id = u'e133a81a-6d04-11e5-ba46-22000b92c6ec'

shared_path = globus_lib.create_dir('2020-12', globus_server_id, '/2-BM/', ac, tc)
globus_lib.share_dir(shared_path, 'decarlof@gmail.com', globus_server_id, ac, tc)