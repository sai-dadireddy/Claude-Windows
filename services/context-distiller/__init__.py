"""Context Distiller - Compress RAG documents using Nova Micro."""

try:
    from .lambda_function import (
        distill_document,
        distill_batch,
        lambda_handler,
        DistillResult,
        BatchResult,
    )

    __all__ = [
        "distill_document",
        "distill_batch",
        "lambda_handler",
        "DistillResult",
        "BatchResult",
    ]
except ImportError:
    # Running as standalone (e.g., pytest in same directory)
    pass
