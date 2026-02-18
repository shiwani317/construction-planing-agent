from crewai import Agent, LLM
import networkx as nx

groq_llm = LLM(model="groq/llama-3.3-70b-versatile")

class SchedulerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Scheduler",
            goal="Optimize task order",
            backstory="Project scheduling expert",
            llm=groq_llm
        )

    def schedule(self, graph, valid):
        order = list(nx.topological_sort(graph))
        return [t for t in order if t in valid]
