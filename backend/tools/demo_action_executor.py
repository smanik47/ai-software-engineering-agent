
class DemoActionExecutor:

    def __init__(self):

        # Sample repository for Day 3 demonstration.
        self.files = {
            "src/UserController.java": """
                public class UserController {

                    public String getUser() {
                        return "User details";
                    }
                }
            """,

            "src/UserService.java": """
                public class UserService {

                    public String findUser() {
                        return "User found";
                    }
                }
            """
        }

    def execute(self, decision):

        action = decision.action

        arguments = decision.arguments

        if action == "inspect_repository":

            return {
                "status": "success",
                "files": list(self.files.keys()),
                "message": "Repository inspected successfully."
            }

        if action == "read_file":

            path = arguments.get("path")

            if path not in self.files:
                return {
                    "status": "error",
                    "message": f"File not found: {path}"
                }

            return {
                "status": "success",
                "path": path,
                "content": self.files[path]
            }

        raise ValueError(
            f"Unsupported action: {action}"
        )