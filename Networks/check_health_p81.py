#!/usr/bin/env python3

from p81api import api
import sys
import os
from typing import List

from p81api.model import GetNetworksHealthApiCallResult, NetworkHealth, NetworkStatus, Auth

token_headers: Auth = api.authenticate(os.environ['APIKEY'])

GREEN = 0
YELLOW = 1
RED = 2


def get_health_single(nwid):

    health_result: GetNetworksHealthApiCallResult = api.get_network_health(token_headers, nwid)
    _exit_code = GREEN
    if not health_result.success:
        print(f"API call was not successful: {health_result.errors}")
        _exit_code = YELLOW
    else:
        network_health_list: List[NetworkHealth] = health_result.results
        monitoring_results = []
        health: NetworkHealth
        for health in network_health_list:
            for status in health:
                monitoring_results.append( f"{status.type}: {status.meta.instanceId if status.type == 'gateway' else status.meta.tunnelName} is {status.status}")
                if _exit_code != RED:
                    _exit_code = RED if str(status.status).lower() != 'passing' else GREEN
    print(','.join(monitoring_results))
    return _exit_code


nwid = 'ps5hya8NTb'
exit_code = get_health_single(nwid)
sys.exit(exit_code)
