from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from crew_pipeline import run_autonomous_crew


from agents.planner import PlannerAgent
from agents.resource import ResourceAgent
from agents.scheduler import SchedulerAgent
from agents.cost_estimator import CostEstimator
from agents.risk_manager import RiskManager
from core.dependency_graph import DependencyGraph
from core.gantt_chart import generate_gantt

app = Flask(__name__)
CORS(app)

planner = PlannerAgent()
resource = ResourceAgent()
scheduler = SchedulerAgent()
cost_estimator = CostEstimator()
risk_manager = RiskManager()
dep_graph = DependencyGraph()


@app.route("/plan", methods=["POST"])
def plan():

    goal = request.json["goal"]

    result = run_autonomous_crew(goal)

    return jsonify({
        "goal": goal,
        **result
    })




@app.route("/gantt.png")
def gantt():
    return send_file("gantt.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
