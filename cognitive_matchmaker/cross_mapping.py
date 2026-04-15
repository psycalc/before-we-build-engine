"""Cross-typology mapping using MBTI/Jungian as common frame."""

from dataclasses import dataclass
from typing import Optional


class CrossTypologyMapper:
    """
    Maps between Temporistics, Psychosophy, Socionics using MBTI as bridge.
    
    This allows converting between systems for comparison and validation.
    """
    
    SOCIONICS_TO_MBTI = {
        "LII": "INTJ", "ILE": "ENTP", "ESE": "ESFJ", "SLI": "ISTP",
        "SLE": "ESTP", "LIE": "ENTJ", "EIE": "ENFJ", "LSI": "ISTJ",
        "SIE": "ESFP", "ILI": "INTP", "ESI": "ISFJ", "LSE": "ESTJ",
        "IEE": "ENFP", "EII": "INFJ", "SEI": "ISFP", "SEE": "ESFP",
    }
    
    MBTI_TO_SOCIONICS = {v: k for k, v in SOCIONICS_TO_MBTI.items()}
    
    TEMPORISTICS_TO_MBTI_HYPOTHESIS = {
        "past": {"dominant": "SJ", "characteristics": "traditional, memory-focused"},
        "present": {"dominant": "SP", "characteristics": "action-oriented, practical"},
        "future": {"dominant": "NP", "characteristics": "visionary, intuitive"},
        "eternal": {"dominant": "NF", "characteristics": "reflective, values-driven"},
    }
    
    PSYCHOSOPHY_TO_MBTI_HYPOTHESIS = {
        (4, 1): {"function": "Thinking", "direction": "Introverted"},
        (1, 4): {"function": "Feeling", "direction": "Extraverted"},
        (3, 2): {"function": "Intuition", "direction": "Extraverted"},
        (2, 3): {"function": "Sensing", "direction": "Introverted"},
    }
    
    def socionics_to_mbti(self, socionics_type: str) -> str:
        """Convert Socionics type to MBTI."""
        return self.SOCIONICS_TO_MBTI.get(socionics_type, socionics_type)
    
    def mbti_to_socionics(self, mbti_type: str) -> str:
        """Convert MBTI type to Socionics."""
        return self.MBTI_TO_SOCIONICS.get(mbti_type.upper(), mbti_type)
    
    def temporistics_to_mbti_profile(self, temporistics: str) -> dict:
        """
        Hypothesize MBTI profile from Temporistics type.
        
        This is a hypothesis based on temporal orientation patterns.
        """
        from temporistics.types import TemporalType
        
        t = TemporalType.from_string(temporistics)
        frame = t.dominant_temporal_frame()
        
        profile = self.TEMPORISTICS_TO_MBTI_HYPOTHESIS.get(
            frame,
            {"dominant": "unknown", "characteristics": "undefined"}
        )
        
        return {
            "temporistics": temporistics,
            "temporal_frame": frame,
            "mbti_hypothesis": profile,
            "confidence": "low",  # This mapping needs empirical validation
        }
    
    def psychosophy_to_mbti_profile(self, psychosophy: str) -> dict:
        """
        Hypothesize MBTI profile from Psychosophy type.
        
        Based on dominant-weakest aspect pairs.
        """
        from psychosophy.types import PsycheType, Aspect
        
        p = PsycheType.from_string(psychosophy)
        dom = p.dominant_aspect()
        weak = p.weakest_aspect()
        
        dom_strength = p.get_strength(dom)
        weak_strength = p.get_strength(weak)
        
        profile = self.PSYCHOSOPHY_TO_MBTI_HYPOTHESIS.get(
            (dom_strength, weak_strength),
            {"function": "Mixed", "direction": "Variable"}
        )
        
        return {
            "psychosophy": psychosophy,
            "dominant_aspect": dom.value,
            "weakest_aspect": weak.value,
            "mbti_hypothesis": profile,
            "confidence": "medium",
        }
    
    def harmonize_types(self, temporistics: str, psychosophy: str, socionics: str) -> dict:
        """
        Check consistency across all three type systems.
        
        Returns analysis of whether the types are mutually consistent
        based on hypothesized MBTI bridge.
        """
        soc_mbti = self.socionics_to_mbti(socionics)
        
        temp_profile = self.temporistics_to_mbti_profile(temporistics)
        psy_profile = self.psychosophy_to_mbti_profile(psychosophy)
        
        temp_hypothesis = temp_profile["mbti_hypothesis"]["dominant"]
        psy_hypothesis = psy_profile["mbti_hypothesis"]["function"]
        
        consistency_issues = []
        
        if temp_hypothesis != "unknown" and psy_hypothesis != "Mixed":
            if temp_hypothesis[:1] != psy_hypothesis[:1]:
                consistency_issues.append(
                    f"Temporistics suggests {temp_hypothesis} but Psychosophy suggests {psy_hypothesis}"
                )
        
        return {
            "socionics_mbti": soc_mbti,
            "temporistics_profile": temp_profile,
            "psychosophy_profile": psy_profile,
            "consistency_score": 1.0 - (len(consistency_issues) * 0.2),
            "consistency_issues": consistency_issues,
        }


@dataclass
class ValidationReport:
    """Report on cross-typology consistency validation."""
    person_id: str
    temporistics: str
    psychosophy: str
    socionics: str
    
    harmonized: dict
    issues: list[str]
    recommendations: list[str]
    
    def is_consistent(self) -> bool:
        """Check if all three types are mutually consistent."""
        return self.harmonized.get("consistency_score", 0) > 0.7
