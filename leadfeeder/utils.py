import requests
import os
from fivetran_connector_sdk import Logging as log
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_TOKEN = os.getenv("LEADFEEDER_API_TOKEN")
BASE_URL = os.getenv("LEADFEEDER_BASE_API_URL")
ACCOUNT_ID = os.getenv("LEADFEEDER_ACCOUNT_ID")

LEADS_ENDPOINT = f'/accounts/{ACCOUNT_ID}/leads'
VISITS_ENDPOINT = f'/accounts/{ACCOUNT_ID}/visits'

session = requests.Session()
retry_strategy = Retry(
    total=5,                 
    backoff_factor=2,         
    status_forcelist=[429, 500, 502, 503, 504], 
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

def fetch_data(endpoint, params):
    headers = {
        "Authorization": f"Token token={API_TOKEN}",
        "User-Agent": "FivetranConnector/1.0",
    }
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = session.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        log.error(f"HTTP error calling {url}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        log.error(f"Request failed calling {url}: {e}")
        raise

def fetch_visits(params):
    visit_params = params.copy()
    visits = []
    visit_routs = []
    
    while True:
        response = fetch_data(VISITS_ENDPOINT, visit_params)

        if 'data' not in response or not response['data']:
            log.info("Reponse has no data, exiting loop")
            break
        
        log.info(f"fetched {len(response['data'])} for page {visit_params['page[number]']}")

        for item in response['data']:
            visit_id = item['id']
            visit = item['attributes']
            visits.append(
                {
                    'visit_id': visit_id,
                    'source': visit['source'],
                    'medium': visit['medium'],
                    'referring_url': visit['referring_url'],
                    'landing_page_path': visit['landing_page_path'],
                    'keyword': visit['keyword'],
                    'visit_length': visit['visit_length'],
                    'started_at': visit['started_at'],
                    'campaign': visit['campaign'],
                    'query_term': visit['query_term'],
                    'lf_client_id': visit['lf_client_id'],
                    'country_code': visit['country_code'],
                    'device_type': visit['device_type'],
                    'visitor_email': visit['visitor_email'],
                    'visitor_first_name': visit['visitor_first_name'],
                    'visitor_last_name': visit['visitor_last_name'],
                    'date': visit['date'],
                    'hour': visit['hour'],
                    'lead_id': visit['lead_id']
                }
            )

            for i, page in enumerate(visit['visit_route']):
                visit_routs.append(
                    {
                        'visit_id': visit_id,
                        'page_number': i + 1,
                        'hostname': page['hostname'],
                        'page_path': page['page_path'],
                        'previous_page_path': page['previous_page_path'],
                        'time_on_page': page['time_on_page'],
                        'page_title': page['page_title'],
                        'page_url': page['page_url'],
                        'display_page_name': page['display_page_name'],
                    }
                )
        
        if 'next' not in response['links']:
            log.info("No next page, exiting loop")
            break
        else:
            visit_params['page[number]'] = visit_params['page[number]'] + 1
    return {
        'visits': visits,
        'visit_routs': visit_routs
    }
