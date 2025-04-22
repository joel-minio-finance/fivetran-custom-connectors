from fivetran_connector_sdk import Connector, Operations as op, Logging as log

def schema(configuration):
    print("✅ schema() called")
    return [
        {
            "table": "test_table",
            "primary_key": ["id"],
            "columns": {
                "id": "int",
                "message": "string"
            }
        }
    ]

def update(configuration, state):
    print("✅ update() called")
    # This is mock data — replace with your API call later
    yield op.upsert(
        table="test_table",
        data={"id": 1, "message": "Hello from Fivetran connector!"}
    )

    # Yield a checkpoint so Fivetran saves progress
    yield op.checkpoint(state)

connector = Connector(schema=schema, update=update)

if __name__ == "__main__":
    import json
    with open("configuration.json", "r") as f:
        configuration = json.load(f)
    connector.debug(configuration=configuration)
