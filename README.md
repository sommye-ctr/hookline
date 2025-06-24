# Plugins Definition

### The plugins are required to declare
- config.json
- execution.py which contains execute() function

***
### config.json - 
It represents the basic information of the plugin.

A sample `config.json` looks like:

```json
{
  "name": "Email Sender",
  "description": "Sends an email notification to a specified address.",
  "version": "1.0",
  "author": "Hookline",
  "icon" : "<url to image asset>",
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

`version` - A float number, used to manage upgrades of plugins

`config_schema` - Renders a form whenever a user tries to 
install the plugin. The data which is required by the plugin 
for its functioning can be declared here. 

The `type` is the datatype of the field, `required` marks the field
mandatory and `description` is shown to the user as help text when
filling the form

Supported `type` for the fields are:
1. string
2. integer
3. float
4. bool

> After updating either of the `config.json` or the `execution.py`
you will need to update the version number. Whenever the system 
detects an increment in the version it will show an option to 
update the plugin to the user.

***
### execution.py

Should contain `execute(payload:dict, config:dict)` which is where
the logic of the plugin reside. The function is called with following
arguments
1. `payload` - The payload received from the third-party platform
which caused the workflow to fire up
2. `config` - The user set configuration for the plugin as described
in the 'config_schema' of the `config.json`

The `config` object for the above plugin should look like:
```json
{
  "to" : "someone@domain.com",
  "subject" : "This is a subject",
  "body" : "This is a body"
}
```

> A time limit of **60** seconds is given to each plugin for
> executing all its operation and return the required data. 
> The request is terminated after the given time frame.

***
### Returning Data

The system expects a dict to be returned by the `execute` function.
A sample should look like

```json
{
  "status": "success" | "failed",
  "message": "What happened",
  "output": { ... }  # Optional plugin-specific output
}
```
The `message` and `output` is used for logging purposes and is
visible in logs for that specific workflow.

