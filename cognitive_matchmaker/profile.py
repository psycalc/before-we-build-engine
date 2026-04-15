"""Person profile combining all three typology systems."""

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class PersonProfile:
    """
    Person profile with types from all three typological systems.
    
    Required:
    - temporistics: Temporal type (e.g., "1P-1F-1V-2P")
    - psychosophy: Psyche type (e.g., "4221")
    - socionics: Socionics type (e.g., "LII")
    
    Optional:
    - name: Person identifier
    - metadata: Additional info (age, gender, preferences)
    """
    temporistics: str
    psychosophy: str
    socionics: str
    name: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate type formats."""
        from temporistics.types import TemporalType
        from psychosophy.types import PsycheType
        from socionics.types import SocionicsType
        
        TemporalType.from_string(self.temporistics)
        PsycheType.from_string(self.psychosophy)
        SocionicsType.from_string(self.socionics)
    
    def to_dict(self) -> dict:
        """Export as dictionary."""
        return {
            "name": self.name,
            "temporistics": self.temporistics,
            "psychosophy": self.psychosophy,
            "socionics": self.socionics,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PersonProfile":
        """Create from dictionary."""
        return cls(
            temporistics=data["temporistics"],
            psychosophy=data["psychosophy"],
            socionics=data["socionics"],
            name=data.get("name"),
            metadata=data.get("metadata", {}),
        )
    
    def to_json(self) -> str:
        """Export as JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "PersonProfile":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))


@dataclass
class MatchResult:
    """
    Compatibility match result between two profiles.
    
    Contains:
    - Overall score
    - Per-system scores
    - Strengths and challenges
    - Description
    """
    profile1: PersonProfile
    profile2: PersonProfile
    
    temporistics_score: float
    psychosophy_score: float
    socionics_score: float
    
    strengths: list[str] = field(default_factory=list)
    challenges: list[str] = field(default_factory=list)
    description: str = ""
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score."""
        return (
            0.40 * self.temporistics_score +
            0.30 * self.psychosophy_score +
            0.30 * self.socionics_score
        )
    
    def __str__(self) -> str:
        score = self.overall_score
        return (
            f"Match: {self.profile1.name or '?'} ↔ {self.profile2.name or '?'}\n"
            f"Overall: {score:.1%} | "
            f"Temp: {self.temporistics_score:.1%} | "
            f"Psy: {self.psychosophy_score:.1%} | "
            f"Soc: {self.socionics_score:.1%}"
        )
    
    def to_dict(self) -> dict:
        """Export as dictionary."""
        return {
            "profile1": self.profile1.to_dict(),
            "profile2": self.profile2.to_dict(),
            "overall_score": self.overall_score,
            "temporistics_score": self.temporistics_score,
            "psychosophy_score": self.psychosophy_score,
            "socionics_score": self.socionics_score,
            "strengths": self.strengths,
            "challenges": self.challenges,
            "description": self.description,
        }
