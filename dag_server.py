"""
DAG Visualization Server

This server provides a REST API for the skill DAG visualizer and serves
the web interface for exploring robot skill compositions.
"""

import json
import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from skill_composition_analyzer import create_skill_analyzer

app = Flask(__name__)
CORS(app)

# Global variables for skill data
analyzer = None
skills_registry = None


def initialize_skills():
    """Initialize the skill analyzer and registry."""
    global analyzer, skills_registry
    try:
        analyzer, skills_registry = create_skill_analyzer()
        print("✅ Skills initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing skills: {e}")
        analyzer = None
        skills_registry = None


@app.route("/")
def index():
    """Serve the main DAG visualizer page."""
    try:
        # Try to serve the standalone visualizer first (no backend required)
        if os.path.exists("standalone_dag_visualizer.html"):
            with open("standalone_dag_visualizer.html", "r") as f:
                return f.read()
        # Fallback to enhanced visualizer
        elif os.path.exists("enhanced_dag_visualizer.html"):
            with open("enhanced_dag_visualizer.html", "r") as f:
                return f.read()
        # Fallback to basic visualizer
        elif os.path.exists("dag_visualizer.html"):
            with open("dag_visualizer.html", "r") as f:
                return f.read()
        else:
            return "DAG visualizer HTML file not found", 404
    except Exception as e:
        return f"Error loading visualizer: {str(e)}", 500


@app.route("/api/skills/dag")
def get_dag_data():
    """Get the complete DAG data for visualization."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        dag_data = analyzer.export_dag_data()
        return jsonify(dag_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/skills/<skill_name>")
def get_skill_details(skill_name):
    """Get detailed information about a specific skill."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        # Get skill hierarchy
        hierarchy = analyzer.get_skill_hierarchy(skill_name)

        # Get dependencies
        dependencies = analyzer.get_skill_dependencies(skill_name)

        # Get usage (what skills use this skill)
        usage = analyzer.get_skill_usage(skill_name)

        # Get execution order
        execution_order = analyzer.get_execution_order(skill_name)

        return jsonify(
            {
                "name": skill_name,
                "tier": analyzer.skill_tiers.get(skill_name, "Unknown"),
                "hierarchy": hierarchy,
                "dependencies": dependencies,
                "usage": usage,
                "execution_order": execution_order,
                "subskills": analyzer.composition_graph.get(skill_name, []),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/skills/<skill_name>/composition")
def get_skill_composition(skill_name):
    """Get the composition breakdown for a skill."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        subskills = analyzer.composition_graph.get(skill_name, [])
        composition = []

        for subskill in subskills:
            subskill_info = {
                "name": subskill,
                "tier": analyzer.skill_tiers.get(subskill, "Unknown"),
                "subskills": analyzer.composition_graph.get(subskill, []),
            }
            composition.append(subskill_info)

        return jsonify(
            {
                "skill": skill_name,
                "tier": analyzer.skill_tiers.get(skill_name, "Unknown"),
                "composition": composition,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/skills/<skill_name>/execution-path")
def get_execution_path(skill_name):
    """Get the complete execution path for a skill."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        execution_order = analyzer.get_execution_order(skill_name)

        # Build execution path with details
        path = []
        for skill in execution_order:
            skill_info = {
                "name": skill,
                "tier": analyzer.skill_tiers.get(skill, "Unknown"),
                "subskills": analyzer.composition_graph.get(skill, []),
                "is_atomic": len(analyzer.composition_graph.get(skill, [])) == 0,
            }
            path.append(skill_info)

        return jsonify(
            {"skill": skill_name, "execution_path": path, "total_steps": len(path)}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/skills/statistics")
def get_skill_statistics():
    """Get statistics about the skill composition."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        stats = analyzer.get_skill_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/skills/search")
def search_skills():
    """Search for skills by name or tier."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        query = request.args.get("q", "").lower()
        tier_filter = request.args.get("tier", "")

        # Filter skills
        filtered_skills = []
        for skill_name, tier in analyzer.skill_tiers.items():
            # Apply tier filter
            if tier_filter and tier != tier_filter:
                continue

            # Apply text search
            if query and query not in skill_name.lower():
                continue

            skill_info = {
                "name": skill_name,
                "tier": tier,
                "subskills": analyzer.composition_graph.get(skill_name, []),
                "usage": analyzer.get_skill_usage(skill_name),
            }
            filtered_skills.append(skill_info)

        return jsonify(
            {
                "query": query,
                "tier_filter": tier_filter,
                "results": filtered_skills,
                "count": len(filtered_skills),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/workflows/create")
def create_workflow():
    """Create a workflow from multiple skills."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        skill_names = request.args.getlist("skills")
        if not skill_names:
            return jsonify({"error": "No skills specified"}), 400

        # Build workflow
        workflow = {
            "skills": skill_names,
            "total_skills": len(skill_names),
            "execution_order": [],
            "dependencies": set(),
            "estimated_time": 0,
        }

        # Collect all dependencies
        for skill in skill_names:
            deps = analyzer.get_skill_dependencies(skill)
            workflow["dependencies"].update(deps)

        workflow["dependencies"] = list(workflow["dependencies"])

        # Build execution order (simplified)
        all_skills = set(skill_names)
        all_skills.update(workflow["dependencies"])
        workflow["execution_order"] = list(all_skills)

        return jsonify(workflow)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/export/dag")
def export_dag():
    """Export the complete DAG data."""
    if not analyzer:
        return jsonify({"error": "Skills not initialized"}), 500

    try:
        dag_data = analyzer.export_dag_data()
        return jsonify(dag_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "skills_initialized": analyzer is not None,
            "total_skills": len(analyzer.skill_tiers) if analyzer else 0,
        }
    )


if __name__ == "__main__":
    # Initialize skills
    initialize_skills()

    print("🚀 Starting DAG Visualization Server...")
    print("📊 Available endpoints:")
    print("  GET  /                    - Main visualizer interface")
    print("  GET  /api/skills/dag      - Complete DAG data")
    print("  GET  /api/skills/<name>   - Skill details")
    print("  GET  /api/skills/statistics - Skill statistics")
    print("  GET  /api/health          - Health check")

    app.run(debug=True, host="0.0.0.0", port=5000)
