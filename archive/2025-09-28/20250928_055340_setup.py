from setuptools import setup, find_packages

setup(
    name="scripturemon-champion-bm25",
    version="1.0.0",
    description="ScriptureMonChampion com BM25 - Refatorado por ChatGPT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],  # Zero dependências externas
    entry_points={
        "console_scripts": [
            "scripturemon=scripturemon_champion.cli:main",
        ],
    },
)