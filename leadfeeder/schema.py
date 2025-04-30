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
                "ga_client_ids": "string",
                "country_code": "string",
                "device_type": "string",
                "visitor_email": "string",
                "visitor_first_name": "string",
                "visitor_last_name": "string",
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
        },
        {
            "table": "raw_leadfeeder__leads",
            "primary_key": ["lead_id"],
            "columns": {
                "lead_id": "string",
                "name": "string",
                "first_visit_date": "string",
                "last_visit_date": "string",
                "website_url": "string",
                "linkedin_url": "string",
                "twitter_handle": "string",
                "facebook_url": "string",
                "employee_count": "int",
                "employees_range_min": "int",
                "employees_range_max": "int",
                "crm_lead_id": "string",
                "crm_organization_id": "string",
                "tags": "string",
                "logo_url": "string",
                "business_id": "string",
                "revenue": "string",
                "view_in_leadfeeder": "string",
                "quality": "int",
                "industries": "string",
                "location_id": "string"
            }
        },
        {
            "table": "raw_leadfeeder__locations",
            "primary_key": ["location_id"],
            "columns": {
                "location_id": "string",
                "country": "string",
                "country_code": "string",
                "region": "string",
                "region_code": "string",
                "city": "string",
                "state_code": "string"
            }
        }
    ]
