#!/usr/bin/env python3
import json

from p81api import api
import sys
import argparse
from csv import reader
from typing import List

from p81api.model import GetNetworksHealthApiCallResult, NetworkHealth, NetworkStatus, Auth, Group, \
    CreateGroupApiCallResult, ApiCallResultBase

parser = argparse.ArgumentParser()
parser.add_argument('--apikey', '-A', type=str, required=True, help='argument takes in the API key from web portal')
parser.add_argument('--file', '-F', type=str, required=True,
                    help='argument takes in a csv format file with groups/descriptions')
parser.add_argument('--delete', '-D', action='store_true', required=False, help='argument allows user to delete groups which are in the csv')



def _get_groups(file_name: str) -> List[Group]:
    results: List[Group] = []
    with open(file_name, 'r') as f:
        csv_reader = reader(f)
        header = next(csv_reader)
        if header is not None:
            for row in csv_reader:
                results.append(Group(*row))
    return results


# TODO handle the result

args = parser.parse_args()
auth: Auth = api.authenticate(args.apikey)

def create_groups():
    groups: List[Group] = _get_groups(args.file)
    result: CreateGroupApiCallResult = api.create_groups(auth, groups)
    if result.success:
        ids = []
        print("Everything is OK")
        for group_creation_result in result.results:
            print(group_creation_result)
            ids.append(group_creation_result.id)
            # del_result: ApiCallResultBase = api.delete_group(auth, group_creation_result.id)
            # if del_result.success:
            #     print(f'Group {group_creation_result.id} was deleted')
            # else:
            #     print(f'Group {group_creation_result.id} was NOT deleted')
        with open('ids.json', 'w') as f:
            json.dump(ids, f)
    else:
        print("There is an error")
        for group_creation_error in result.errors:
            print(group_creation_error)


def delete_groups():
    with open('ids.json', 'r') as f:
        ids = json.load(f)
        for id in ids:
            del_result: ApiCallResultBase = api.delete_group(auth, id)
            if del_result.success:
                 print(f'Group {id} was deleted')
            else:
                 print(f'Group {id} was NOT deleted')

if args.delete:
    delete_groups()
else:
    create_groups()
