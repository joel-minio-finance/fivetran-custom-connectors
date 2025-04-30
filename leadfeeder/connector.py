from fivetran_connector_sdk import Connector, Operations as op, Logging as log
from datetime import datetime, timedelta
from utils import fetch_visits, fetch_leads
from state import get_state, update_state
from schema import get_schema

def schema(configuration):
    return get_schema(configuration)



def update_leads(configuration, state):
    yield from sync_records(
        fetch_function= fetch_leads,
        state= state,
        table_to_update= 'raw_leadfeeder__leads',
        configuration= configuration
    )

def update_visits(configuration, state):
    yield from sync_records(
        fetch_function= fetch_visits,
        state= state,
        table_to_update= 'raw_leadfeeder__visits',
        configuration= configuration
    )

def sync_records(configuration, fetch_function, state, table_to_update):
    state_key = f'last_{table_to_update}_sync'
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    start_date_override = configuration.get('start_date_override')
    start_date_from_state = state.get(state_key)
    if not start_date_override:
        start_date = datetime.strptime(start_date_from_state, "%Y-%m-%d").date()
    else:
        start_date = datetime.strptime(start_date_override, "%Y-%m-%d").date()
   

    while start_date <= yesterday:
        log.info(f'Now processing records for {start_date}')

        params = {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': start_date.strftime("%Y-%m-%d"),
            'page[number]': 1,
            'page[size]': int(configuration.get("page_size", 100))
        }
        records_to_upsert = fetch_function(params, configuration)
        if not records_to_upsert:
            log.info('No records to update')
        for table_name, records in records_to_upsert.items():
                log.info(f'Prepping {len(records)} to upsert in {table_name}')
                for record in records:
                    yield op.upsert(
                    table= table_name,
                    data= record
                )

        start_date += timedelta(days=1)
        state = update_state(state, state_key, start_date.strftime("%Y-%m-%d"))
        log.info('updating checkpoint')
        yield op.checkpoint(state)

def update(configuration, state):
    yield from update_visits(configuration, state)
    yield from update_leads(configuration, state)

connector = Connector(schema=schema, update=update)

if __name__ == "__main__":
    import json
    with open("configuration.json", "r") as f:
        configuration = json.load(f)
    connector.debug(configuration=configuration)
