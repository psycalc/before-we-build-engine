"""Main matching orchestrator combining all three typology systems."""

from cognitive_matchmaker.profile import PersonProfile, MatchResult
from cognitive_matchmaker.cross_mapping import CrossTypologyMapper


class Matchmaker:
    """
    Main orchestrator for multi-typology compatibility matching.
    
    Combines Temporistics, Psychosophy, and Socionics using weighted scoring.
    """
    
    WEIGHTS = {
        "strategic": 0.40,    # Temporistics: temporal structuring
        "operational": 0.30,   # Psychosophy: analysis/action organization
        "tactical": 0.30,     # Socionics: information metabolism
    }
    
    def __init__(self, cross_mapper: CrossTypologyMapper | None = None):
        self.cross_mapper = cross_mapper or CrossTypologyMapper()
    
    def predict_compatibility(
        self,
        profile1: PersonProfile,
        profile2: PersonProfile,
    ) -> MatchResult:
        """
        Calculate compatibility between two profiles.
        
        Args:
            profile1: First person's profile
            profile2: Second person's profile
            
        Returns:
            MatchResult with scores and analysis
        """
        from temporistics.types import TemporalType
        from temporistics.compatibility import Compatibility as TempCompat
        from psychosophy.types import PsycheType
        from psychosophy.blocks import Compatibility as PsyCompat
        from socionics.types import SocionicsType
        from socionics.relations import IntertypeRelation
        
        t1 = TemporalType.from_string(profile1.temporistics)
        t2 = TemporalType.from_string(profile2.temporistics)
        temp_score = TempCompat.calculate(t1, t2)
        
        p1 = PsycheType.from_string(profile1.psychosophy)
        p2 = PsycheType.from_string(profile2.psychosophy)
        psy_score = PsyCompat.calculate(p1, p2)
        
        s1 = SocionicsType.from_string(profile1.socionics)
        s2 = SocionicsType.from_string(profile2.socionics)
        soc_result = IntertypeRelation.between(s1, s2)
        soc_score = soc_result["compatibility_score"]
        
        result = MatchResult(
            profile1=profile1,
            profile2=profile2,
            temporistics_score=temp_score,
            psychosophy_score=psy_score,
            socionics_score=soc_score,
            strengths=self._derive_strengths(temp_score, psy_score, soc_score),
            challenges=self._derive_challenges(temp_score, psy_score, soc_score),
            description=self._generate_description(profile1, profile2, temp_score, psy_score, soc_score),
        )
        
        return result
    
    def batch_predict(
        self,
        target: PersonProfile,
        candidates: list[PersonProfile],
    ) -> list[MatchResult]:
        """
        Calculate compatibility between target and multiple candidates.
        
        Args:
            target: Person to match
            candidates: List of potential matches
            
        Returns:
            List of MatchResults sorted by overall score (descending)
        """
        results = [self.predict_compatibility(target, c) for c in candidates]
        return sorted(results, key=lambda r: r.overall_score, reverse=True)
    
    def _derive_strengths(
        self,
        temp_score: float,
        psy_score: float,
        soc_score: float,
    ) -> list[str]:
        """Derive relationship strengths from scores."""
        strengths = []
        
        if temp_score > 0.7:
            strengths.append("Compatible temporal perspectives")
        if psy_score > 0.7:
            strengths.append("Complementary approach to analysis and action")
        if soc_score > 0.7:
            strengths.append("Harmonious communication styles")
        
        if temp_score > 0.85 and psy_score > 0.85:
            strengths.append("Excellent strategic and operational alignment")
        
        if soc_score > 0.9:
            strengths.append("Natural duality in information exchange")
        
        return strengths
    
    def _derive_challenges(
        self,
        temp_score: float,
        psy_score: float,
        soc_score: float,
    ) -> list[str]:
        """Derive relationship challenges from scores."""
        challenges = []
        
        if temp_score < 0.4:
            challenges.append("Different temporal orientations may cause friction")
        if psy_score < 0.4:
            challenges.append("Conflicting approaches to decision-making")
        if soc_score < 0.4:
            challenges.append("Communication style mismatch")
        
        if temp_score < 0.3 and soc_score < 0.3:
            challenges.append("Significant coordination challenges across multiple dimensions")
        
        return challenges
    
    def _generate_description(
        self,
        p1: PersonProfile,
        p2: PersonProfile,
        temp_score: float,
        psy_score: float,
        soc_score: float,
    ) -> str:
        """Generate human-readable match description."""
        overall = self.overall_score(p1, p2)
        
        if overall > 0.8:
            quality = "highly compatible"
        elif overall > 0.6:
            quality = "moderately compatible"
        elif overall > 0.4:
            quality = "somewhat challenging"
        else:
            quality = "potentially difficult"
        
        return (
            f"{p1.name or 'Person 1'} and {p2.name or 'Person 2'} are {quality}. "
            f"Overall compatibility: {overall:.0%}. "
            f"Strategic alignment: {temp_score:.0%}, "
            f"operational harmony: {psy_score:.0%}, "
            f"tactical fit: {soc_score:.0%}."
        )
    
    @staticmethod
    def overall_score(p1: PersonProfile, p2: PersonProfile) -> float:
        """Calculate overall weighted score (convenience method)."""
        return (
            0.40 * Matchmaker._temp_score(p1, p2) +
            0.30 * Matchmaker._psy_score(p1, p2) +
            0.30 * Matchmaker._soc_score(p1, p2)
        )
    
    @staticmethod
    def _temp_score(p1: PersonProfile, p2: PersonProfile) -> float:
        from temporistics.types import TemporalType
        from temporistics.compatibility import Compatibility
        t1 = TemporalType.from_string(p1.temporistics)
        t2 = TemporalType.from_string(p2.temporistics)
        return Compatibility.calculate(t1, t2)
    
    @staticmethod
    def _psy_score(p1: PersonProfile, p2: PersonProfile) -> float:
        from psychosophy.types import PsycheType
        from psychosophy.blocks import Compatibility
        p1t = PsycheType.from_string(p1.psychosophy)
        p2t = PsycheType.from_string(p2.psychosophy)
        return Compatibility.calculate(p1t, p2t)
    
    @staticmethod
    def _soc_score(p1: PersonProfile, p2: PersonProfile) -> float:
        from socionics.types import SocionicsType
        from socionics.relations import IntertypeRelation
        s1 = SocionicsType.from_string(p1.socionics)
        s2 = SocionicsType.from_string(p2.socionics)
        return IntertypeRelation.between(s1, s2)["compatibility_score"]
