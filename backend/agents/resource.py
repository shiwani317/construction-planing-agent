from crewai import Agent, LLM
from tools.resource_tool import check_resources

groq_llm = LLM(model="groq/llama-3.3-70b-versatile")

class ResourceAgent:
    def __init__(self):
        self.agent = Agent(
            role="Resource Manager",
            goal="Validate resources",
            backstory="Ensures availability",
            llm=groq_llm
        )

    def validate(self, tasks):
        valid, delayed = [], []

        for t in tasks:
            if check_resources(t["task"]):
                valid.append(t["task"])
            else:
                delayed.append(t["task"])

        return valid, delayed
