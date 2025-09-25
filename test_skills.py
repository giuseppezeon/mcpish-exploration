#!/usr/bin/env python3
"""
Test script for robot skills execution

This script demonstrates how to use the skill hierarchy system
to execute robot workflows with proper composition.
"""

import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills_main import create_skill_executor


def test_tier0_skills():
    """Test Tier 0 (atomic) skills."""
    print("🔧 TESTING TIER 0 SKILLS")
    print("-" * 40)

    skills = create_skill_executor()

    # Test move
    print("Testing move...")
    move_result = skills.execute_skill(
        "move",
        rotations={"x": 0, "y": 0, "z": 0},
        translations={"x": 100, "y": 200, "z": 50},
    )
    print(f"  Move result: {move_result}")

    # Test grab_object
    print("Testing grab_object...")
    grab_result = skills.execute_skill(
        "grab_object",
        object_id="test_object",
        grasp_pose={
            "position": {"x": 100, "y": 200, "z": 50},
            "orientation": {"x": 0, "y": 0, "z": 0},
        },
    )
    print(f"  Grab result: {grab_result}")

    # Test vlm_assert
    print("Testing vlm_assert...")
    assert_result = skills.execute_skill(
        "vlm_assert", assertion="object_visible", object_id="test_object"
    )
    print(f"  Assert result: {assert_result}")

    print("✅ Tier 0 skills test completed\n")


def test_tier1_skills():
    """Test Tier 1 (reusable patterns) skills."""
    print("🔧 TESTING TIER 1 SKILLS")
    print("-" * 40)

    skills = create_skill_executor()

    # Test grab_tip (composed of move + adjust_gripper + vlm_assert)
    print("Testing grab_tip...")
    tip_result = skills.execute_skill(
        "grab_tip", pipette_id="pipette_1", tip_type="p200"
    )
    print(f"  Grab tip result: {tip_result}")

    # Test aspirate (composed of move + pose_estimation + move + vlm_assert)
    print("Testing aspirate...")
    aspirate_result = skills.execute_skill(
        "aspirate", pipette_id="pipette_1", volume=50.0, source_position="A1"
    )
    print(f"  Aspirate result: {aspirate_result}")

    # Test dispense (composed of move + pose_estimation + move + vlm_assert)
    print("Testing dispense...")
    dispense_result = skills.execute_skill(
        "dispense", pipette_id="pipette_1", volume=50.0, target_position="B1"
    )
    print(f"  Dispense result: {dispense_result}")

    # Test discard_tip (composed of move + adjust_gripper + vlm_assert)
    print("Testing discard_tip...")
    discard_result = skills.execute_skill("discard_tip", pipette_id="pipette_1")
    print(f"  Discard tip result: {discard_result}")

    print("✅ Tier 1 skills test completed\n")


def test_tier2_skills():
    """Test Tier 2 (procedural) skills."""
    print("🏭 TESTING TIER 2 SKILLS")
    print("-" * 40)

    skills = create_skill_executor()

    # Test transfer_liquid (composed of grab_tip + aspirate + dispense + discard_tip)
    print("Testing transfer_liquid...")
    transfer_result = skills.execute_skill(
        "transfer_liquid",
        source_position="A1",
        destination_position="B1",
        volume=50.0,
        pipette_id="pipette_1",
    )
    print(f"  Transfer result: {transfer_result}")

    # Test load_machine (composed of move + grab_object + move + adjust_gripper)
    print("Testing load_machine...")
    load_result = skills.execute_skill(
        "load_machine", machine_id="centrifuge_1", sample_id="sample_001"
    )
    print(f"  Load machine result: {load_result}")

    print("✅ Tier 2 skills test completed\n")


def test_skill_composition():
    """Test skill composition and hierarchy."""
    print("🌳 TESTING SKILL COMPOSITION")
    print("-" * 40)

    skills = create_skill_executor()

    # Show skill information
    print("Skill information:")
    for skill_name in ["move", "grab_tip", "transfer_liquid"]:
        info = skills.get_skill_info(skill_name)
        print(f"  {skill_name}: {info}")

    # Show statistics
    stats = skills.get_skill_statistics()
    print(f"\nSkill statistics: {stats}")

    print("✅ Skill composition test completed\n")


def test_workflow_execution():
    """Test complete workflow execution."""
    print("🔄 TESTING COMPLETE WORKFLOW")
    print("-" * 40)

    skills = create_skill_executor()

    print("Executing liquid transfer workflow...")

    # Step 1: Scan workspace
    scan_result = skills.execute_skill("scan_workspace", scan_resolution=1.0)
    print(f"  Step 1 - Scan workspace: {scan_result['success']}")

    # Step 2: Transfer liquid (this internally uses grab_tip -> aspirate -> dispense -> discard_tip)
    transfer_result = skills.execute_skill(
        "transfer_liquid",
        source_position="A1",
        destination_position="B1",
        volume=100.0,
        pipette_id="pipette_1",
    )
    print(f"  Step 2 - Transfer liquid: {transfer_result['success']}")

    # Step 3: Unload sample
    unload_result = skills.execute_skill(
        "unload_machine", machine_id="centrifuge_1", sample_id="sample_001"
    )
    print(f"  Step 3 - Unload sample: {unload_result['success']}")

    print("✅ Complete workflow test completed\n")


def main():
    """Run all tests."""
    print("🤖 ROBOT SKILLS TEST SUITE")
    print("=" * 50)
    print()

    try:
        # Test each tier
        test_tier0_skills()
        test_tier1_skills()
        test_tier2_skills()

        # Test composition
        test_skill_composition()

        # Test workflow
        test_workflow_execution()

        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
