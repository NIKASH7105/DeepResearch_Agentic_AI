"""
Service layer for DeepResearch Agent
"""
from .evidence_extractor import extract_evidence, generate_cited_answer
from .pdf_generator import pdf_generator

__all__ = ["extract_evidence", "generate_cited_answer", "pdf_generator"]
