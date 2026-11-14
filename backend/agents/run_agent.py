
from backend.llm.llm_client import LLMClient

from backend.tools.demo_action_executor import DemoActionExecutor

from backend.orchestrator.agent_orchestrator import AgentOrchestrator


def main():

    # Step 1: Initialize LLM client

    llm_client = LLMClient()

    # Step 2: Initialize action executor

    action_executor = DemoActionExecutor()

    # Step 3: Initialize orchestrator

    agent = AgentOrchestrator(

        llm_client=llm_client,

        action_executor=action_executor,

        max_iterations=5
    )

    # Step 4: Submit task

    result = agent.run(

        user_task="""
        Understand this sample Spring Boot repository.

        Inspect the repository.
        Read UserController.java and UserService.java.
        Explain the responsibility of both classes.
        """
    )

    # Step 5: Display final result

    print("\n========== FINAL RESULT ==========")

    print("Status:", result["status"])

    print("Answer:", result["answer"])

    print("Iterations:", result["iterations"])

    print("\nExecution History:")

    for item in result["execution_history"]:
        print(item)


if __name__ == "__main__":
    main()
