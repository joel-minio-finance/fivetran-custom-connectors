def get_state(state):
    return state.get("last_synced", "2024-01-01")

def update_state(state, new_timestamp):
    return { "last_synced": new_timestamp }
