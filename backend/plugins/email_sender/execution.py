from hookline_sdk.decorators import plugin_version
from hookline_sdk.registry import HooklinePlugin


class EmailPlugin(HooklinePlugin):

    @plugin_version("1.0.1")
    def execute(self, payload: dict, config: dict):
        print(f"Sending mail to {config.get("to")}")

        return {
            "status": "success",
            "message": "Email sent successfully",
            "status_code": 200,
        }

def create_plugin(version) -> HooklinePlugin:
    return EmailPlugin(version)
