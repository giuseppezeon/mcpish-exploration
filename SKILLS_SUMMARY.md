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

### Machine Operations
- **load_machine** - Load a sample into a laboratory machine
- **operate_machine_interface** - Operate machine interface (open/close doors, lids, etc.)
- **unload_machine** - Unload samples from a laboratory machine

### Liquid Processing
- **transfer_liquid** - Transfer liquid from source to destination with volume control
- **plate_processing** - Process a microplate with multiple liquid handling operations

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

### Complex Workflow: Sample Processing
```
1. scan_workspace (T1)
2. load_machine (T2, machine_id="centrifuge_1", sample_id="sample_001")
3. operate_machine_interface (T2, machine_id="centrifuge_1", operation="close_door")
4. unload_machine (T2, machine_id="centrifuge_1", sample_id="sample_001")
5. transfer_liquid (T2, source_position="A1", destination_position="B1", volume=100.0, pipette_id="pipette_1")
6. plate_processing (T2, plate_id="plate_001", operations=[...])
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
- **Tier 2 (Procedural)**: 5 skills - Machine operations and liquid processing

**Total: 18 skills** organized across 3 tiers for maximum flexibility and composition.

### Recent Updates
1. **Split `change_tip`** into `grab_tip` and `discard_tip` for better granularity
2. **Simplified machine operations** to focus on core functionality
3. **Removed overly generic skills** (calibrate_instrument, quality_control, clean_workspace, sterilize_equipment)
4. **Streamlined skill registry** to 18 focused skills across 3 tiers

This skill registry provides a comprehensive foundation for building complex laboratory automation workflows while maintaining safety, reliability, and flexibility.
