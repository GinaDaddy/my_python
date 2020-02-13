import requests
import sys

# if a client request huge list, 4,000 listings can be returned per page.
# Total 100,000 listings can be returned across 25 pages.
# 100,000 is set by the elastic window size command.
# V1 feeds used to use called scroll and it seemed to handle it but V2 lacks of this.
# The attempt to fetch 100,001 by the page 26th in this case, it blows up.
# This script shows that.

# url = "https://channel.homeaway.com/channel/vacationRentalIndexFeed"
url = "http://api-operations-channel-war-production.us-aus-1-prod.slb.prod.vxe.away.black/channel/vacationRentalIndexFeed"
querystring = {"fromDate": "1970-01-01T00:00:00Z", "paged": "true"}
headers = {
    'authorization': "Bearer NmNhNzMwOGMtODQ3OS00N2U3LWIzODktMzgwM2NlMWU1Y2Nk",
    'content-type': "application/json",
    'cache-control': "no-cache"
}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.json())  # 4,000 listings can be returned at max.
page_number = 1
raw_index_feed = len(response.json()['responseEntity']['entries'])
while 'entries' in response.json()['responseEntity'] and len(response.json()['responseEntity']['entries']) > 0:
    try:
        page_number += 1
        new_params = dict(querystring)
        new_params['page'] = str(page_number)
        response = requests.request("GET", url, headers=headers, params=new_params)
        raw_index_feed += len(response.json()['responseEntity']['entries'])
        print(raw_index_feed)
    except:
        print(f'unknown error: {sys.exc_info()}')
print ('Done')