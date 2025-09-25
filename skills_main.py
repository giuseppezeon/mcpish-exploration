"""
Main Skills Module - Unified interface for simple robot skills

This module provides a unified interface to simple robot skills (T0 and T1 only),
using the simplified skill definitions from the skills/simple/ folder.
"""

import json
import os
from typing import Any, Dict, List, Optional


class RobotSkills:
    """
    Unified interface for simple robot skills (T0 and T1 only).

    This class loads skill definitions from the skills/simple/ folder and provides
    access to T0 (atomic) and T1 (reusable patterns) skills only.
    """

    def __init__(self, skills_folder: str = "skills/simple"):
        """Initialize with simple skills from the specified folder."""
        self.skills_folder = skills_folder
        self.skill_definitions = self._load_skill_definitions()

        # Organize skills by tier
        self.tier0 = {}
        self.tier1 = {}

        for skill_name, skill_def in self.skill_definitions.items():
            tier = skill_def.get("tier", "T0")
            if tier == "T0":
                self.tier0[skill_name] = skill_def
            elif tier == "T1":
                self.tier1[skill_name] = skill_def

        # All skills combined (T0 and T1 only)
        self.all_skills = {**self.tier0, **self.tier1}

    def _load_skill_definitions(self) -> Dict[str, Any]:
        """Load all skill definitions from the simple skills folder."""
        skill_definitions = {}

        if not os.path.exists(self.skills_folder):
            print(f"Warning: Skills folder not found at {self.skills_folder}")
            return skill_definitions

        for filename in os.listdir(self.skills_folder):
            if filename.endswith(".json"):
                skill_name = filename[:-5]  # Remove .json extension
                file_path = os.path.join(self.skills_folder, filename)

                try:
                    with open(file_path, "r") as f:
                        skill_def = json.load(f)
                        skill_definitions[skill_name] = skill_def
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not load {filename}: {e}")

        return skill_definitions

    def get_skill(self, skill_name: str) -> Dict[str, Any]:
        """Get a skill definition by name."""
        if skill_name in self.all_skills:
            return self.all_skills[skill_name]
        else:
            raise ValueError(f"Skill '{skill_name}' not found")

    def get_skills_by_tier(self, tier: str) -> Dict[str, Any]:
        """Get all skills for a specific tier."""
        if tier == "T0":
            return self.tier0
        elif tier == "T1":
            return self.tier1
        else:
            raise ValueError(f"Invalid tier: {tier}. Must be T0 or T1")

    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """Simulate skill execution with given parameters."""
        skill_def = self.get_skill(skill_name)

        # Simple simulation - in real implementation, this would call actual robot functions
        return {
            "success": True,
            "skill_name": skill_name,
            "tier": skill_def.get("tier", "T0"),
            "execution_time": skill_def.get("timeout_s", 10),
            "parameters": kwargs,
            "message": f"Simulated execution of {skill_name}",
        }

    def get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Get information about a skill including its tier and composition."""
        if skill_name in self.tier0:
            tier = "T0"
            composition = "Atomic - cannot be decomposed"
        elif skill_name in self.tier1:
            tier = "T1"
            composition = "Reusable pattern - composed of T0 skills"
        else:
            return {"error": f"Skill '{skill_name}' not found"}

        skill_def = self.get_skill(skill_name)
        return {
            "name": skill_name,
            "tier": tier,
            "description": skill_def.get("description", ""),
            "composition": composition,
            "timeout_s": skill_def.get("timeout_s", 10),
            "available": True,
        }

    def list_skills(self, tier: Optional[str] = None) -> List[str]:
        """List all available skills, optionally filtered by tier."""
        if tier:
            return list(self.get_skills_by_tier(tier).keys())
        else:
            return list(self.all_skills.keys())

    def get_skill_statistics(self) -> Dict[str, Any]:
        """Get statistics about available skills."""
        return {
            "total_skills": len(self.all_skills),
            "tier0_count": len(self.tier0),
            "tier1_count": len(self.tier1),
            "skills_folder": self.skills_folder,
            "skills_loaded": len(self.skill_definitions),
        }


def create_skill_executor():
    """Create a RobotSkills instance for use in workflows."""
    return RobotSkills()


# Example usage and workflow execution
def example_workflow():
    """Example of how to use the skills in a workflow."""
    print("🤖 ROBOT SKILLS WORKFLOW EXAMPLE")
    print("=" * 50)

    # Create skill executor
    skills = create_skill_executor()

    # Show available skills
    print(f"Available T0 skills: {skills.list_skills('T0')}")
    print(f"Available T1 skills: {skills.list_skills('T1')}")
    print()

    # Example: Simple liquid transfer workflow
    print("🔄 Executing liquid transfer workflow...")

    # Step 1: Grab tip
    tip_result = skills.execute_skill("grab_tip", pipette_id="pipette_1", force=1.0)
    print(f"Grab tip result: {tip_result['success']}")
    if not tip_result["success"]:
        print(f"Error: {tip_result['error']}")

    # Step 2: Aspirate liquid
    aspirate_result = skills.execute_skill(
        "aspirate", pipette_id="pipette_1", volume=50.0, source_position="A1"
    )
    print(f"Aspirate result: {aspirate_result['success']}")
    if not aspirate_result["success"]:
        print(f"Error: {aspirate_result['error']}")

    # Step 3: Dispense liquid
    dispense_result = skills.execute_skill(
        "dispense", pipette_id="pipette_1", volume=50.0, target_position="B1"
    )
    print(f"Dispense result: {dispense_result['success']}")
    if not dispense_result["success"]:
        print(f"Error: {dispense_result['error']}")

    # Step 4: Discard tip
    discard_result = skills.execute_skill("discard_tip", pipette_id="pipette_1")
    print(f"Discard tip result: {discard_result['success']}")
    if not discard_result["success"]:
        print(f"Error: {discard_result['error']}")

    print("\n✅ Workflow completed successfully!")


def example_manipulation_workflow():
    """Example of manipulation workflow using T0 and T1 skills."""
    print("\n🤖 MANIPULATION WORKFLOW EXAMPLE")
    print("=" * 50)

    skills = create_skill_executor()

    # Example: Pick and place workflow
    print("🔄 Executing pick and place workflow...")

    # Step 1: Move to object
    move_result = skills.execute_skill(
        "move",
        rotations={"x": 0, "y": 0, "z": 0},
        translations={"x": 100, "y": 50, "z": 10},
    )
    print(f"Move result: {move_result['success']}")

    # Step 2: Grab object
    grab_result = skills.execute_skill(
        "grab_object",
        object_id="object_001",
        grasp_pose={
            "position": {"x": 100, "y": 50, "z": 10},
            "orientation": {"x": 0, "y": 0, "z": 0},
        },
    )
    print(f"Grab result: {grab_result['success']}")

    # Step 3: Move to target
    move_result2 = skills.execute_skill(
        "move",
        rotations={"x": 0, "y": 0, "z": 0},
        translations={"x": 200, "y": 100, "z": 10},
    )
    print(f"Move to target result: {move_result2['success']}")

    # Step 4: Release object
    release_result = skills.execute_skill("release_object", object_id="object_001")
    print(f"Release result: {release_result['success']}")

    print("\n✅ Manipulation workflow completed successfully!")


if __name__ == "__main__":
    # Run examples
    example_workflow()
    example_manipulation_workflow()

    # Show skill statistics
    skills = create_skill_executor()
    stats = skills.get_skill_statistics()
    print(f"\n📊 SKILL STATISTICS")
    print(f"Total skills: {stats['total_skills']}")
    print(f"T0 skills: {stats['tier0_count']}")
    print(f"T1 skills: {stats['tier1_count']}")
    print(f"Skills folder: {stats['skills_folder']}")
    print(f"Skills loaded: {stats['skills_loaded']}")
