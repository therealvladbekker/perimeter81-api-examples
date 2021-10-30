import os
from datetime import datetime
from io import TextIOWrapper

from p81api import api
from p81api.model import Auth, ListNetworksApiCallResult


def _before(file_descriptor: TextIOWrapper):
    file_descriptor.write('# Perimeter81 Health monitoring section - Start\n')
    file_descriptor.write(f'# Do not modify - config was auto generated at {datetime.now()}\n\n')


def _after(file_descriptor: TextIOWrapper):
    file_descriptor.write('\n# Perimeter81 Health monitoring section - End\n')


auth: Auth = api.authenticate(os.getenv('token'))

result: ListNetworksApiCallResult = api.list_networks(auth)
if result.success:
    cmd_list = []
    service_list = []
    for idx, network in enumerate(result.results, 1):
        cmd_entry = f''' 
define command 
{{
 command_name check_p81_network_health_{idx}
 command_line /usr/local/nagios/libexec/check_health_p81_wrapper.sh {network.id}
}}'''
        cmd_list.append(cmd_entry)
        service_entry = f'''
define service 
{{
    use                     local-service          
    host_name               localhost
    service_description     P81 GW HEALTH_{idx}
    check_command           check_p81_network_health_{idx}
    notifications_enabled   {os.getenv('notifications_enabled', '0')}
    max_check_attempts      {os.getenv('max_check_attempts', '3')}
    normal_check_interval   {os.getenv('normal_check_interval', '0.1')}
    retry_check_interval    {os.getenv('retry_check_interval', '0.1')}
    notification_interval   {os.getenv('notification_interval', '60')}
}}'''
        service_list.append(service_entry)
    home_folder = os.path.expanduser('~')
    with open(os.path.join(home_folder, 'commands.cfg'), 'w') as f:
        _before(f)
        f.write('\n'.join(cmd_list))
        _after(f)
    with open(os.path.join(home_folder, 'localhost.cfg'), 'w') as f:
        _before(f)
        f.write('\n'.join(service_list))
        _after(f)

    print(
        f'Done. The nagios configuration files (for {len(result.results)} networks) [commands.cfg,localhost.cfg] were created under folder: {home_folder}')
else:
    print(f'Failed to list networks: {result.errors}')

