from src.analysis.registry import AnalysisToolRegistry
from src.analysis.schemas.tool import AnalysisTool
from src.analysis.tools.rank_categories import rank_categories


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
                "Ranks categories according to the value of "
                "a numeric metric."
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

    return registry