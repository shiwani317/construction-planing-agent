from agents.planner import PlannerAgent
from agents.resource import ResourceAgent
from agents.scheduler import SchedulerAgent
from agents.cost_estimator import CostEstimator
from agents.risk_manager import RiskManager
from core.dependency_graph import DependencyGraph

planner = PlannerAgent()
resource = ResourceAgent()
scheduler = SchedulerAgent()
cost_estimator = CostEstimator()
risk_manager = RiskManager()
dep_graph = DependencyGraph()


def run_autonomous_crew(goal):

    # ---------------- 1. TASK DECOMPOSITION ----------------
    tasks = planner.run(goal)

    task_decomposition = []
    for i, t in enumerate(tasks, 1):
        task_decomposition.append({
            "step": i,
            "task": t["task"],
            "depends_on": t["depends_on"]
        })

    # ---------------- 2. DEPENDENCY MANAGEMENT ----------------
    graph = dep_graph.build(tasks)
    dependencies = list(graph.edges())

    dependency_details = []
    for d in dependencies:
        dependency_details.append({
            "task": d[1],
            "depends_on": d[0],
            "explanation": f"{d[1]} can start only after completion of {d[0]}"
        })

    # ---------------- 3. RESOURCE VALIDATION ----------------
    valid, delayed = resource.validate(tasks)

    resource_report = []
    for t in tasks:
        status = "Available" if t["task"] in valid else "Delayed"
        resource_report.append({
            "task": t["task"],
            "labor": ["Engineer", "Skilled Labor"],
            "materials": ["Concrete", "Steel", "Tools"],
            "equipment": ["Excavator", "Mixer"],
            "status": status
        })

    # ---------------- 4. EXECUTION SCHEDULE ----------------
    schedule = scheduler.schedule(graph, valid)

    schedule_report = []
    for i, s in enumerate(schedule, 1):
        schedule_report.append({
            "order": i,
            "task": s,
            "description": f"Execute {s} in scheduled sequence"
        })

    # ---------------- 5. COST & TIME ESTIMATION ----------------
    estimates = cost_estimator.estimate(schedule)

    cost_time_report = []
    for t in schedule:
        cost_time_report.append({
            "task": t,
            "days": estimates[t]["days"],
            "cost": estimates[t]["cost"],
            "note": f"{t} expected to take {estimates[t]['days']} days with estimated cost {estimates[t]['cost']}"
        })

    # ---------------- 6. RISK ANALYSIS ----------------
    risk_text = risk_manager.recover(delayed)

    risk_report = []
    if delayed:
        for d in delayed:
            risk_report.append({
                "task": d,
                "risk": "Delay due to resource constraint",
                "mitigation": "Allocate backup resources / adjust schedule"
            })
    else:
        risk_report.append({
            "task": "Project",
            "risk": "No major risks detected",
            "mitigation": "Proceed with current plan"
        })

    # ---------------- 7. CHECKLIST ----------------
    checklist = []
    for t in tasks:
        checklist.append({
            "task": t["task"],
            "status": "Pending"
        })

    # ---------------- FINAL DETAILED OUTPUT ----------------
    return {
        "task_decomposition": task_decomposition,
        "dependencies": dependency_details,
        "resource_validation": resource_report,
        "execution_schedule": schedule_report,
        "cost_time": cost_time_report,
        "risk_analysis": risk_report,
        "checklist": checklist
    }
