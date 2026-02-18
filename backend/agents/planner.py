from crewai import Agent, LLM
import json

# Groq LLM configuration
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.2
)


class PlannerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Construction Planner",
            goal="Generate a detailed construction execution plan with tasks and dependencies",
            backstory=(
                "You are an expert construction project planner with experience "
                "in residential and commercial construction planning."
            ),
            llm=groq_llm,
            verbose=False
        )

    def run(self, goal):
        """
        Uses Groq LLM to generate a detailed task list with dependencies
        """

        prompt = f"""
Create a VERY DETAILED construction project plan for the goal below.

GOAL:
{goal}

INSTRUCTIONS:
- Return ONLY valid JSON
- Do NOT add explanation or markdown
- Include 25 to 40 tasks
- Cover phases:
  Planning, Site Preparation, Foundation, Structure,
  Electrical, Plumbing, HVAC, Finishing, Inspection
- Each task must include:
  - "task": string
  - "depends_on": list of previous task names
- First task MUST have empty depends_on list

FORMAT:
[
  {{
    "task": "Task name",
    "depends_on": []
  }}
]
"""

        try:
            # Call Groq LLM correctly
            response = groq_llm.call(prompt)

            # Clean JSON from response (Groq sometimes adds text)
            start = response.find("[")
            end = response.rfind("]") + 1
            json_str = response[start:end]

            tasks = json.loads(json_str)

            # Validate structure
            for t in tasks:
                if "task" not in t or "depends_on" not in t:
                    raise ValueError("Invalid task structure")

            return tasks

        except Exception as e:
            print("⚠ Planner fallback used due to error:", e)

            # SAFE FALLBACK (always works)
            return [
                {"task": "Project planning and budgeting", "depends_on": []},
                {"task": "Land survey and soil testing", "depends_on": ["Project planning and budgeting"]},
                {"task": "Architectural design and drawings", "depends_on": ["Land survey and soil testing"]},
                {"task": "Permit and approval acquisition", "depends_on": ["Architectural design and drawings"]},
                {"task": "Site clearing and fencing", "depends_on": ["Permit and approval acquisition"]},
                {"task": "Excavation work", "depends_on": ["Site clearing and fencing"]},
                {"task": "Foundation footing construction", "depends_on": ["Excavation work"]},
                {"task": "Foundation concrete pouring", "depends_on": ["Foundation footing construction"]},
                {"task": "Foundation curing and inspection", "depends_on": ["Foundation concrete pouring"]},
                {"task": "Structural column construction", "depends_on": ["Foundation curing and inspection"]},
                {"task": "Beam and slab construction", "depends_on": ["Structural column construction"]},
                {"task": "Wall masonry work", "depends_on": ["Beam and slab construction"]},
                {"task": "Roof structure construction", "depends_on": ["Wall masonry work"]},
                {"task": "Electrical conduit installation", "depends_on": ["Wall masonry work"]},
                {"task": "Plumbing pipe installation", "depends_on": ["Wall masonry work"]},
                {"task": "HVAC duct installation", "depends_on": ["Wall masonry work"]},
                {"task": "Internal plastering", "depends_on": ["Electrical conduit installation", "Plumbing pipe installation"]},
                {"task": "External plastering", "depends_on": ["Roof structure construction"]},
                {"task": "Flooring work", "depends_on": ["Internal plastering"]},
                {"task": "Door and window installation", "depends_on": ["Internal plastering"]},
                {"task": "Electrical wiring and fixtures", "depends_on": ["Internal plastering"]},
                {"task": "Plumbing fixtures installation", "depends_on": ["Internal plastering"]},
                {"task": "Painting and finishing", "depends_on": ["Flooring work"]},
                {"task": "Final electrical inspection", "depends_on": ["Electrical wiring and fixtures"]},
                {"task": "Final plumbing inspection", "depends_on": ["Plumbing fixtures installation"]},
                {"task": "Overall quality inspection", "depends_on": ["Painting and finishing"]},
                {"task": "Site cleanup", "depends_on": ["Overall quality inspection"]},
                {"task": "Project handover", "depends_on": ["Site cleanup"]}
            ]
