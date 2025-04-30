import requests
from fivetran_connector_sdk import Logging as log
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json


session = requests.Session()
retry_strategy = Retry(
    total=5,                 
    backoff_factor=2,         
    status_forcelist=[429, 500, 502, 503, 504], 
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

def fetch_data(endpoint, params, configuration):
    headers = {
        "Authorization": f"Token token={configuration.get('LEADFEEDER_API_TOKEN')}",
        "User-Agent": "FivetranConnector/1.0",
    }
    url = f"{configuration.get('LEADFEEDER_BASE_API_URL')}/{endpoint}"

    try:
        response = session.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        log.info(f"HTTP error calling {url}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        log.info(f"Request failed calling {url}: {e}")
        raise

def fetch_visits(params, configuration):
    visit_params = params.copy()
    visits = []
    visit_routs = []
    VISITS_ENDPOINT = f'/accounts/{configuration.get("LEADFEEDER_ACCOUNT_ID")}/visits'
    
    while True:
        response = fetch_data(VISITS_ENDPOINT, visit_params, configuration)

        if 'data' not in response or not response['data']:
            log.info("Reponse has no data, exiting loop")
            break
        
        log.info(f"fetched {len(response['data'])} for page {visit_params['page[number]']} for visits call")

        for item in response['data']:
            visit_id = item['id']
            visit = item['attributes']
            # fivetran can not accept lists. Lists must be converted to strings
            if isinstance(visit["ga_client_ids"], list):
                visit["ga_client_ids"] = ", ".join(visit["ga_client_ids"])
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
                    'ga_client_ids': visit['ga_client_ids'],
                    'country_code': visit['country_code'],
                    'device_type': visit['device_type'],
                    'visitor_email': visit['visitor_email'],
                    'visitor_first_name': visit['visitor_first_name'],
                    'visitor_last_name': visit['visitor_last_name'],
                    'lead_id': visit['lead_id'],
                }
            )
            for index, element in enumerate(visit.get('visit_route',[])):
                visit_routs.append({
                    'visit_id': visit_id,
                    'page_number': index + 1,
                    'hostname': element['hostname'],
                    'page_path': element['page_path'],
                    'previous_page_path': element['previous_page_path'],
                    'time_on_page': element['time_on_page'],
                    'page_title': element['page_title'],
                    'page_url': element['page_url'],
                    'display_page_name': element['display_page_name'],
                })
        
        if not response.get('links', {}).get('next'):
            log.info("No next page, exiting loop")
            break
        else:
            visit_params['page[number]'] += 1
    log.info(f'{len(visits)} visits and {len(visit_routs)} visit routs fetched sending them to be synced')
    return {
        'raw_leadfeeder__visits': visits,
        'raw_leadfeeder__visit_routs': visit_routs
    }


def fetch_leads(params, configuration):
    leads_params = params.copy()
    leads = []
    locations = []
    LEADS_ENDPOINT = f'/accounts/{configuration.get("LEADFEEDER_ACCOUNT_ID")}/leads'
    
    while True:
        response = fetch_data(LEADS_ENDPOINT, leads_params, configuration)

        if 'data' not in response or not response['data']:
            log.info("Reponse has no data, exiting loop")
            break
        
        log.info(f"fetched {len(response['data'])} for page {leads_params['page[number]']} for leads call")

        for item in response['data']:
            lead_id = item['id']
            lead = item['attributes']
            # fivetran can not accept lists. Lists must be converted to strings
            if isinstance(lead["tags"], list):
                lead["tags"] = ", ".join(lead["tags"])
            leads.append(
                {
                    'lead_id': lead_id,
                    'name': lead['name'],
                    'industries': [i.get('name') for i in lead.get('industries', [])] if lead.get('industries') else None,
                    'first_visit_date': lead['first_visit_date'],
                    'last_visit_date': lead['last_visit_date'],
                    'website_url': lead['website_url'],
                    'linkedin_url': lead['linkedin_url'],
                    'twitter_handle': lead['twitter_handle'],
                    'facebook_url': lead['facebook_url'],
                    'employee_count': lead['employee_count'],
                    'employees_range_min': lead['employees_range']['min'],
                    'employees_range_max': lead['employees_range']['max'],
                    'crm_lead_id': lead['crm_lead_id'],
                    'crm_organization_id': lead['crm_organization_id'],
                    'tags':lead['tags'],
                    'logo_url': lead['logo_url'],
                    'business_id': lead['business_id'],
                    'revenue': lead['revenue'],
                    'view_in_leadfeeder': lead['view_in_leadfeeder'],
                    'quality': lead['quality'],
                    'location_id': item.get('relationships',{}).get('location',{}).get('data',{}).get('id')
                }
            )

        for item in response.get('included',[]):
            location_id = item['id']
            location = item['attributes']
            locations.append({
                'location_id': location_id,
                'country': location['country'],
                'country_code': location['country_code'],
                'region': location['region'],
                'region_code': location['region_code'],
                'city': location['city'],
                'state_code': location['state_code'],
            })
        
        if not response.get('links', {}).get('next'):
            log.info("No next page, exiting loop")
            break
        else:
            leads_params['page[number]'] += 1
    
    log.info(f"Fetched total {len(leads)} leads and {len(locations)} locations.")
    return {
        'raw_leadfeeder__locations': locations,
        'raw_leadfeeder__leads': leads
    }
