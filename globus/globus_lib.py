import sys, random

def rdp(ac,           # Authorize client
        tc,           # Transfer client
        endpoint_id,  # Endpoint id on which to create shared folder
        endpoint_top, # Endpoint top directory
        new_share,    # Subdirectory name under top to be created and shared with user
        email):       # User email address for notification

    # Create directory to be shared
    share_path = endpoint_top + new_share + '/'
    tc.operation_mkdir(endpoint_id, path=share_path)

    # Generate user id from user email
    r = ac.get_identities(usernames=email)
    user_id = r['identities'][0]['id']
    # print(r, user_id)
    
    # Set access control and notify user
    rule_data = {
      'DATA_TYPE': 'access',
      'principal_type': 'identity',
      'principal': user_id,
      'path': share_path,
      'permissions': 'r',
      'notify_email': email,
      'notify_message': 
          'The data that you requested from RDP is available.'
    }
    tc.add_endpoint_acl_rule(endpoint_id, rule_data)

