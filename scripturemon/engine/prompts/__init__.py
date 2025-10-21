"""
Scripturemon Prompts Package
Personalized prompts for each screenplay theory author.
"""

from .author_prompts import (
    AUTHOR_SPECIFIC_REQUIREMENTS,
    get_author_specific_requirements,
    build_personalized_prompt_pass1,
    build_personalized_prompt_pass2
)

__all__ = [
    'AUTHOR_SPECIFIC_REQUIREMENTS',
    'get_author_specific_requirements',
    'build_personalized_prompt_pass1',
    'build_personalized_prompt_pass2'
]
