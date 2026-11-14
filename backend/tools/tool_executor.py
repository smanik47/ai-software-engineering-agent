
class ToolExecutor:

    def __init__(self, filesystem_tools):
        self.filesystem_tools = filesystem_tools

        # Tool registry: action name -> Python function
        self.tool_registry = {
            "list_directory": self.filesystem_tools.list_directory,
            "read_file": self.filesystem_tools.read_file,
            "search_code": self.filesystem_tools.search_code,
            "write_file": self.filesystem_tools.write_file
        }

    def execute(self, decision):

        action = decision.action
        arguments = decision.arguments

        if action not in self.tool_registry:
            raise ValueError(f"Unsupported action: {action}")

        tool_function = self.tool_registry[action]

        try:
            result = tool_function(**arguments)

            return {
                "status": "success",
                "action": action,
                "result": result
            }

        except (ValueError, OSError, TypeError) as exc:
            return {
                "status": "error",
                "action": action,
                "message": str(exc)
            }
