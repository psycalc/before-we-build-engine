"""Setup for cognitive-matchmaker."""

from setuptools import setup, find_packages

setup(
    name="cognitive-matchmaker",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "temporistics-core @ file:///${PROJECT_ROOT}/temporistics-core",
        "socionics-core @ file:///${PROJECT_ROOT}/socionics-core",
        "psychosophy-core @ file:///${PROJECT_ROOT}/psychosophy-core",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-cov"],
        "simulation": ["openai>=1.0", "anthropic>=0.20"],
    },
)
