# Robot Skills Registry Summary

This document provides an overview of all the robot skills created for the agent workflow system, organized by tier.

## Tier 0 (Atomic Skills) - Context-free, atomic robot actions

### Basic Movement & Manipulation
- **move** - Move robot end-effector with specified rotations and translations
- **grab_object** - Grasp an object with the robot gripper
- **align_objects** - Align two objects relative to each other with specified orientation
- **adjust_gripper** - Adjust gripper position, force, or configuration

### Vision & Perception
- **vlm_assert** - Use Vision Language Model to verify scene conditions and object states
- **pose_estimation** - Estimate the 6DOF pose of an object using computer vision

### Emergency & Safety
- **emergency_stop** - Emergency stop all robot operations and return to safe state

## Tier 1 (Reusable Patterns) - Composed of Tier 0 skills

### Liquid Handling
- **grab_tip** - Pick up a new pipette tip from tip rack
- **discard_tip** - Discard used pipette tip to waste container
- **aspirate** - Aspirate liquid from a source container using pipette
- **dispense** - Dispense liquid from pipette to target container
- **mix** - Mix liquid in a container using pipette mixing cycles

### Workspace Management
- **scan_workspace** - Scan and map the robot workspace to identify objects and obstacles

### Measurement
- **measure_volume** - Measure liquid volume in a container using various methods

## Tier 2 (Procedural Skills) - High-level workflows

### Generic Machine Operations
- **load_machine** - Load a sample or plate into a laboratory machine using machine database waypoints
- **operate_machine_interface** - Operate machine interface (open/close doors, lids, etc.) using machine database waypoints
- **execute_machine_operation** - Execute machine operations (start cycles, set parameters, etc.) using machine database commands
- **unload_machine** - Unload samples from a laboratory machine using machine database waypoints

### Liquid Processing
- **transfer_liquid** - Transfer liquid from source to destination with volume control
- **plate_processing** - Process a microplate with multiple liquid handling operations

### Quality & Calibration
- **calibrate_instrument** - Calibrate laboratory instruments (pipettes, scales, etc.)
- **quality_control** - Perform quality control checks on samples or processes

### Maintenance & Safety
- **clean_workspace** - Clean and sanitize the robot workspace
- **sterilize_equipment** - Sterilize laboratory equipment using appropriate methods

## Skill Composition Examples

### Simple Workflow: Liquid Transfer
```
1. scan_workspace (T1)
2. grab_object (T0) - pick up pipette
3. grab_tip (T1)
4. aspirate (T1)
5. dispense (T1)
6. discard_tip (T1)
7. adjust_gripper (T0) - release pipette
```

### Complex Workflow: PCR Analysis
```
1. scan_workspace (T1)
2. load_machine (T2, machine_id="thermocycler_1") - load samples into thermocycler
3. operate_machine_interface (T2, machine_id="thermocycler_1", operation="close_lid")
4. execute_machine_operation (T2, machine_id="thermocycler_1", operation="start_protocol", parameters={"protocol_name": "pcr_standard", "cycles": 30})
5. unload_machine (T2, machine_id="thermocycler_1")
6. load_machine (T2, machine_id="centrifuge_1") - transfer to centrifuge
7. execute_machine_operation (T2, machine_id="centrifuge_1", operation="start_cycle", parameters={"rpm": 3000, "duration": 300})
8. unload_machine (T2, machine_id="centrifuge_1")
9. load_machine (T2, machine_id="spectrophotometer_1")
10. execute_machine_operation (T2, machine_id="spectrophotometer_1", operation="start_reading", parameters={"wavelengths": [260, 280], "measurement_type": "absorbance"})
11. quality_control (T2)
```

### Maintenance Workflow
```
1. emergency_stop (T0) - if needed
2. clean_workspace (T2)
3. sterilize_equipment (T2)
4. calibrate_instrument (T2)
5. quality_control (T2)
```

## Key Features of the Skill System

### Safety & Error Handling
- Comprehensive failure modes with mitigation strategies
- Safety constraints and limits
- Emergency stop capabilities
- Retry policies with backoff

### Flexibility & Reusability
- Skills can be composed into complex workflows
- Clear tier separation allows for modular design
- Extensive input validation through JSON schemas
- Preconditions and postconditions for workflow planning

### Monitoring & Telemetry
- Detailed output schemas for result tracking
- Telemetry data for performance monitoring
- Cost models for resource planning
- Timeout and retry configurations

### Laboratory-Specific Features
- Support for various laboratory equipment
- Contamination prevention measures
- Quality control integration
- Temperature and environmental control

## Machine Database Integration

The system now includes a `machine_database.json` file that contains:

### Machine Definitions
- **Machine IDs**: Unique identifiers for each machine (e.g., "centrifuge_1", "incubator_1")
- **Machine Types**: Categorization (centrifuge, incubator, thermocycler, spectrophotometer)
- **Locations**: Physical workspace positions
- **Waypoints**: Predefined robot positions for machine interaction
- **Operations**: Available machine commands and their parameters
- **Safety Limits**: Machine-specific operational constraints

### Generic Machine Skills
All machine operations now use the generic pattern:
- `load_machine(machine_id, sample_id)` - Load samples using machine-specific waypoints
- `operate_machine_interface(machine_id, operation)` - Open/close doors, lids, etc.
- `execute_machine_operation(machine_id, operation, parameters)` - Start cycles, set parameters
- `unload_machine(machine_id, sample_id)` - Retrieve samples from machines

### Benefits
1. **Flexibility**: Add new machines by updating the database file
2. **Consistency**: Standardized waypoints and operations across all machines
3. **Maintainability**: Centralized machine configuration
4. **Safety**: Machine-specific safety limits and constraints
5. **Scalability**: Easy to add new machine types and operations

## Complete Skill Registry

### Skill Count by Tier
- **Tier 0 (Atomic)**: 7 skills - Basic robot movements, vision, and safety
- **Tier 1 (Reusable Patterns)**: 6 skills - Liquid handling, workspace management, measurement
- **Tier 2 (Procedural)**: 10 skills - Machine operations, liquid processing, quality control, maintenance

**Total: 23 skills** organized across 3 tiers for maximum flexibility and composition.

### Recent Updates
1. **Split `change_tip`** into `grab_tip` and `discard_tip` for better granularity
2. **Refactored machine operations** to use generic `machine_id` parameter with centralized database
3. **Removed machine-specific skills** in favor of generic operations
4. **Added machine database** with waypoints, operations, and safety limits

This skill registry provides a comprehensive foundation for building complex laboratory automation workflows while maintaining safety, reliability, and flexibility.
