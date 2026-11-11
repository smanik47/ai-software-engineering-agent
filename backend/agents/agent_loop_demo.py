
def call_llm(user_input, tool_result=None):

    """
    Simulates an LLM decision.
    In Day 2, we will replace this with
    an actual OpenAI API call.
    """

    if tool_result is None:

        return {
            "action": "list_directory",
            "arguments": {
                "path": "src"
            }
        }

    return {
        "action": "finish",
        "response": "I have inspected the project."
    }


def list_directory(path):

    """
    Simulates a filesystem tool.
    """

    print(f"Listing directory: {path}")

    return [
        "controller",
        "service",
        "repository"
    ]


def run_agent(user_input):

    tool_result = None

    while True:

        # Step 1: Ask the LLM what to do
        decision = call_llm(
            user_input,
            tool_result
        )

        # Step 2: Check whether the task is complete
        if decision["action"] == "finish":

            print(decision["response"])
            break

        # Step 3: Execute the requested tool
        if decision["action"] == "list_directory":

            tool_result = list_directory(
                decision["arguments"]["path"]
            )


if __name__ == "__main__":

    run_agent(
        "Understand my Spring Boot project"
    )
