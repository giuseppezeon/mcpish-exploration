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
- **change_tip** - Change pipette tip (discard old, pick up new)
- **aspirate** - Aspirate liquid from a source container using pipette
- **dispense** - Dispense liquid from pipette to target container
- **mix** - Mix liquid in a container using pipette mixing cycles

### Workspace Management
- **scan_workspace** - Scan and map the robot workspace to identify objects and obstacles

### Measurement
- **measure_volume** - Measure liquid volume in a container using various methods

## Tier 2 (Procedural Skills) - High-level workflows

### Machine Operations
- **load_machine** - Load a sample or plate into a laboratory machine
- **centrifuge_cycle** - Run a centrifuge cycle for a plate (existing)
- **centrifuge_samples** - Centrifuge samples at specified speed and duration

### Liquid Processing
- **transfer_liquid** - Transfer liquid from source to destination with volume control
- **plate_processing** - Process a microplate with multiple liquid handling operations

### Quality & Calibration
- **calibrate_instrument** - Calibrate laboratory instruments (pipettes, scales, etc.)
- **quality_control** - Perform quality control checks on samples or processes

### Sample Processing
- **incubate_samples** - Incubate samples at specified temperature and conditions
- **pcr_cycle** - Execute PCR thermal cycling protocol
- **spectrophotometer_reading** - Take spectrophotometer readings of samples

### Maintenance & Safety
- **clean_workspace** - Clean and sanitize the robot workspace
- **sterilize_equipment** - Sterilize laboratory equipment using appropriate methods

## Skill Composition Examples

### Simple Workflow: Liquid Transfer
```
1. scan_workspace (T1)
2. grab_object (T0) - pick up pipette
3. change_tip (T1)
4. aspirate (T1)
5. dispense (T1)
6. adjust_gripper (T0) - release pipette
```

### Complex Workflow: PCR Analysis
```
1. scan_workspace (T1)
2. load_machine (T2) - load samples into thermocycler
3. pcr_cycle (T2)
4. load_machine (T2) - transfer to centrifuge
5. centrifuge_samples (T2)
6. spectrophotometer_reading (T2)
7. quality_control (T2)
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

This skill registry provides a comprehensive foundation for building complex laboratory automation workflows while maintaining safety, reliability, and flexibility.
