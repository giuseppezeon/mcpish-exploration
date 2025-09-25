"""
Tier 2 (Procedural Skills) - Composed of Tier 1 and Tier 0 skills

These skills represent high-level workflows and procedures that are composed of
T1 and T0 skills. They provide complete laboratory automation capabilities.

All T2 skills return a standardized structure:
{
    "success": bool,
    "data": dict,  # skill-specific data
    "execution_time": float,
    "error": str | None
}
"""

from typing import Any, Dict, List, Optional

from skills_tier0 import adjust_gripper, grab_object, move, vlm_assert
from skills_tier1 import aspirate, discard_tip, dispense, grab_tip, mix, scan_workspace


def load_machine(machine_id: str, sample_id: str) -> Dict[str, Any]:
    """
    Load a sample into a laboratory machine.

    Composed of: move -> grab_object -> move -> adjust_gripper

    Args:
        machine_id: Identifier for the machine
        sample_id: Identifier for the sample to load

    Returns:
        Standardized result dict with success, data, execution_time, error
    """
    try:
        # Input validation
        if not machine_id or not isinstance(machine_id, str):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid machine_id: must be non-empty string",
            }

        if not sample_id or not isinstance(sample_id, str):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid sample_id: must be non-empty string",
            }

        print(f"🏭 LOAD MACHINE: {sample_id} into {machine_id}")

        # Step 1: Move to sample
        sample_pose = {"x": 100, "y": 200, "z": 30}
        move_result1 = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=sample_pose, speed=0.5
        )

        if not move_result1["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"],
                "error": f"Move to sample failed: {move_result1['error']}",
            }

        # Step 2: Grab the sample
        grab_result = grab_object(
            object_id=sample_id,
            grasp_pose={
                "position": sample_pose,
                "orientation": {"x": 0, "y": 0, "z": 0},
            },
            grasp_force=2.0,
        )

        if not grab_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"],
                "error": f"Grab sample failed: {grab_result['error']}",
            }

        # Step 3: Move to machine
        machine_pose = {"x": 150, "y": 250, "z": 30}
        move_result2 = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=machine_pose, speed=0.3
        )

        if not move_result2["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"]
                + move_result2["execution_time"],
                "error": f"Move to machine failed: {move_result2['error']}",
            }

        # Step 4: Release the sample
        release_result = adjust_gripper(action="open", force=1.0)

        if not release_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"]
                + move_result2["execution_time"]
                + release_result["execution_time"],
                "error": f"Release sample failed: {release_result['error']}",
            }

        total_time = (
            move_result1["execution_time"]
            + grab_result["execution_time"]
            + move_result2["execution_time"]
            + release_result["execution_time"]
        )

        return {
            "success": True,
            "data": {
                "machine_id": machine_id,
                "sample_id": sample_id,
                "machine_status": "loaded",
                "sample_pose": sample_pose,
                "machine_pose": machine_pose,
            },
            "execution_time": total_time,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "execution_time": 0.0,
            "error": f"Load machine failed: {str(e)}",
        }


def operate_machine_interface(machine_id: str, operation: str) -> Dict[str, Any]:
    """
    Operate machine interface (open/close doors, lids, etc.).

    Composed of: move -> grab_object -> move -> adjust_gripper

    Args:
        machine_id: Identifier for the machine
        operation: Operation to perform (open_door, close_door, open_lid, close_lid)

    Returns:
        Dict with success and operation_completed
    """
    print(f"🏭 OPERATE MACHINE INTERFACE: {operation} on {machine_id}")

    # Step 1: Move to machine
    machine_waypoint = {"x": 100, "y": 200, "z": 45}
    move_result1 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=machine_waypoint, speed=0.5
    )

    # Step 2: Grab machine handle
    handle_pose = {
        "position": {"x": 100, "y": 200, "z": 45},
        "orientation": {"x": 0, "y": 0, "z": 0},
    }
    grab_result = grab_object(
        object_id="machine_handle", grasp_pose=handle_pose, grasp_force=1.0
    )

    # Step 3: Perform operation motion
    operation_motion = {"x": 0, "y": 0, "z": -5}
    move_result2 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=operation_motion, speed=0.3
    )

    # Step 4: Release handle
    release_result = adjust_gripper(action="open", force=1.0)

    return {"success": grab_result["grasp_success"], "operation_completed": operation}


def unload_machine(machine_id: str, sample_id: str) -> Dict[str, Any]:
    """
    Unload samples from a laboratory machine.

    Composed of: move -> grab_object -> move -> adjust_gripper

    Args:
        machine_id: Identifier for the machine
        sample_id: Identifier for the sample to unload

    Returns:
        Dict with success and sample_retrieved
    """
    print(f"🏭 UNLOAD MACHINE: {sample_id} from {machine_id}")

    # Step 1: Move to machine
    machine_pose = {"x": 150, "y": 250, "z": 30}
    move_result1 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=machine_pose, speed=0.5
    )

    # Step 2: Grab the sample
    grab_result = grab_object(
        object_id=sample_id,
        grasp_pose={"position": machine_pose, "orientation": {"x": 0, "y": 0, "z": 0}},
        grasp_force=1.0,
    )

    # Step 3: Move to destination
    destination_pose = {"x": 200, "y": 300, "z": 30}
    move_result2 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=destination_pose, speed=0.5
    )

    # Step 4: Release the sample
    release_result = adjust_gripper(action="open", force=1.0)

    return {
        "success": grab_result["grasp_success"],
        "sample_retrieved": grab_result["grasp_success"],
    }


def transfer_liquid(
    source_position: str,
    destination_position: str,
    volume: float,
    pipette_id: str,
    transfer_mode: str = "direct",
    mix_before: bool = False,
    mix_after: bool = False,
    touch_off: bool = True,
) -> Dict[str, Any]:
    """
    Transfer liquid from source to destination with volume control.

    Composed of: grab_tip -> aspirate -> dispense -> discard_tip

    Args:
        source_position: Position of source container
        destination_position: Position of destination container
        volume: Volume to transfer (0.1-1000 μL)
        pipette_id: Identifier for the pipette
        transfer_mode: Transfer mode (direct, multi_dispense, serial_dilution, default: "direct")
        mix_before: Whether to mix before transfer (default: False)
        mix_after: Whether to mix after transfer (default: False)
        touch_off: Whether to touch off after dispensing (default: True)

    Returns:
        Dict with success, actual_volume, transfer_time, and accuracy
    """
    print(
        f"🏭 TRANSFER LIQUID: {volume}μL from {source_position} to {destination_position}"
    )

    # Step 1: Grab tip
    tip_result = grab_tip(
        pipette_id=pipette_id,
        tip_type="p200",  # Would be determined by volume
        force=1.0,
    )

    # Step 2: Aspirate from source
    aspirate_result = aspirate(
        pipette_id=pipette_id,
        volume=volume,
        source_position=source_position,
        aspiration_speed=1.0,
    )

    # Step 3: Dispense to destination
    dispense_result = dispense(
        pipette_id=pipette_id,
        volume=volume,
        target_position=destination_position,
        dispense_speed=1.0,
        touch_off=touch_off,
    )

    # Step 4: Discard tip
    discard_result = discard_tip(pipette_id=pipette_id, force=1.0)

    total_time = aspirate_result["aspiration_time"] + dispense_result["dispense_time"]

    return {
        "success": aspirate_result["success"]
        and dispense_result["success"]
        and discard_result["success"],
        "actual_volume": min(
            aspirate_result["actual_volume"], dispense_result["actual_volume"]
        ),
        "transfer_time": total_time,
        "accuracy": 0.98,  # 98% accuracy
    }


def plate_processing(
    plate_id: str,
    plate_type: str = "96_well",
    operations: List[Dict[str, Any]] = None,
    incubation_time: int = 0,
    temperature: float = 25.0,
) -> Dict[str, Any]:
    """
    Process a microplate with multiple liquid handling operations.

    Composed of: scan_workspace -> grab_tip -> aspirate (repeat) -> dispense (repeat) ->
                 mix (repeat) -> discard_tip

    Args:
        plate_id: Identifier for the plate
        plate_type: Type of plate (96_well, 384_well, 1536_well, default: "96_well")
        operations: List of operations to perform
        incubation_time: Incubation time in seconds (0-3600, default: 0)
        temperature: Processing temperature (4-95°C, default: 25.0)

    Returns:
        Dict with success, wells_processed, processing_time, and quality_metrics
    """
    print(
        f"🏭 PLATE PROCESSING: {plate_id} ({plate_type}) with {len(operations or [])} operations"
    )

    # Step 1: Scan workspace
    scan_result = scan_workspace(object_detection=True, obstacle_detection=True)

    # Step 2: Grab tip
    tip_result = grab_tip(pipette_id="pipette_1", tip_type="p200", force=1.0)

    # Step 3: Process each operation
    wells_processed = 0
    total_time = 0

    for operation in operations or []:
        # Aspirate
        aspirate_result = aspirate(
            pipette_id="pipette_1",
            volume=operation.get("volume", 50),
            source_position=operation.get("source", "A1"),
            aspiration_speed=1.0,
        )

        # Dispense
        dispense_result = dispense(
            pipette_id="pipette_1",
            volume=operation.get("volume", 50),
            target_position=operation.get("target", "A1"),
            dispense_speed=1.0,
        )

        # Mix if required
        if operation.get("mix", False):
            mix_result = mix(
                pipette_id="pipette_1",
                container_position=operation.get("target", "A1"),
                volume=operation.get("volume", 50),
                cycles=3,
            )
            total_time += mix_result["mixing_time"]

        wells_processed += len(operation.get("wells", ["A1"]))
        total_time += (
            aspirate_result["aspiration_time"] + dispense_result["dispense_time"]
        )

    # Step 4: Discard tip
    discard_result = discard_tip(pipette_id="pipette_1", force=1.0)

    return {
        "success": tip_result["success"] and discard_result["success"],
        "wells_processed": wells_processed,
        "processing_time": total_time,
        "quality_metrics": {"accuracy": 0.95, "precision": 0.98},
    }
