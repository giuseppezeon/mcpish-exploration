#!/usr/bin/env python3
"""
Skill Hierarchy Visualizer

This script creates visual representations of skill compositions showing how
T1 skills are composed of T0 skills and T2 skills are composed of T1/T0 skills.
"""

import json
import sys
from typing import Any, Dict, List


def load_skill_compositions(file_path: str) -> Dict[str, Any]:
    """Load skill compositions from JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def print_skill_hierarchy(compositions: Dict[str, Any]) -> None:
    """Print a text-based hierarchy of skills."""
    print("=" * 80)
    print("ROBOT SKILL HIERARCHY")
    print("=" * 80)

    # T1 Compositions (T1 -> T0)
    print("\n🔧 TIER 1 SKILLS (Composed of T0 skills)")
    print("-" * 50)

    for skill_name, skill_data in compositions["skill_hierarchies"][
        "T1_compositions"
    ].items():
        print(f"\n📋 {skill_name.upper()}")
        print(f"   Description: {skill_data['description']}")
        print("   Composed of:")

        for step in skill_data["composed_of"]:
            order = step["order"]
            skill = step["skill"]
            params = step.get("parameters", {})
            repeat = step.get("repeat", None)

            param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
            repeat_str = f" (repeats: {repeat})" if repeat else ""

            print(f"     {order}. {skill}({param_str}){repeat_str}")

    # T2 Compositions (T2 -> T1/T0)
    print("\n🏭 TIER 2 SKILLS (Composed of T1/T0 skills)")
    print("-" * 50)

    for skill_name, skill_data in compositions["skill_hierarchies"][
        "T2_compositions"
    ].items():
        print(f"\n📋 {skill_name.upper()}")
        print(f"   Description: {skill_data['description']}")
        print("   Composed of:")

        for step in skill_data["composed_of"]:
            order = step["order"]
            skill = step["skill"]
            params = step.get("parameters", {})
            repeat = step.get("repeat", None)

            param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
            repeat_str = f" (repeats: {repeat})" if repeat else ""

            print(f"     {order}. {skill}({param_str}){repeat_str}")


def print_execution_tree(compositions: Dict[str, Any]) -> None:
    """Print execution trees for complex workflows."""
    print("\n🌳 EXECUTION TREES")
    print("=" * 80)

    for tree_name, tree_data in compositions["execution_trees"].items():
        print(f"\n📊 {tree_name.upper()}")
        print(f"Description: {tree_data['description']}")
        print("\nWorkflow Execution:")

        for i, step in enumerate(tree_data["workflow"], 1):
            print(f"\n  Step {i}: {step['skill']} (Tier {step['tier']})")
            if step.get("parameters"):
                params = ", ".join([f"{k}={v}" for k, v in step["parameters"].items()])
                print(f"    Parameters: {params}")

            print("    Decomposition:")
            for j, action in enumerate(step["decomposition"], 1):
                print(f"      {j}. {action}")


def create_mermaid_diagram(compositions: Dict[str, Any]) -> str:
    """Create a Mermaid diagram showing skill hierarchies."""
    mermaid = ["graph TD"]

    # Add T0 skills (base level)
    t0_skills = [
        "move",
        "grab_object",
        "align_objects",
        "adjust_gripper",
        "vlm_assert",
        "pose_estimation",
        "emergency_stop",
    ]
    for skill in t0_skills:
        mermaid.append(f"    {skill}[{skill}]")

    # Add T1 skills and their connections
    for skill_name, skill_data in compositions["skill_hierarchies"][
        "T1_compositions"
    ].items():
        mermaid.append(f"    {skill_name}[{skill_name}]")
        for step in skill_data["composed_of"]:
            mermaid.append(f"    {step['skill']} --> {skill_name}")

    # Add T2 skills and their connections
    for skill_name, skill_data in compositions["skill_hierarchies"][
        "T2_compositions"
    ].items():
        mermaid.append(f"    {skill_name}[{skill_name}]")
        for step in skill_data["composed_of"]:
            mermaid.append(f"    {step['skill']} --> {skill_name}")

    return "\n".join(mermaid)


def print_skill_statistics(compositions: Dict[str, Any]) -> None:
    """Print statistics about skill usage."""
    print("\n📊 SKILL USAGE STATISTICS")
    print("=" * 80)

    # Count T0 skills used
    t0_usage = {}
    t1_usage = {}

    # Count T0 usage in T1 skills
    for skill_data in compositions["skill_hierarchies"]["T1_compositions"].values():
        for step in skill_data["composed_of"]:
            skill = step["skill"]
            t0_usage[skill] = t0_usage.get(skill, 0) + 1

    # Count T1 usage in T2 skills
    for skill_data in compositions["skill_hierarchies"]["T2_compositions"].values():
        for step in skill_data["composed_of"]:
            skill = step["skill"]
            if skill in compositions["skill_hierarchies"]["T1_compositions"]:
                t1_usage[skill] = t1_usage.get(skill, 0) + 1
            else:
                t0_usage[skill] = t0_usage.get(skill, 0) + 1

    print("\nT0 Skills Usage Count:")
    for skill, count in sorted(t0_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {skill}: {count} times")

    print("\nT1 Skills Usage Count:")
    for skill, count in sorted(t1_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {skill}: {count} times")


def main():
    """Main function to run the skill hierarchy visualizer."""
    if len(sys.argv) > 1:
        compositions_file = sys.argv[1]
    else:
        compositions_file = "skill_compositions.json"

    try:
        compositions = load_skill_compositions(compositions_file)

        print_skill_hierarchy(compositions)
        print_execution_tree(compositions)
        print_skill_statistics(compositions)

        # Create Mermaid diagram
        mermaid_diagram = create_mermaid_diagram(compositions)
        print("\n🎨 MERMAID DIAGRAM")
        print("=" * 80)
        print("Copy this into a Mermaid editor (like mermaid.live):")
        print("\n```mermaid")
        print(mermaid_diagram)
        print("```")

    except FileNotFoundError:
        print(f"Error: Could not find {compositions_file}")
        print("Make sure the skill compositions file exists.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
