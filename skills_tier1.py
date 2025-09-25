"""
Tier 1 (Reusable Patterns) Skills - Composed of Tier 0 skills

These skills represent reusable robotic patterns that are composed of atomic T0 skills.
They provide higher-level functionality while maintaining composability.
"""

from typing import Any, Dict, Optional

from skills_tier0 import adjust_gripper, move, pose_estimation, vlm_assert


def grab_tip(
    pipette_id: str,
    tip_type: str,
    tip_rack_position: Optional[str] = None,
    force: float = 1.0,
    approach_angle: float = 0,
) -> Dict[str, Any]:
    """
    Pick up a new pipette tip from tip rack.

    Composed of: move -> adjust_gripper -> vlm_assert

    Args:
        pipette_id: Identifier for the pipette
        tip_type: Type of tip (p10, p20, p200, p1000, p5000)
        tip_rack_position: Position of tip rack
        force: Grasp force (0.1-5.0, default: 1.0)
        approach_angle: Approach angle (0-90, default: 0)

    Returns:
        Dict with success, tip_position, tip_quality, and attachment_force
    """
    print(f"🔧 GRAB TIP: {pipette_id} ({tip_type})")

    # Step 1: Move to tip rack position
    tip_rack_pose = {"x": 100, "y": 200, "z": 50}  # Would come from machine database
    move_result = move(
        rotations={"x": 0, "y": 0, "z": approach_angle},
        translations=tip_rack_pose,
        speed=0.5,
    )

    # Step 2: Adjust gripper to close and grasp tip
    gripper_result = adjust_gripper(action="close", force=force, speed=0.5)

    # Step 3: Verify tip attachment
    assert_result = vlm_assert(
        assertion="tip_attached", object_id="pipette_tip", confidence_threshold=0.8
    )

    return {
        "success": assert_result["assertion_passed"],
        "tip_position": tip_rack_position or "A1",
        "tip_quality": "good" if assert_result["confidence"] > 0.8 else "poor",
        "attachment_force": gripper_result["final_force"],
    }


def discard_tip(
    pipette_id: str,
    waste_position: Optional[str] = None,
    force: float = 1.0,
    ejection_speed: float = 2.0,
    rinse_before_discard: bool = True,
) -> Dict[str, Any]:
    """
    Discard used pipette tip to waste container.

    Composed of: move -> adjust_gripper -> vlm_assert

    Args:
        pipette_id: Identifier for the pipette
        waste_position: Position of waste container
        force: Ejection force (0.1-5.0, default: 1.0)
        ejection_speed: Speed of tip ejection (0.1-10.0, default: 2.0)
        rinse_before_discard: Whether to rinse before discarding (default: True)

    Returns:
        Dict with success, tip_discarded, waste_position, and ejection_time
    """
    print(f"🔧 DISCARD TIP: {pipette_id}")

    # Step 1: Move to waste position
    waste_pose = {"x": 150, "y": 250, "z": 30}  # Would come from machine database
    move_result = move(
        rotations={"x": 0, "y": 0, "z": 0},
        translations=waste_pose,
        speed=ejection_speed,
    )

    # Step 2: Open gripper to release tip
    gripper_result = adjust_gripper(action="open", force=force, speed=1.0)

    # Step 3: Verify tip was discarded
    assert_result = vlm_assert(
        assertion="tip_discarded", object_id="waste_container", confidence_threshold=0.8
    )

    return {
        "success": assert_result["assertion_passed"],
        "tip_discarded": assert_result["assertion_passed"],
        "waste_position": waste_position or "W1",
        "ejection_time": move_result["execution_time"],
    }


def aspirate(
    pipette_id: str,
    volume: float,
    source_position: str,
    aspiration_speed: float = 1.0,
    pre_wet: bool = False,
    mix_before: bool = False,
    mix_cycles: int = 3,
) -> Dict[str, Any]:
    """
    Aspirate liquid from a source container using pipette.

    Composed of: move -> pose_estimation -> move -> vlm_assert

    Args:
        pipette_id: Identifier for the pipette
        volume: Volume to aspirate (0.1-5000 μL)
        source_position: Position of source container
        aspiration_speed: Speed of aspiration (0.1-10.0, default: 1.0)
        pre_wet: Whether to pre-wet the tip (default: False)
        mix_before: Whether to mix before aspirating (default: False)
        mix_cycles: Number of mixing cycles (1-10, default: 3)

    Returns:
        Dict with success, actual_volume, liquid_level, and aspiration_time
    """
    print(f"🔧 ASPIRATE: {volume}μL from {source_position}")

    # Step 1: Move to source position
    source_pose = {"x": 200, "y": 300, "z": 40}  # Would come from workspace map
    move_result1 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=source_pose, speed=0.5
    )

    # Step 2: Estimate liquid surface pose
    pose_result = pose_estimation(
        object_id="liquid_surface", object_type="liquid", confidence_threshold=0.7
    )

    # Step 3: Move to aspiration depth
    aspiration_depth = pose_result["pose"]["position"]["z"] - 5.0  # 5mm below surface
    move_result2 = move(
        rotations={"x": 0, "y": 0, "z": 0},
        translations={
            "x": source_pose["x"],
            "y": source_pose["y"],
            "z": aspiration_depth,
        },
        speed=aspiration_speed,
    )

    # Step 4: Verify liquid was aspirated
    assert_result = vlm_assert(
        assertion="liquid_aspirated", object_id="pipette_tip", confidence_threshold=0.8
    )

    return {
        "success": assert_result["assertion_passed"],
        "actual_volume": volume * 0.98,  # Assume 2% loss
        "liquid_level": 0.8,  # 80% of tip filled
        "aspiration_time": move_result2["execution_time"],
    }


def dispense(
    pipette_id: str,
    volume: float,
    target_position: str,
    dispense_speed: float = 1.0,
    blowout: bool = True,
    touch_off: bool = False,
    mix_after: bool = False,
    mix_cycles: int = 3,
) -> Dict[str, Any]:
    """
    Dispense liquid from pipette to target container.

    Composed of: move -> pose_estimation -> move -> vlm_assert

    Args:
        pipette_id: Identifier for the pipette
        volume: Volume to dispense (0.1-5000 μL)
        target_position: Position of target container
        dispense_speed: Speed of dispensing (0.1-10.0, default: 1.0)
        blowout: Whether to blowout after dispensing (default: True)
        touch_off: Whether to touch off after dispensing (default: False)
        mix_after: Whether to mix after dispensing (default: False)
        mix_cycles: Number of mixing cycles (1-10, default: 3)

    Returns:
        Dict with success, actual_volume, dispense_time, and remaining_volume
    """
    print(f"🔧 DISPENSE: {volume}μL to {target_position}")

    # Step 1: Move to target position
    target_pose = {"x": 250, "y": 350, "z": 40}  # Would come from workspace map
    move_result1 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=target_pose, speed=0.5
    )

    # Step 2: Estimate target container pose
    pose_result = pose_estimation(
        object_id="target_container", object_type="container", confidence_threshold=0.7
    )

    # Step 3: Move to dispense height
    dispense_height = pose_result["pose"]["position"]["z"] + 2.0  # 2mm above surface
    move_result2 = move(
        rotations={"x": 0, "y": 0, "z": 0},
        translations={
            "x": target_pose["x"],
            "y": target_pose["y"],
            "z": dispense_height,
        },
        speed=dispense_speed,
    )

    # Step 4: Verify liquid was dispensed
    assert_result = vlm_assert(
        assertion="liquid_dispensed",
        object_id="target_container",
        confidence_threshold=0.8,
    )

    return {
        "success": assert_result["assertion_passed"],
        "actual_volume": volume * 0.99,  # Assume 1% loss
        "dispense_time": move_result2["execution_time"],
        "remaining_volume": 0.0,  # Assume all dispensed
    }


def mix(
    pipette_id: str,
    container_position: str,
    volume: float,
    cycles: int = 5,
    mix_height: float = 2.0,
    speed: float = 1.0,
    pattern: str = "vertical",
) -> Dict[str, Any]:
    """
    Mix liquid in a container using pipette mixing cycles.

    Composed of: move -> move (repeat) -> vlm_assert

    Args:
        pipette_id: Identifier for the pipette
        container_position: Position of container
        volume: Volume to mix (1-1000 μL)
        cycles: Number of mixing cycles (1-20, default: 5)
        mix_height: Height of mixing motion (0.1-10.0, default: 2.0)
        speed: Mixing speed (0.1-5.0, default: 1.0)
        pattern: Mixing pattern (vertical, circular, figure8, vortex, default: "vertical")

    Returns:
        Dict with success, cycles_completed, mixing_time, and final_volume
    """
    print(f"🔧 MIX: {volume}μL in {container_position} ({cycles} cycles, {pattern})")

    # Step 1: Move to container position
    container_pose = {"x": 300, "y": 400, "z": 35}  # Would come from workspace map
    move_result1 = move(
        rotations={"x": 0, "y": 0, "z": 0}, translations=container_pose, speed=0.5
    )

    # Step 2: Perform mixing cycles (repeated move operations)
    mixing_time = 0
    for cycle in range(cycles):
        # Mixing motion would be more complex in reality
        mix_result = move(
            rotations={"x": 0, "y": 0, "z": 0},
            translations={
                "x": container_pose["x"],
                "y": container_pose["y"],
                "z": container_pose["z"] - mix_height,
            },
            speed=speed,
        )
        mixing_time += mix_result["execution_time"]

    # Step 3: Verify liquid is mixed
    assert_result = vlm_assert(
        assertion="liquid_mixed", object_id="container", confidence_threshold=0.8
    )

    return {
        "success": assert_result["assertion_passed"],
        "cycles_completed": cycles,
        "mixing_time": mixing_time,
        "final_volume": volume,  # Assume no volume loss
    }


def scan_workspace(
    scan_resolution: float = 1.0,
    scan_height: float = 10.0,
    object_detection: bool = True,
    obstacle_detection: bool = True,
    save_map: bool = True,
) -> Dict[str, Any]:
    """
    Scan and map the robot workspace to identify objects and obstacles.

    Composed of: move (repeat) -> pose_estimation -> vlm_assert

    Args:
        scan_resolution: Resolution of scan (0.1-5.0, default: 1.0)
        scan_height: Height to scan (0-50, default: 10)
        object_detection: Whether to detect objects (default: True)
        obstacle_detection: Whether to detect obstacles (default: True)
        save_map: Whether to save the map (default: True)

    Returns:
        Dict with success, objects_detected, obstacles_detected, workspace_dimensions, and map_file
    """
    print(f"🔧 SCAN WORKSPACE: resolution={scan_resolution}, height={scan_height}")

    # Step 1: Move to scan positions (simplified - would be a grid)
    scan_positions = [
        {"x": 0, "y": 0, "z": scan_height},
        {"x": 100, "y": 0, "z": scan_height},
        {"x": 200, "y": 0, "z": scan_height},
        {"x": 0, "y": 100, "z": scan_height},
        {"x": 100, "y": 100, "z": scan_height},
        {"x": 200, "y": 100, "z": scan_height},
    ]

    total_scan_time = 0
    for pos in scan_positions:
        move_result = move(
            rotations={"x": 0, "y": 0, "z": 0}, translations=pos, speed=0.3
        )
        total_scan_time += move_result["execution_time"]

    # Step 2: Detect objects using pose estimation
    objects_detected = 0
    if object_detection:
        pose_result = pose_estimation(
            object_id="all_objects", object_type="any", confidence_threshold=0.5
        )
        objects_detected = 5  # Placeholder count

    # Step 3: Verify workspace is mapped
    assert_result = vlm_assert(
        assertion="workspace_mapped", object_id="workspace", confidence_threshold=0.8
    )

    return {
        "success": assert_result["assertion_passed"],
        "objects_detected": objects_detected,
        "obstacles_detected": 2 if obstacle_detection else 0,
        "workspace_dimensions": {"x": 300, "y": 200, "z": 100},
        "map_file": "workspace_map.json" if save_map else None,
    }


def measure_volume(
    container_id: str,
    measurement_method: str,
    precision: float = 0.01,
    calibration_standard: Optional[str] = None,
    temperature_compensation: bool = True,
) -> Dict[str, Any]:
    """
    Measure liquid volume in a container using various methods.

    Composed of: pose_estimation -> vlm_assert

    Args:
        container_id: Identifier for the container
        measurement_method: Method to use (gravimetric, volumetric, optical, capacitive)
        precision: Measurement precision (0.001-1.0, default: 0.01)
        calibration_standard: Calibration standard to use
        temperature_compensation: Whether to apply temperature compensation (default: True)

    Returns:
        Dict with success, volume, uncertainty, measurement_time, and method_used
    """
    print(f"🔧 MEASURE VOLUME: {container_id} using {measurement_method}")

    # Step 1: Estimate container pose for measurement
    pose_result = pose_estimation(
        object_id=container_id, object_type="container", confidence_threshold=0.7
    )

    # Step 2: Verify measurement was successful
    assert_result = vlm_assert(
        assertion="volume_measured", object_id=container_id, confidence_threshold=0.8
    )

    return {
        "success": assert_result["assertion_passed"],
        "volume": 25.5,  # Placeholder volume
        "uncertainty": precision,
        "measurement_time": "2024-01-01T12:00:00Z",
        "method_used": measurement_method,
    }
