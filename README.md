# 🤖 Robot Skills System - Interactive DAG Visualization

A comprehensive robot skills hierarchy system with interactive DAG visualization, skill composition analysis, and workflow management.

## 🎯 Overview

This system provides a three-tier robot skills architecture:
- **Tier 0 (Atomic)**: 7 fundamental robot operations
- **Tier 1 (Pattern)**: 7 reusable robotic patterns
- **Tier 2 (Procedural)**: 5 high-level laboratory workflows

All skills are fully standardized with consistent error handling, input validation, and return formats.

## 🚀 Quick Start

### 1. **Interactive DAG Visualization** (Recommended)
```bash
# Start the web-based DAG visualizer
python launch_dag_visualizer.py
```
**Features:**
- 🕸️ Interactive skill hierarchy visualization
- 🔍 Drill-down skill composition analysis
- 📊 Real-time skill statistics
- 🎨 Multiple layout options (hierarchical, force-directed, circular)
- 🔗 Workflow builder
- 📈 Execution path visualization

### 2. **Standalone HTML Visualizer**
```bash
# Open in browser (no Python server required)
open standalone_dag_visualizer.html
```

### 3. **Python Backend Server**
```bash
# Install dependencies
pip install -r requirements_dag.txt

# Start server
python dag_server.py
# Then open: http://localhost:5000
```

## 📊 Available Visualizations

### **1. DAG Visualizer Web Interface**
- **Interactive Nodes**: Click any skill to see its composition
- **Tier Filtering**: Filter by T0, T1, or T2 skills
- **Layout Options**:
  - Hierarchical (T0 → T1 → T2 flow)
  - Force-directed (natural clustering)
  - Circular (radial arrangement)
- **Search & Filter**: Find specific skills quickly
- **Workflow Builder**: Combine multiple skills into workflows

### **2. Skill Composition Analysis**
```bash
# Analyze skill compositions programmatically
python skill_composition_analyzer.py
```
**Output:**
- Complete skill dependency graphs
- Execution order analysis
- Usage statistics
- Composition breakdowns

### **3. Skill Testing & Examples**
```bash
# Run comprehensive skill tests
python test_skills.py
```
**Features:**
- Tier-by-tier skill testing
- Composition verification
- Workflow execution examples
- Error handling validation

### **4. Main Skills Interface**
```bash
# Run the main skills examples
python skills_main.py
```
**Examples:**
- Liquid transfer workflow
- Machine loading/unloading
- Skill statistics and information

## 🎨 Visualization Features

### **Interactive DAG Features:**
- **Zoom & Pan**: Navigate large skill hierarchies
- **Node Highlighting**: Click to highlight skill relationships
- **Tooltips**: Hover for quick skill information
- **Color Coding**:
  - 🔴 T0 (Atomic) - Red
  - 🟢 T1 (Pattern) - Teal
  - 🔵 T2 (Procedural) - Blue
- **Real-time Stats**: Live skill count and relationship metrics

### **Skill Explorer:**
- **Composition View**: See exactly which sub-skills are called
- **Execution Path**: Step-by-step execution breakdown
- **Dependency Analysis**: What skills depend on each other
- **Usage Tracking**: Which skills use a particular sub-skill

### **Workflow Builder:**
- **Drag & Drop**: Build custom workflows visually
- **Skill Combination**: Combine multiple T2 skills
- **Execution Planning**: Plan complex laboratory procedures
- **Validation**: Ensure workflow compatibility

## 🛠️ Development & Testing

### **Run All Tests:**
```bash
# Test all skill tiers
python test_skills.py

# Test specific components
python -c "from skills_main import create_skill_executor; skills = create_skill_executor(); print('✅ All skills loaded successfully')"
```

### **Skill Development:**
```bash
# Add new skills to any tier
# 1. Add function to appropriate tier file (skills_tier0.py, skills_tier1.py, skills_tier2.py)
# 2. Update skills_main.py registry
# 3. Run tests to verify
```

### **API Endpoints** (when server running):
- `GET /api/skills/dag` - Complete DAG data
- `GET /api/skills/<name>` - Individual skill details
- `GET /api/skills/statistics` - Skill statistics
- `GET /api/health` - System health check

## 📁 Project Structure

```
mcpish-exploration/
├── skills_tier0.py          # Atomic skills (7 functions)
├── skills_tier1.py          # Pattern skills (7 functions)
├── skills_tier2.py          # Procedural skills (5 functions)
├── skills_main.py           # Unified interface
├── skill_composition_analyzer.py  # DAG analysis
├── test_skills.py           # Comprehensive testing
├── dag_server.py            # Web server backend
├── standalone_dag_visualizer.html  # Standalone visualizer
├── enhanced_dag_visualizer.html   # Enhanced visualizer
├── launch_dag_visualizer.py # Launcher script
└── requirements_dag.txt     # Dependencies
```

## 🎯 Key Features

### **Standardized Skill Interface:**
```python
{
    "success": bool,
    "data": dict,        # skill-specific data
    "execution_time": float,
    "error": str | None
}
```

### **Comprehensive Error Handling:**
- Input validation for all parameters
- Error propagation through skill hierarchy
- Detailed error messages with context
- Graceful failure handling

### **Skill Composition:**
- **T1 Skills**: Composed of T0 skills
- **T2 Skills**: Composed of T1 and T0 skills
- **Clear Documentation**: Each skill shows its sub-skill composition
- **Execution Tracking**: Time and success metrics

## 🔧 Customization

### **Add New Skills:**
1. **T0 Skills**: Add to `skills_tier0.py` (atomic operations)
2. **T1 Skills**: Add to `skills_tier1.py` (composed of T0)
3. **T2 Skills**: Add to `skills_tier2.py` (composed of T1/T0)
4. **Update Registry**: Add to `skills_main.py`
5. **Test**: Run `test_skills.py` to verify

### **Modify Visualizations:**
- **Colors**: Edit color schemes in HTML files
- **Layouts**: Modify D3.js layout algorithms
- **Styling**: Update CSS in visualization files
- **Data**: Modify skill data in Python files

## 📈 Performance & Monitoring

### **Execution Time Tracking:**
- All skills report execution time
- Hierarchical time accumulation
- Performance bottleneck identification

### **Success Rate Monitoring:**
- Individual skill success rates
- Workflow completion rates
- Error pattern analysis

### **Skill Usage Analytics:**
- Most frequently used skills
- Skill dependency analysis
- Workflow optimization insights

## 🚨 Troubleshooting

### **Common Issues:**

**1. DAG Visualizer Not Loading:**
```bash
# Check if server is running
curl http://localhost:5000/api/health

# Restart server
python dag_server.py
```

**2. Skills Not Found:**
```bash
# Verify skill registry
python -c "from skills_main import create_skill_executor; skills = create_skill_executor(); print(skills.list_skills())"
```

**3. Import Errors:**
```bash
# Install dependencies
pip install -r requirements_dag.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## 🎉 Examples

### **Simple Skill Execution:**
```python
from skills_main import create_skill_executor

skills = create_skill_executor()
result = skills.execute_skill("move",
    rotations={"x": 0, "y": 0, "z": 0},
    translations={"x": 100, "y": 200, "z": 50}
)
print(f"Success: {result['success']}")
```

### **Complex Workflow:**
```python
# Liquid transfer workflow
skills = create_skill_executor()

# Scan workspace
scan_result = skills.execute_skill("scan_workspace")

# Transfer liquid
transfer_result = skills.execute_skill("transfer_liquid",
    source_position="A1",
    destination_position="B1",
    volume=50.0,
    pipette_id="pipette_1"
)
```

### **Skill Analysis:**
```python
from skill_composition_analyzer import create_skill_analyzer

analyzer, skills = create_skill_analyzer()

# Get skill composition
composition = analyzer.get_skill_hierarchy("transfer_liquid")
print(f"Transfer liquid is composed of: {composition}")

# Get execution order
order = analyzer.get_execution_order("transfer_liquid")
print(f"Execution order: {order}")
```

## 📚 Documentation

- **Skill Documentation**: Each function has comprehensive docstrings
- **API Reference**: Available when server is running at `/api/`
- **Examples**: See `skills_main.py` for usage examples
- **Testing**: See `test_skills.py` for test patterns

## 🤝 Contributing

1. **Add Skills**: Follow the standardized format
2. **Update Tests**: Add tests for new skills
3. **Update Documentation**: Update this README
4. **Test Everything**: Run all test suites

## 📄 License

This project is part of the Zeon robot skills system for laboratory automation.

---

**🎯 Ready to explore? Start with the DAG visualizer:**
```bash
python launch_dag_visualizer.py
```

**🌐 Or open the standalone version:**
```bash
open standalone_dag_visualizer.html
```
