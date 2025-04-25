def get_schema(configuration):
    return [
        {
            "table": "raw_leadfeeder__visits",
            "primary_key": ["visit_id"],
            "columns": {
                "visit_id": "string",
                "source": "string",
                "medium": "string",
                "referring_url": "string",
                "landing_page_path": "string",
                "keyword": "string",
                "visit_length": "int",
                "started_at": "string",
                "campaign": "string",
                "query_term": "string",
                "lf_client_id": "string",
                "country_code": "string",
                "device_type": "string",
                "visitor_email": "string",
                "visitor_first_name": "string",
                "visitor_last_name": "string",
                "date": "string",
                "hour": "int",
                "lead_id": "string"
            }
        },
        {
            "table": "raw_leadfeeder__visit_routs",
            "primary_key": ["visit_id", "page_number"],
            "columns": {
                "visit_id": "string",
                "page_number": "int",
                "hostname": "string",
                "page_path": "string",
                "previous_page_path": "string",
                "time_on_page": "int",
                "page_title": "string",
                "page_url": "string",
                "display_page_name": "string"
            }
        }
    ]
