# Jinja2 Matrix Filters

## Overview

Jinja2 Matrix Filters is a functionality extension to handle matrix data.

### Included filters

- user_bridge_info
- user_bridge_prefix
- user_bridge_account_id
- user_homeserver
- location_message_geo_uri
- location_message_latitude
- location_message_longitude
- google_location_url

## Install

`pip install jinja2-matrix-filters`

## Usage

### Typical usage with jinja2

```python
  from jinja2 import Environment

...
  env = Environment(extensions=['jinja2_matrix_filters.MatrixFiltersExtension'])
...
# OR
  from jinja2_matrix_filters import MatrixFiltersExtension
  env = Environment(extensions=[MatrixFiltersExtension])
...
```

### Include into cookiecutter

cookiecutter.json

```json
{
  "_extensions": ["jinja2_matrix_filters.MatrixFiltersExtension"]
}
```
