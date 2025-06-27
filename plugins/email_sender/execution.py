from hookline_sdk.decorators import plugin_version

@plugin_version("1.0.0")
def execute(payload:dict, config:dict):
    print(f"Sending mail to {config.get("to")}")

    return {
        "status": "success",
        "message": "Email sent successfully",
        "status_code": 200,
    }
