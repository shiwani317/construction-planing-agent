def generate_detailed_plan(goal, tasks):

    phases = {
        "Planning": [],
        "Site Preparation": [],
        "Foundation": [],
        "Structure": [],
        "MEP": [],
        "Finishing": [],
        "Inspection": []
    }

    for t in tasks:
        name = t["task"].lower()

        if "permit" in name or "plan" in name:
            phases["Planning"].append(t["task"])
        elif "site" in name or "survey" in name or "excav" in name:
            phases["Site Preparation"].append(t["task"])
        elif "foundation" in name:
            phases["Foundation"].append(t["task"])
        elif "frame" in name or "structure" in name:
            phases["Structure"].append(t["task"])
        elif "electrical" in name or "plumb" in name or "hvac" in name:
            phases["MEP"].append(t["task"])
        elif "paint" in name or "finish" in name:
            phases["Finishing"].append(t["task"])
        else:
            phases["Inspection"].append(t["task"])

    checklist = [t["task"] for t in tasks]

    resources = {
        "materials": [
            "Cement, steel, sand, bricks",
            "Electrical wiring, switches",
            "Plumbing pipes",
            "Paint and tiles"
        ],
        "labor": [
            "Engineers", "Architect", "Labor", "Electricians",
            "Plumbers", "Carpenters", "Painters"
        ],
        "equipment": [
            "Excavator", "Concrete mixer", "Drilling machine",
            "Scaffolding"
        ]
    }

    return {
        "phases": phases,
        "checklist": checklist,
        "resources": resources
    }
