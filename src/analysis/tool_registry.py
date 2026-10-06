from src.analysis.registry import AnalysisToolRegistry
from src.analysis.schemas.tool import AnalysisTool

from src.analysis.tools.analyze_trend import analyze_trend
from src.analysis.tools.calculate_change import calculate_change
from src.analysis.tools.calculate_contribution import calculate_contribution
from src.analysis.tools.compare_groups import compare_groups
from src.analysis.tools.correlation_analysis import correlation_analysis
from src.analysis.tools.descriptive_statistics import descriptive_statistics
from src.analysis.tools.detect_outliers import detect_outliers
from src.analysis.tools.distribution_statistics import distribution_statistics
from src.analysis.tools.frequency_analysis import frequency_analysis
from src.analysis.tools.group_statistics import group_statistics
from src.analysis.tools.percentage_change_analysis import (
    percentage_change_analysis,
)
from src.analysis.tools.rank_categories import rank_categories
from src.analysis.tools.share_distribution import share_distribution
from src.analysis.tools.top_bottom_analysis import top_bottom_analysis


def build_analysis_tool_registry() -> AnalysisToolRegistry:
    """
    Build the registry containing all analysis tools
    currently available to NEXA.
    """

    registry = AnalysisToolRegistry()

    registry.register(
        definition=AnalysisTool(
            name="rank_categories",
            description=(
                "Ranks categories according to the value "
                "of a numeric metric."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={
                "order": {
                    "type": "string",
                    "allowed_values": [
                        "ascending",
                        "descending",
                    ],
                    "default": "descending",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "optional": True,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=rank_categories,
    )

    registry.register(
        definition=AnalysisTool(
            name="compare_groups",
            description=(
                "Compares groups using a numeric metric "
                "and identifies the highest, lowest, "
                "and difference."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={
                "groups": {
                    "type": "array",
                    "optional": True,
                    "minimum_items": 2,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=compare_groups,
    )

    registry.register(
        definition=AnalysisTool(
            name="calculate_contribution",
            description=(
                "Calculates the contribution of a specific "
                "category to the total metric."
            ),
            required_semantics=[
                "metric",
                "dimension",
                "category",
            ],
            argument_schema={
                "category": {
                    "type": "any",
                    "required": True,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=calculate_contribution,
    )

    registry.register(
        definition=AnalysisTool(
            name="descriptive_statistics",
            description=(
                "Calculates basic descriptive statistics "
                "for a numeric metric."
            ),
            required_semantics=[
                "metric",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=descriptive_statistics,
    )

    registry.register(
        definition=AnalysisTool(
            name="distribution_statistics",
            description=(
                "Analyzes the spread and distribution of "
                "a numeric metric."
            ),
            required_semantics=[
                "metric",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=distribution_statistics,
    )

    registry.register(
        definition=AnalysisTool(
            name="analyze_trend",
            description=(
                "Analyzes whether a numeric metric is "
                "increasing, decreasing, or stable "
                "across chronological periods."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=analyze_trend,
    )

    registry.register(
        definition=AnalysisTool(
            name="calculate_change",
            description=(
                "Calculates absolute and percentage change "
                "between two specific dimension values."
            ),
            required_semantics=[
                "metric",
                "dimension",
                "start",
                "end",
            ],
            argument_schema={
                "start": {
                    "type": "any",
                    "required": True,
                },
                "end": {
                    "type": "any",
                    "required": True,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=calculate_change,
    )

    registry.register(
        definition=AnalysisTool(
            name="detect_outliers",
            description=(
                "Detects statistical outliers in a numeric "
                "metric using the IQR method."
            ),
            required_semantics=[
                "metric",
            ],
            argument_schema={
                "dimension": {
                    "type": "string",
                    "optional": True,
                },
                "multiplier": {
                    "type": "number",
                    "minimum": 0,
                    "default": 1.5,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=detect_outliers,
    )

    registry.register(
        definition=AnalysisTool(
            name="correlation_analysis",
            description=(
                "Measures the strength and direction of the "
                "linear relationship between two numeric metrics."
            ),
            required_semantics=[
                "metric_x",
                "metric_y",
            ],
            argument_schema={
                "metric_x": {
                    "type": "string",
                    "required": True,
                },
                "metric_y": {
                    "type": "string",
                    "required": True,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=correlation_analysis,
    )

    registry.register(
        definition=AnalysisTool(
            name="group_statistics",
            description=(
                "Calculates descriptive statistics separately "
                "for each category or group."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=group_statistics,
    )

    registry.register(
        definition=AnalysisTool(
            name="top_bottom_analysis",
            description=(
                "Identifies the top and bottom categories "
                "according to a numeric metric."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 3,
                },
            },
            evidence_type="AnalysisEvidence",
        ),
        execute=top_bottom_analysis,
    )

    registry.register(
        definition=AnalysisTool(
            name="percentage_change_analysis",
            description=(
                "Calculates percentage changes between "
                "consecutive chronological periods."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=percentage_change_analysis,
    )

    registry.register(
        definition=AnalysisTool(
            name="share_distribution",
            description=(
                "Calculates each category's share and "
                "cumulative share of a numeric metric."
            ),
            required_semantics=[
                "metric",
                "dimension",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=share_distribution,
    )

    registry.register(
        definition=AnalysisTool(
            name="frequency_analysis",
            description=(
                "Calculates how frequently each category "
                "occurs and its percentage of total records."
            ),
            required_semantics=[
                "dimension",
            ],
            argument_schema={},
            evidence_type="AnalysisEvidence",
        ),
        execute=frequency_analysis,
    )

    return registry