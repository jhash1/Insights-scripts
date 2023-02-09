import requests
import datetime
import json
import pprint
from datetime import date
import time
import config


org = config.FairwindsOrg
bearer_token = config.ApiKey

def query_Fairwinds(start_date, end_date, bearer_token, aggregator, timeout):
    url = f"https://insights.fairwinds.com/v0/organizations/{org}/resources-summary"
    
    bearer_token = config.ApiKey

    headers = {
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json"
    }

    timeout = 300
    #returns list of cluster names from API to use as a param.
    names = getClusterList(start_date, end_date, bearer_token, timeout)
    #iterate over names in cluster list to use as an input var to the requests module.
    for name in names:
        params = {
        "startDate": "2023-01-01T01:00:00Z",
        "endDate": "2023-01-30T23:00:00Z",
        "aggregator": ["cluster", "namespace"],
        "cluster": name,
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            for resource in data["resources"]:
                clusterName = resource['cluster']
                namespace = (resource['namespace'])
                cost = (resource['costs']['actual']['total'])
                # print(clusterName,namespace, cost)
                if cost > float(5):
                    print("Cluster:",clusterName, "->", namespace, "namespace is over the $5 threshold and MTD costs $",(float(round(cost,2))))

        except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            

def getClusterList(start_date: str, end_date: str, bearer_token: str, timeout: int) -> list:
    url= "https://insights.fairwinds.com/v0/organizations/centaurus/all-clusters"

    bearer_token = config.ApiKey

    headers = {
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json"
    }
    params2 = {
        "startDate": "2023-01-01T01:00:00Z",
        "endDate": "2023-01-31T23:00:00Z",
    }
    try:
        response = requests.get(url, params=params2, headers=headers, timeout=timeout)
        if response.status_code == 200:
            cluster_list = response.json()
            return cluster_list
    except:
        print("Request failed with status code:", response.status_code, Exception)   

start_date = "2023-01-01T00:00:00Z",
end_date = "2023-01-30T00:00:00Z",
bearer_token = config.ApiKey
aggregator = ["cluster", "namespace"]
timeout = 300

data = query_Fairwinds(start_date, end_date, bearer_token, aggregator, timeout)
names = getClusterList(start_date, end_date, bearer_token, timeout)
