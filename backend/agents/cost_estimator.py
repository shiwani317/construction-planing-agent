from crewai import Agent, LLM
from tools.cost_tool import estimate_cost_time

groq_llm = LLM(model="groq/llama-3.3-70b-versatile")

class CostEstimator:
    def __init__(self):
        self.agent = Agent(
            role="Cost Estimator",
            goal="Estimate cost and time",
            backstory="Construction budgeting expert",
            llm=groq_llm
        )

    def estimate(self, schedule):
        return {t: estimate_cost_time(t) for t in schedule}
