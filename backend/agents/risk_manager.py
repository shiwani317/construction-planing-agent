from crewai import Agent, LLM

groq_llm = LLM(model="groq/llama-3.3-70b-versatile")

class RiskManager:
    def __init__(self):
        self.agent = Agent(
            role="Risk Analyst",
            goal="Detect risks",
            backstory="Risk management expert",
            llm=groq_llm
        )

    def recover(self, delayed):
        if not delayed:
            return "No major risks detected."

        msg = "Potential risks:\n"
        for d in delayed:
            msg += f"- Delay risk in {d}\n"

        msg += "Mitigation: allocate backup resources and monitor critical tasks."
        return msg
