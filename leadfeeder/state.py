def get_state(state, key):
    return state.get(key)


def update_state(state, key, new_timestamp):
    update_state = state.copy()
    update_state[key] = new_timestamp
    return update_state
