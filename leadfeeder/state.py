from datetime import date, datetime

def get_state(state, key):
    return state.get(key)


def update_state(state, key, new_timestamp):
    if isinstance(new_timestamp, (date, datetime)):
        new_timestamp = new_timestamp.strftime("%Y-%m-%d")
    state[key] = new_timestamp
