"""Tests for cognitive-matchmaker."""

import pytest
from cognitive_matchmaker import Matchmaker, PersonProfile, CrossTypologyMapper


def test_person_profile():
    p = PersonProfile(
        temporistics="1P-1F-1V-2P",
        psychosophy="4221",
        socionics="LII",
        name="Alice"
    )
    assert p.name == "Alice"
    assert p.temporistics == "1P-1F-1V-2P"


def test_person_profile_json():
    p = PersonProfile(
        temporistics="1P-1F-1V-2P",
        psychosophy="4221",
        socionics="LII",
    )
    json_str = p.to_json()
    p2 = PersonProfile.from_json(json_str)
    assert p2.temporistics == p.temporistics


def test_matchmaker_predict():
    p1 = PersonProfile(
        temporistics="1P-1F-1V-2P",
        psychosophy="4221",
        socionics="LII",
        name="Alice"
    )
    p2 = PersonProfile(
        temporistics="1F-1P-2V-2P",
        psychosophy="2144",
        socionics="ESE",
        name="Bob"
    )
    
    m = Matchmaker()
    result = m.predict_compatibility(p1, p2)
    
    assert 0.0 <= result.overall_score <= 1.0
    assert 0.0 <= result.temporistics_score <= 1.0
    assert 0.0 <= result.psychosophy_score <= 1.0
    assert 0.0 <= result.socionics_score <= 1.0


def test_batch_predict():
    target = PersonProfile(
        temporistics="1P-1F-1V-2P",
        psychosophy="4221",
        socionics="LII",
    )
    
    candidates = [
        PersonProfile(temporistics="1F-1P-2V-2P", psychosophy="2144", socionics="ESE"),
        PersonProfile(temporistics="1P-2P-1F-2F", psychosophy="1111", socionics="ILI"),
    ]
    
    m = Matchmaker()
    results = m.batch_predict(target, candidates)
    
    assert len(results) == 2
    assert results[0].overall_score >= results[1].overall_score


def test_cross_typology_mapper():
    mapper = CrossTypologyMapper()
    
    mbti = mapper.socionics_to_mbti("LII")
    assert mbti == "INTJ"
    
    socionics = mapper.mbti_to_socionics("INTJ")
    assert socionics == "LII"


def test_temporistics_hypothesis():
    mapper = CrossTypologyMapper()
    profile = mapper.temporistics_to_mbti_profile("1P-1F-1V-2P")
    assert "temporal_frame" in profile
    assert "mbti_hypothesis" in profile


def test_psychosophy_hypothesis():
    mapper = CrossTypologyMapper()
    profile = mapper.psychosophy_to_mbti_profile("4221")
    assert "dominant_aspect" in profile
    assert "mbti_hypothesis" in profile


def test_harmonize_types():
    mapper = CrossTypologyMapper()
    result = mapper.harmonize_types(
        temporistics="1P-1F-1V-2P",
        psychosophy="4221",
        socionics="LII"
    )
    assert "socionics_mbti" in result
    assert "consistency_score" in result
