"""
Skill Composition Analyzer

This module analyzes the skill hierarchy and extracts the composition relationships
to build a DAG (Directed Acyclic Graph) for visualization.
"""

import ast
import inspect
from collections import defaultdict, deque
from typing import Any, Dict, List, Set, Tuple


class SkillCompositionAnalyzer:
    """
    Analyzes skill functions to extract their composition relationships.
    """

    def __init__(self):
        self.skill_modules = {
            "T0": "skills_tier0",
            "T1": "skills_tier1",
            "T2": "skills_tier2",
        }
        self.composition_graph = defaultdict(list)
        self.skill_tiers = {}
        self.skill_imports = {}

    def analyze_skill_composition(self, skill_func) -> List[str]:
        """
        Analyze a skill function to find which other skills it calls.

        Args:
            skill_func: The skill function to analyze

        Returns:
            List of skill names that this function calls
        """
        try:
            source = inspect.getsource(skill_func)
            tree = ast.parse(source)

            called_skills = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        called_skills.append(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        # Handle method calls like skills.move()
                        if hasattr(node.func.value, "id"):
                            called_skills.append(
                                f"{node.func.value.id}.{node.func.attr}"
                            )

            return called_skills

        except Exception as e:
            print(f"Error analyzing {skill_func.__name__}: {e}")
            return []

    def build_composition_graph(self, skills_registry):
        """
        Build the complete composition graph from the skills registry.

        Args:
            skills_registry: RobotSkills instance with all skills
        """
        # Analyze T0 skills (atomic - no subskills)
        for skill_name, skill_func in skills_registry.tier0.items():
            self.skill_tiers[skill_name] = "T0"
            self.composition_graph[skill_name] = []  # T0 skills have no subskills

        # Analyze T1 skills
        for skill_name, skill_func in skills_registry.tier1.items():
            self.skill_tiers[skill_name] = "T1"
            subskills = self.analyze_skill_composition(skill_func)
            # Filter to only include actual skill calls (not print statements, etc.)
            skill_calls = [s for s in subskills if s in skills_registry.all_skills]
            self.composition_graph[skill_name] = skill_calls

        # Analyze T2 skills
        for skill_name, skill_func in skills_registry.tier2.items():
            self.skill_tiers[skill_name] = "T2"
            subskills = self.analyze_skill_composition(skill_func)
            # Filter to only include actual skill calls
            skill_calls = [s for s in subskills if s in skills_registry.all_skills]
            self.composition_graph[skill_name] = skill_calls

    def get_skill_dependencies(self, skill_name: str) -> List[str]:
        """
        Get all skills that a given skill depends on (recursively).

        Args:
            skill_name: Name of the skill

        Returns:
            List of all dependent skill names
        """
        dependencies = set()
        queue = deque([skill_name])

        while queue:
            current_skill = queue.popleft()
            if current_skill in self.composition_graph:
                for subskill in self.composition_graph[current_skill]:
                    if subskill not in dependencies:
                        dependencies.add(subskill)
                        queue.append(subskill)

        return list(dependencies)

    def get_skill_usage(self, skill_name: str) -> List[str]:
        """
        Get all skills that use a given skill as a subskill.

        Args:
            skill_name: Name of the skill

        Returns:
            List of skills that use this skill
        """
        users = []
        for skill, subskills in self.composition_graph.items():
            if skill_name in subskills:
                users.append(skill)
        return users

    def get_skill_hierarchy(self, skill_name: str) -> Dict[str, Any]:
        """
        Get the complete hierarchy for a skill including all subskills.

        Args:
            skill_name: Name of the skill

        Returns:
            Dictionary with hierarchy information
        """
        if skill_name not in self.composition_graph:
            return {"error": f"Skill '{skill_name}' not found"}

        def build_hierarchy(skill, visited=None):
            if visited is None:
                visited = set()

            if skill in visited:
                return {
                    "name": skill,
                    "tier": self.skill_tiers.get(skill, "Unknown"),
                    "circular": True,
                }

            visited.add(skill)

            hierarchy = {
                "name": skill,
                "tier": self.skill_tiers.get(skill, "Unknown"),
                "subskills": [],
            }

            for subskill in self.composition_graph[skill]:
                hierarchy["subskills"].append(build_hierarchy(subskill, visited.copy()))

            return hierarchy

        return build_hierarchy(skill_name)

    def get_execution_order(self, skill_name: str) -> List[str]:
        """
        Get the execution order for a skill (topological sort).

        Args:
            skill_name: Name of the skill

        Returns:
            List of skills in execution order
        """
        if skill_name not in self.composition_graph:
            return []

        # Build dependency graph
        dependencies = defaultdict(set)
        for skill, subskills in self.composition_graph.items():
            for subskill in subskills:
                dependencies[skill].add(subskill)

        # Topological sort
        in_degree = defaultdict(int)
        for skill in dependencies:
            in_degree[skill] = 0
        for skill, deps in dependencies.items():
            for dep in deps:
                in_degree[dep] += 1

        queue = deque([skill_name])
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            for skill, deps in dependencies.items():
                if current in deps:
                    in_degree[skill] -= 1
                    if in_degree[skill] == 0:
                        queue.append(skill)

        return result

    def get_skill_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the skill composition.

        Returns:
            Dictionary with composition statistics
        """
        stats = {
            "total_skills": len(self.composition_graph),
            "tier_counts": defaultdict(int),
            "max_depth": 0,
            "most_complex_skill": None,
            "most_used_skill": None,
        }

        # Count by tier
        for skill, tier in self.skill_tiers.items():
            stats["tier_counts"][tier] += 1

        # Find most complex skill (most subskills)
        max_subskills = 0
        for skill, subskills in self.composition_graph.items():
            if len(subskills) > max_subskills:
                max_subskills = len(subskills)
                stats["most_complex_skill"] = skill

        # Find most used skill
        usage_count = defaultdict(int)
        for skill, subskills in self.composition_graph.items():
            for subskill in subskills:
                usage_count[subskill] += 1

        if usage_count:
            stats["most_used_skill"] = max(usage_count, key=usage_count.get)

        return stats

    def export_dag_data(self) -> Dict[str, Any]:
        """
        Export the complete DAG data for visualization.

        Returns:
            Dictionary with nodes and edges for DAG visualization
        """
        nodes = []
        edges = []

        # Create nodes
        for skill_name, tier in self.skill_tiers.items():
            nodes.append(
                {"id": skill_name, "tier": tier, "label": skill_name, "type": "skill"}
            )

        # Create edges
        for skill, subskills in self.composition_graph.items():
            for subskill in subskills:
                edges.append(
                    {"source": skill, "target": subskill, "type": "composition"}
                )

        return {
            "nodes": nodes,
            "edges": edges,
            "tiers": {
                "T0": {"color": "#ff6b6b", "label": "Atomic Skills"},
                "T1": {"color": "#4ecdc4", "label": "Pattern Skills"},
                "T2": {"color": "#45b7d1", "label": "Procedural Skills"},
            },
        }


def create_skill_analyzer():
    """Create and configure a skill composition analyzer."""
    from skills_main import create_skill_executor

    # Create skills registry
    skills = create_skill_executor()

    # Create analyzer
    analyzer = SkillCompositionAnalyzer()
    analyzer.build_composition_graph(skills)

    return analyzer, skills


if __name__ == "__main__":
    # Example usage
    analyzer, skills = create_skill_analyzer()

    print("🔍 SKILL COMPOSITION ANALYSIS")
    print("=" * 50)

    # Show composition for a T2 skill
    print("\n📊 Transfer Liquid Composition:")
    hierarchy = analyzer.get_skill_hierarchy("transfer_liquid")
    print(f"Hierarchy: {hierarchy}")

    # Show dependencies
    print(f"\nDependencies: {analyzer.get_skill_dependencies('transfer_liquid')}")

    # Show usage
    print(f"\nUsed by: {analyzer.get_skill_usage('move')}")

    # Show statistics
    stats = analyzer.get_skill_statistics()
    print(f"\n📈 Statistics: {stats}")

    # Export DAG data
    dag_data = analyzer.export_dag_data()
    print(
        f"\n🕸️ DAG Data: {len(dag_data['nodes'])} nodes, {len(dag_data['edges'])} edges"
    )
