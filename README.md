# before-we-build-engine

Simulation-based personality compatibility matching using three typological systems.

## Overview

Cognitive Matchmaker integrates:
- **Temporistics** (strategic level): Temporal experience structuring
- **Psychosophy** (operational level): Analysis, synthesis, action organization
- **Socionics** (tactical level): Information metabolism and communication

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    before-we-build-engine                     │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ temporistics │  │  psychosophy │  │   socionics  │       │
│  │    -core    │  │    -core    │  │    -core    │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│                        ↓                                    │
│              PersonaNexus (trait bridge)                    │
│              Cross-typology mapping                         │
│                        ↓                                    │
│              JPAF (simulation layer)                       │
│              Triple mechanisms for personality              │
│                        ↓                                    │
│              OASIS-sim (social layer)                       │
│              Multi-agent interaction                        │
└─────────────────────────────────────────────────────────────┘
```

## Installation

```bash
git clone https://github.com/before-we-build/before-we-build-engine.git
cd before-we-build-engine
pip install -e ".[dev]"
```

## Quick Start

```python
from cognitive_matchmaker import Matchmaker, PersonProfile

user = PersonProfile(
    temporistics="1P-2F-1V-2P",
    psychosophy="4221",
    socionics="LII"
)

partner = PersonProfile(
    temporistics="1F-1P-2V-2P",
    psychosophy="2144",
    socionics="ESE"
)

match = Matchmaker.predict_compatibility(user, partner)
print(f"Compatibility: {match.score:.2%}")
print(f"Strengths: {match.strengths}")
print(f"Challenges: {match.challenges}")
```

## Submodules

- `temporistics-core/` — Temporal frame matching
- `socionics-core/` — Intertype relation scoring
- `psychosophy-core/` — 4-aspect function blocks

## Skills

See `skills/` for agentic workflows:
- Persona generation (BFI-2 → 300-500 word narratives)
- Multi-agent simulation
- Compatibility scoring with Bradley-Terry
- Cross-typology validation

## Research

Based on:
- CogniPair (ICLR 2026): GNWT-Agent, 72% human correlation
- Love First, Know Later (NeurIPS 2025): 3-phase simulation pipeline
- JPAF: 100% MBTI alignment, personality evolution

## License

MIT
