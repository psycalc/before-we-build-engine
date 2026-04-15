"""Cognitive Matchmaker — multi-typology compatibility system."""

from cognitive_matchmaker.profile import PersonProfile, MatchResult
from cognitive_matchmaker.matcher import Matchmaker
from cognitive_matchmaker.cross_mapping import CrossTypologyMapper

__version__ = "0.1.0"
__all__ = ["PersonProfile", "MatchResult", "Matchmaker", "CrossTypologyMapper"]
