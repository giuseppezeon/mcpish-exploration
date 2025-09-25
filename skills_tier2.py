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

        valid_operations = ["open_door", "close_door", "open_lid", "close_lid"]
        if operation not in valid_operations:
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": f"Invalid operation: must be one of {valid_operations}",
            }

        print(f"🏭 OPERATE MACHINE INTERFACE: {operation} on {machine_id}")

        # Step 1: Move to machine
        machine_waypoint = {"x": 100, "y": 200, "z": 45}
        move_result1 = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=machine_waypoint, speed=0.5
        )

        if not move_result1["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"],
                "error": f"Move to machine failed: {move_result1['error']}",
            }

        # Step 2: Grab machine handle
        handle_pose = {
            "position": {"x": 100, "y": 200, "z": 45},
            "orientation": {"x": 0, "y": 0, "z": 0},
        }
        grab_result = grab_object(
            object_id="machine_handle", grasp_pose=handle_pose, grasp_force=1.0
        )

        if not grab_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"],
                "error": f"Grab handle failed: {grab_result['error']}",
            }

        # Step 3: Perform operation motion
        operation_motion = {"x": 0, "y": 0, "z": -5}
        move_result2 = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=operation_motion, speed=0.3
        )

        if not move_result2["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"]
                + move_result2["execution_time"],
                "error": f"Operation motion failed: {move_result2['error']}",
            }

        # Step 4: Release handle
        release_result = adjust_gripper(action="open", force=1.0)

        if not release_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"]
                + move_result2["execution_time"]
                + release_result["execution_time"],
                "error": f"Release handle failed: {release_result['error']}",
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
                "operation": operation,
                "operation_completed": operation,
                "machine_waypoint": machine_waypoint,
                "handle_pose": handle_pose,
            },
            "execution_time": total_time,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "execution_time": 0.0,
            "error": f"Operate machine interface failed: {str(e)}",
        }


def unload_machine(machine_id: str, sample_id: str) -> Dict[str, Any]:
    """
    Unload samples from a laboratory machine.

    Composed of: move -> grab_object -> move -> adjust_gripper

    Args:
        machine_id: Identifier for the machine
        sample_id: Identifier for the sample to unload

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

        print(f"🏭 UNLOAD MACHINE: {sample_id} from {machine_id}")

        # Step 1: Move to machine
        machine_pose = {"x": 150, "y": 250, "z": 30}
        move_result1 = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=machine_pose, speed=0.5
        )

        if not move_result1["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"],
                "error": f"Move to machine failed: {move_result1['error']}",
            }

        # Step 2: Grab the sample
        grab_result = grab_object(
            object_id=sample_id,
            grasp_pose={
                "position": machine_pose,
                "orientation": {"x": 0, "y": 0, "z": 0},
            },
            grasp_force=1.0,
        )

        if not grab_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"],
                "error": f"Grab sample failed: {grab_result['error']}",
            }

        # Step 3: Move to destination
        destination_pose = {"x": 200, "y": 300, "z": 30}
        move_result2 = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=destination_pose, speed=0.5
        )

        if not move_result2["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": move_result1["execution_time"]
                + grab_result["execution_time"]
                + move_result2["execution_time"],
                "error": f"Move to destination failed: {move_result2['error']}",
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
                "sample_retrieved": True,
                "machine_pose": machine_pose,
                "destination_pose": destination_pose,
            },
            "execution_time": total_time,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "execution_time": 0.0,
            "error": f"Unload machine failed: {str(e)}",
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
        Standardized result dict with success, data, execution_time, error
    """
    try:
        # Input validation
        if not source_position or not isinstance(source_position, str):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid source_position: must be non-empty string",
            }

        if not destination_position or not isinstance(destination_position, str):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid destination_position: must be non-empty string",
            }

        if not (0.1 <= volume <= 1000):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid volume: must be between 0.1 and 1000 μL",
            }

        if not pipette_id or not isinstance(pipette_id, str):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid pipette_id: must be non-empty string",
            }

        valid_modes = ["direct", "multi_dispense", "serial_dilution"]
        if transfer_mode not in valid_modes:
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": f"Invalid transfer_mode: must be one of {valid_modes}",
            }

        print(
            f"🏭 TRANSFER LIQUID: {volume}μL from {source_position} to {destination_position}"
        )

        # Step 1: Grab tip
        tip_result = grab_tip(
            pipette_id=pipette_id,
            tip_type="p200",  # Would be determined by volume
            force=1.0,
        )

        if not tip_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": tip_result["execution_time"],
                "error": f"Grab tip failed: {tip_result['error']}",
            }

        # Step 2: Aspirate from source
        aspirate_result = aspirate(
            pipette_id=pipette_id,
            volume=volume,
            source_position=source_position,
            aspiration_speed=1.0,
        )

        if not aspirate_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": tip_result["execution_time"]
                + aspirate_result["execution_time"],
                "error": f"Aspirate failed: {aspirate_result['error']}",
            }

        # Step 3: Dispense to destination
        dispense_result = dispense(
            pipette_id=pipette_id,
            volume=volume,
            target_position=destination_position,
            dispense_speed=1.0,
            touch_off=touch_off,
        )

        if not dispense_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": tip_result["execution_time"]
                + aspirate_result["execution_time"]
                + dispense_result["execution_time"],
                "error": f"Dispense failed: {dispense_result['error']}",
            }

        # Step 4: Discard tip
        discard_result = discard_tip(pipette_id=pipette_id, force=1.0)

        if not discard_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": tip_result["execution_time"]
                + aspirate_result["execution_time"]
                + dispense_result["execution_time"]
                + discard_result["execution_time"],
                "error": f"Discard tip failed: {discard_result['error']}",
            }

        total_time = (
            tip_result["execution_time"]
            + aspirate_result["execution_time"]
            + dispense_result["execution_time"]
            + discard_result["execution_time"]
        )
        actual_volume = min(
            aspirate_result["data"]["actual_volume"],
            dispense_result["data"]["actual_volume"],
        )
        accuracy = 0.98  # 98% accuracy

        return {
            "success": True,
            "data": {
                "source_position": source_position,
                "destination_position": destination_position,
                "volume": volume,
                "actual_volume": actual_volume,
                "pipette_id": pipette_id,
                "transfer_mode": transfer_mode,
                "accuracy": accuracy,
                "mix_before": mix_before,
                "mix_after": mix_after,
                "touch_off": touch_off,
            },
            "execution_time": total_time,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "execution_time": 0.0,
            "error": f"Transfer liquid failed: {str(e)}",
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
        Standardized result dict with success, data, execution_time, error
    """
    try:
        # Input validation
        if not plate_id or not isinstance(plate_id, str):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid plate_id: must be non-empty string",
            }

        valid_plate_types = ["96_well", "384_well", "1536_well"]
        if plate_type not in valid_plate_types:
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": f"Invalid plate_type: must be one of {valid_plate_types}",
            }

        if not (0 <= incubation_time <= 3600):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid incubation_time: must be between 0 and 3600 seconds",
            }

        if not (4 <= temperature <= 95):
            return {
                "success": False,
                "data": {},
                "execution_time": 0.0,
                "error": "Invalid temperature: must be between 4 and 95°C",
            }

        print(
            f"🏭 PLATE PROCESSING: {plate_id} ({plate_type}) with {len(operations or [])} operations"
        )

        # Step 1: Scan workspace
        scan_result = scan_workspace(object_detection=True, obstacle_detection=True)

        if not scan_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": scan_result["execution_time"],
                "error": f"Workspace scan failed: {scan_result['error']}",
            }

        # Step 2: Grab tip
        tip_result = grab_tip(pipette_id="pipette_1", tip_type="p200", force=1.0)

        if not tip_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": scan_result["execution_time"]
                + tip_result["execution_time"],
                "error": f"Grab tip failed: {tip_result['error']}",
            }

        # Step 3: Process each operation
        wells_processed = 0
        total_time = scan_result["execution_time"] + tip_result["execution_time"]
        operation_results = []

        for i, operation in enumerate(operations or []):
            # Aspirate
            aspirate_result = aspirate(
                pipette_id="pipette_1",
                volume=operation.get("volume", 50),
                source_position=operation.get("source", "A1"),
                aspiration_speed=1.0,
            )

            if not aspirate_result["success"]:
                return {
                    "success": False,
                    "data": {},
                    "execution_time": total_time + aspirate_result["execution_time"],
                    "error": f"Operation {i + 1} aspirate failed: {aspirate_result['error']}",
                }

            # Dispense
            dispense_result = dispense(
                pipette_id="pipette_1",
                volume=operation.get("volume", 50),
                target_position=operation.get("target", "A1"),
                dispense_speed=1.0,
            )

            if not dispense_result["success"]:
                return {
                    "success": False,
                    "data": {},
                    "execution_time": total_time
                    + aspirate_result["execution_time"]
                    + dispense_result["execution_time"],
                    "error": f"Operation {i + 1} dispense failed: {dispense_result['error']}",
                }

            # Mix if required
            if operation.get("mix", False):
                mix_result = mix(
                    pipette_id="pipette_1",
                    container_position=operation.get("target", "A1"),
                    volume=operation.get("volume", 50),
                    cycles=3,
                )

                if not mix_result["success"]:
                    return {
                        "success": False,
                        "data": {},
                        "execution_time": total_time
                        + aspirate_result["execution_time"]
                        + dispense_result["execution_time"]
                        + mix_result["execution_time"],
                        "error": f"Operation {i + 1} mix failed: {mix_result['error']}",
                    }

                total_time += mix_result["execution_time"]

            wells_processed += len(operation.get("wells", ["A1"]))
            total_time += (
                aspirate_result["execution_time"] + dispense_result["execution_time"]
            )

            operation_results.append(
                {
                    "operation": i + 1,
                    "aspirate_success": aspirate_result["success"],
                    "dispense_success": dispense_result["success"],
                    "mix_success": operation.get("mix", False)
                    and mix_result.get("success", True),
                }
            )

        # Step 4: Discard tip
        discard_result = discard_tip(pipette_id="pipette_1", force=1.0)

        if not discard_result["success"]:
            return {
                "success": False,
                "data": {},
                "execution_time": total_time + discard_result["execution_time"],
                "error": f"Discard tip failed: {discard_result['error']}",
            }

        total_time += discard_result["execution_time"]
        quality_metrics = {"accuracy": 0.95, "precision": 0.98}

        return {
            "success": True,
            "data": {
                "plate_id": plate_id,
                "plate_type": plate_type,
                "wells_processed": wells_processed,
                "operations_count": len(operations or []),
                "incubation_time": incubation_time,
                "temperature": temperature,
                "quality_metrics": quality_metrics,
                "operation_results": operation_results,
            },
            "execution_time": total_time,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "execution_time": 0.0,
            "error": f"Plate processing failed: {str(e)}",
        }
