"""
Main Skills Module - Unified interface for all robot skills

This module provides a unified interface to all robot skills across all tiers,
allowing easy access to T0, T1, and T2 skills with proper composition.
"""

import json
from typing import Any, Dict, List, Optional

# Import all skill modules
from skills_tier0 import (
    adjust_gripper,
    align_objects,
    emergency_stop,
    grab_object,
    move,
    pose_estimation,
    vlm_assert,
)
from skills_tier1 import (
    aspirate,
    discard_tip,
    dispense,
    grab_tip,
    measure_volume,
    mix,
    scan_workspace,
)
from skills_tier2 import (
    load_machine,
    operate_machine_interface,
    plate_processing,
    transfer_liquid,
    unload_machine,
)


class RobotSkills:
    """
    Unified interface for all robot skills with tier-based organization.

    This class provides access to all skills while maintaining the hierarchical
    composition structure defined in the skill compositions.
    """

    def __init__(self, machine_database_path: str = "machine_database.json"):
        """Initialize with machine database for T2 skills."""
        self.machine_database = self._load_machine_database(machine_database_path)

        # Tier 0 (Atomic) Skills
        self.tier0 = {
            "move": move,
            "grab_object": grab_object,
            "align_objects": align_objects,
            "adjust_gripper": adjust_gripper,
            "vlm_assert": vlm_assert,
            "pose_estimation": pose_estimation,
            "emergency_stop": emergency_stop,
        }

        # Tier 1 (Reusable Patterns) Skills
        self.tier1 = {
            "grab_tip": grab_tip,
            "discard_tip": discard_tip,
            "aspirate": aspirate,
            "dispense": dispense,
            "mix": mix,
            "scan_workspace": scan_workspace,
            "measure_volume": measure_volume,
        }

        # Tier 2 (Procedural) Skills
        self.tier2 = {
            "load_machine": load_machine,
            "operate_machine_interface": operate_machine_interface,
            "unload_machine": unload_machine,
            "transfer_liquid": transfer_liquid,
            "plate_processing": plate_processing,
        }

        # All skills combined
        self.all_skills = {**self.tier0, **self.tier1, **self.tier2}

    def _load_machine_database(self, path: str) -> Dict[str, Any]:
        """Load machine database for T2 skills."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Machine database not found at {path}")
            return {}

    def get_skill(self, skill_name: str):
        """Get a skill function by name."""
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
        elif tier == "T2":
            return self.tier2
        else:
            raise ValueError(f"Invalid tier: {tier}. Must be T0, T1, or T2")

    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a skill with given parameters."""
        skill_func = self.get_skill(skill_name)
        return skill_func(**kwargs)

    def get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Get information about a skill including its tier and composition."""
        if skill_name in self.tier0:
            tier = "T0"
            composition = "Atomic - cannot be decomposed"
        elif skill_name in self.tier1:
            tier = "T1"
            composition = "Composed of T0 skills"
        elif skill_name in self.tier2:
            tier = "T2"
            composition = "Composed of T1 and T0 skills"
        else:
            return {"error": f"Skill '{skill_name}' not found"}

        return {
            "name": skill_name,
            "tier": tier,
            "composition": composition,
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
            "tier2_count": len(self.tier2),
            "machine_database_loaded": bool(self.machine_database),
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
    print(f"Available T2 skills: {skills.list_skills('T2')}")
    print()

    # Example: Simple liquid transfer workflow
    print("🔄 Executing liquid transfer workflow...")

    # Step 1: Scan workspace
    scan_result = skills.execute_skill("scan_workspace", scan_resolution=1.0)
    print(f"Scan result: {scan_result['success']}")
    if not scan_result["success"]:
        print(f"Error: {scan_result['error']}")

    # Step 2: Grab tip
    tip_result = skills.execute_skill(
        "grab_tip", pipette_id="pipette_1", tip_type="p200"
    )
    print(f"Grab tip result: {tip_result['success']}")
    if not tip_result["success"]:
        print(f"Error: {tip_result['error']}")

    # Step 3: Aspirate liquid
    aspirate_result = skills.execute_skill(
        "aspirate", pipette_id="pipette_1", volume=50.0, source_position="A1"
    )
    print(f"Aspirate result: {aspirate_result['success']}")
    if not aspirate_result["success"]:
        print(f"Error: {aspirate_result['error']}")

    # Step 4: Dispense liquid
    dispense_result = skills.execute_skill(
        "dispense", pipette_id="pipette_1", volume=50.0, target_position="B1"
    )
    print(f"Dispense result: {dispense_result['success']}")
    if not dispense_result["success"]:
        print(f"Error: {dispense_result['error']}")

    # Step 5: Discard tip
    discard_result = skills.execute_skill("discard_tip", pipette_id="pipette_1")
    print(f"Discard tip result: {discard_result['success']}")
    if not discard_result["success"]:
        print(f"Error: {discard_result['error']}")

    print("\n✅ Workflow completed successfully!")


def example_machine_workflow():
    """Example of machine-based workflow using T2 skills."""
    print("\n🏭 MACHINE WORKFLOW EXAMPLE")
    print("=" * 50)

    skills = create_skill_executor()

    # Example: Load sample into centrifuge
    print("🔄 Loading sample into centrifuge...")

    load_result = skills.execute_skill(
        "load_machine", machine_id="centrifuge_1", sample_id="sample_001"
    )
    print(f"Load result: {load_result['success']}")
    if not load_result["success"]:
        print(f"Error: {load_result['error']}")

    # Operate machine interface
    interface_result = skills.execute_skill(
        "operate_machine_interface", machine_id="centrifuge_1", operation="close_door"
    )
    print(f"Interface result: {interface_result['success']}")
    if not interface_result["success"]:
        print(f"Error: {interface_result['error']}")

    # Unload sample
    unload_result = skills.execute_skill(
        "unload_machine", machine_id="centrifuge_1", sample_id="sample_001"
    )
    print(f"Unload result: {unload_result['success']}")
    if not unload_result["success"]:
        print(f"Error: {unload_result['error']}")

    print("\n✅ Machine workflow completed successfully!")


if __name__ == "__main__":
    # Run examples
    example_workflow()
    example_machine_workflow()

    # Show skill statistics
    skills = create_skill_executor()
    stats = skills.get_skill_statistics()
    print(f"\n📊 SKILL STATISTICS")
    print(f"Total skills: {stats['total_skills']}")
    print(f"T0 skills: {stats['tier0_count']}")
    print(f"T1 skills: {stats['tier1_count']}")
    print(f"T2 skills: {stats['tier2_count']}")
    print(f"Machine database loaded: {stats['machine_database_loaded']}")
