from fivetran_connector_sdk import Connector, Operations as op, Logging as log
from datetime import datetime, timedelta
from utils import fetch_visits
from state import get_state, update_state
from schema import get_schema

def schema(configuration):
    return get_schema(configuration)

def update_visits(configuration, state):
    #for now we will pull data for yesterday. Before going to production we should pull from last date we had a successful post
    today = datetime.today().strftime("%Y-%m-%d")
    params = {
        'start_date': today,
        'end_date': today,
        'page[number]': 1,
        'page[size]': 10
    }

    data = fetch_visits(params)

    log.info(f"Pulled {len(data['visits'])} visits and {len(data['visit_routs'])} visit routes.")

    for visit in data["visits"]:
        yield op.upsert(
            table ='raw_leadfeeder__visits',
            data = visit
        )
    
    for visit_rout in data["visit_routs"]:
        yield op.upsert(
            table ='raw_leadfeeder__visit_routs',
            data = visit_rout
        )

    if not data["visits"] and not data["visit_routs"]:
        log.info("No data pulled. Exiting gracefully.")
        yield op.checkpoint(state)
        return

    yield op.checkpoint(state)

connector = Connector(schema=schema, update=update_visits)

if __name__ == "__main__":
    import json
    with open("configuration.json", "r") as f:
        configuration = json.load(f)
    connector.debug(configuration=configuration)
