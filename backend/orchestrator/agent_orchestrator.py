
import json

from backend.schemas.agent_decision import AgentDecision
from backend.llm.prompts import AGENT_LOOP_INSTRUCTIONS


class AgentOrchestrator:

    def __init__(
            self,
            llm_client,
            action_executor,
            max_iterations=5
    ):

        self.llm_client = llm_client

        self.action_executor = action_executor

        self.max_iterations = max_iterations

    def run(self, user_task):

        if not user_task or not user_task.strip():
            raise ValueError("User task cannot be empty")

        observations = []

        execution_history = []

        for iteration in range(1, self.max_iterations + 1):

            print(f"\n--- Agent Iteration {iteration} ---")

            # Step 1: Send task and previous observations to LLM

            observation_context = json.dumps(observations)

            llm_result = self.llm_client.get_agent_decision(

                user_input=user_task,

                observation=observation_context,

                decision_schema=AgentDecision,

                instructions=AGENT_LOOP_INSTRUCTIONS
            )

            decision = llm_result["data"]

            if not isinstance(decision, AgentDecision):
                decision = AgentDecision.model_validate(decision)

            print("Action:", decision.action)

            print("Reason:", decision.reason)

            # Step 2: Check for task completion

            if decision.action == "finish":

                if decision.status != "completed":
                    raise ValueError(
                        "Finish action must have completed status"
                    )

                return {
                    "status": "completed",
                    "answer": decision.reason,
                    "iterations": iteration,
                    "observations": observations,
                    "execution_history": execution_history
                }

            if decision.status != "continue":
                raise ValueError(
                    "Non-finish actions must have continue status"
                )

            # Step 3: Execute the requested action

            observation = self.action_executor.execute(
                decision
            )

            # Step 4: Save the observation

            observations.append({
                "iteration": iteration,
                "action": decision.action,
                "result": observation
            })

            execution_history.append(
                decision.model_dump()
            )

            print("Observation:", observation)

        # Step 5: Stop when maximum iterations are reached

        return {
            "status": "max_iterations_reached",
            "answer": "Agent stopped because the iteration limit was reached.",
            "iterations": self.max_iterations,
            "observations": observations,
            "execution_history": execution_history
        }
