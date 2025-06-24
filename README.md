# Plugin Definition Guide

## Overview

Plugins are required to declare two essential files:
- `config.json` - Plugin metadata and configuration schema
- `execution.py` - Contains the main `execute()` function

---

## config.json

This file represents the basic information and configuration schema of the plugin.

### Sample config.json

```json
{
  "name": "Email Sender",
  "slug": "email_sender",
  "description": "Sends an email notification to a specified address.",
  "version": "1.0",
  "author": "Hookline",
  "icon": "<url to image asset>",
  "config_schema": {
    "to": {
      "type": "string",
      "required": true,
      "description": "Recipient email address"
    },
    "subject": {
      "type": "string",
      "required": true,
      "description": "Email subject"
    },
    "body": {
      "type": "string",
      "required": true,
      "description": "Body of the email. You can use variables like {task_id} or {event_type}"
    }
  }
}
```

### Field Descriptions

- **`slug`** - A snake_case representation of the plugin name
- **`version`** - A single decimal version number (e.g., "1.0", "1.3", "2.1") used to manage plugin upgrades
- **`config_schema`** - Defines the configuration form displayed when users select the plugin for an action

### Configuration Schema Fields

Each field in `config_schema` supports the following properties:

- **`type`** - The data type of the field
- **`required`** - Boolean indicating if the field is mandatory
- **`description`** - Help text shown to users when filling the form

### Supported Data Types

1. `string`
2. `integer`
3. `float`
4. `boolean`

### Version Management

After updating either `config.json` or `execution.py`, you must increment the version number. When the system detects a version increment, it will prompt users with an option to update the plugin.

---

## execution.py

This file must contain an `execute(payload: dict, config: dict)` function where the plugin's main logic resides.

### Function Parameters

1. **`payload`** - The payload received from the third-party platform that triggered the workflow
2. **`config`** - The user-configured settings for the plugin as defined in `config_schema`

### Sample Configuration Object

For the email sender plugin above, the config object would look like:

```json
{
  "to": "someone@domain.com",
  "subject": "This is a subject",
  "body": "This is a body"
}
```

### Execution Constraints

- **Time limit**: 60 seconds maximum execution time per plugin
- **Timeout behavior**: Requests are automatically terminated after the time limit

---

## Return Value Requirements

The `execute` function must return a dictionary with the following structure:

```json
{
  "status": "success" | "failed",
  "message": "Description of what happened",
  "status_code": 200,    // HTTP status code (required)
  "output": { ... }      // Optional: plugin-specific output data
}
```

### Return Fields

- **`status`** - Either "success" or "failed" (required)
- **`message`** - Human-readable description of the execution result (required)
- **`status_code`** - HTTP status code indicating the result type (required)
  - `200` - Success
  - `400` - Bad Request (validation error, invalid input)
  - `401` - Unauthorized (authentication failure)
  - `403` - Forbidden (insufficient permissions)
  - `404` - Not Found (resource not found)
  - `408` - Request Timeout (execution timeout)
  - `422` - Unprocessable Entity (invalid data format)
  - `429` - Too Many Requests (rate limit exceeded)
  - `500` - Internal Server Error (unexpected plugin error)
  - `502` - Bad Gateway (external service error)
  - `503` - Service Unavailable (external service unavailable)
  - `504` - Gateway Timeout (external service timeout)
- **`output`** - Optional dictionary containing plugin-specific output data

The `message` and `output` fields are used for logging purposes and are visible in the workflow logs.

---

## Example Implementation

Here's a complete example of a plugin's `execute` function:

```python
def execute(payload: dict, config: dict) -> dict:
    try:
        # Plugin logic here
        result = send_email(
            to=config['to'],
            subject=config['subject'],
            body=config['body']
        )
        
        return {
            "status": "success",
            "message": "Email sent successfully",
            "status_code": 200,
            "output": {
                "email_id": result.get('id'),
                "sent_at": result.get('timestamp')
            }
        }
    
    except ValidationError as e:
        return {
            "status": "failed",
            "message": f"Validation error: {str(e)}",
            "status_code": 400,
            "output": None
        }
    
    except TimeoutError:
        return {
            "status": "failed",
            "message": "Request timed out",
            "status_code": 408,
            "output": None
        }
    
    except Exception as e:
        return {
            "status": "failed",
            "message": f"Unexpected error: {str(e)}",
            "status_code": 500,
            "output": None
        }
```

### Example Response Formats

Success response:
```json
{
  "status": "success",
  "message": "Email sent successfully",
  "status_code": 200,
  "output": {
    "email_id": "msg_12345",
    "sent_at": "2025-06-24T10:30:00Z"
  }
}
```

Error response:
```json
{
  "status": "failed",
  "message": "Invalid email address format",
  "status_code": 400,
  "output": null
}
```