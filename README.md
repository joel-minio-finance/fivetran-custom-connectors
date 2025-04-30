
# Leadfeeder Fivetran Connector

This repository contains a custom Fivetran connector for syncing data from Leadfeeder. It fetches visits, leads, locations, and associated information, processes the data, and upserts it usings Fivetran's sdk.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [How it Works](#how-it-works)
6. [Usage](#usage)
7. [Schema](#schema)
8. [Logging](#logging)
9. [Error Handling](#error-handling)
10. [License](#license)

## Overview

This Fivetran connector integrates with Leadfeeder, a B2B lead generation platform. The connector fetches data from Leadfeeder's API, processes it, and syncs the data to the appropriate tables within a data warehouse. 

The connector handles the following tasks:
- Fetching visit data from Leadfeeder and syncing it into the `raw_leadfeeder__visits` table.
- Fetching lead data and syncing it into the `raw_leadfeeder__leads` table.
- Handling location data and syncing it into the `raw_leadfeeder__locations` table.
- Storing visit routes (page paths and visit details) into the `raw_leadfeeder__visit_routs` table as a child record.
  
It also manages pagination to handle large data sets by iterating through pages of results.

information on leadfeeders apis can be found here: https://docs.leadfeeder.com/api/#introduction

## Prerequisites

- Python 3.8+
- `pip` for Python package management
- Fivetran custom connector SDK
- Leadfeeder API token and account ID (See [configuration](#configuration) below for details)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/leadfeeder-fivetran-connector.git
   cd leadfeeder-fivetran-connector
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

To configure the connector, you need to set up a `configuration.json` file with the following fields:

- `LEADFEEDER_API_TOKEN`: Your Leadfeeder API token.
- `LEADFEEDER_ACCOUNT_ID`: Your Leadfeeder account ID.
- `LEADFEEDER_BASE_API_URL`: The base URL of the Leadfeeder API (default is `https://api.leadfeeder.com`).
- `start_date_override`: Optional. The start date for syncing. If not provided, defaults to `2024-01-01`.
- `page_size`: The number of records per page (default is `100`).

Example `configuration.json`:

```json
{
  "start_date_override": "2025-04-26",
  "page_size": "100",
  "LEADFEEDER_API_TOKEN": "your_api_token_here",
  "LEADFEEDER_ACCOUNT_ID": "your_account_id_here",
  "LEADFEEDER_BASE_API_URL": "https://api.leadfeeder.com"
}
```

## How it Works

The connector is divided into multiple Python modules for handling various tasks:

- **`connector.py`**: Main file that defines the connector's schema and update logic. It uses the Fivetran Connector SDK to manage the sync process.
- **`utils.py`**: Contains functions for fetching data from the Leadfeeder API. It handles retries and pagination.
- **`state.py`**: Manages the state of the connector, including tracking the last sync date to prevent redundant data fetching.
- **`schema.py`**: Defines the structure of the tables that will be synced with Fivetran.
- **`constants.py`**: Contains constants such as the API URL and account ID.

### Data Sync Process

1. The `update_visits` and `update_leads` functions call `sync_records`, which:
   - Fetches data from Leadfeeder for the given date range.
   - Iterates through pages of results (pagination).
   - Processes the `visit_route` data into child records.
   
2. Data is then upserted into the following tables:
   - `raw_leadfeeder__visits`
   - `raw_leadfeeder__leads`
   - `raw_leadfeeder__locations`
   - `raw_leadfeeder__visit_routs` (child records)

3. The `update_state` function updates the sync timestamp for each table to keep track of where the connector left off.

## Usage

1. Ensure your `configuration.json` is properly set up with your Leadfeeder credentials.
2. Run the connector:
   ```bash
   python connector.py
   ```

This will start the syncing process and process the records in batches according to the configuration.

## Schema

The connector defines the following schema for syncing data:

- **`raw_leadfeeder__visits`**: Contains visit information such as source, medium, referring URL, visit length, etc.
- **`raw_leadfeeder__leads`**: Contains lead information including name, contact details, employee count, and associated industries.
- **`raw_leadfeeder__visit_routs`**: Stores the visit route data for each visit (page path, time on page, etc.), acting as a child record linked to `visit_id`.
- **`raw_leadfeeder__locations`**: Contains location data associated with leads.

Schema definitions are located in the `schema.py` file, which defines the columns, primary keys, and field types.

## Logging

Logging is managed using the `Logging` module from the Fivetran Connector SDK. You can view detailed logs of the sync process, including pagination, data processing, and any errors encountered during the sync.

Log entries are printed to the console, and you can adjust the logging level as needed in the code.

## Error Handling

The connector includes basic error handling:

- If an API request fails, it retries the request up to 5 times with exponential backoff.
- If a `KeyError` occurs (due to missing fields), the connector will log a warning and continue processing the remaining records.
