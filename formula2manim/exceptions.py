"""Custom exceptions for Formula2Manim."""


class Formula2ManimError(Exception):
    """Base exception for all Formula2Manim errors."""
    pass


class ParseError(Formula2ManimError):
    """Raised when formula or parameter parsing fails."""
    pass


class ModelValidationError(Formula2ManimError):
    """Raised when a model's formulas or params are insufficient."""
    pass


class RenderingError(Formula2ManimError):
    """Raised when the manim subprocess fails."""
    pass


class DeepSeekAPIError(Formula2ManimError):
    """Raised when a DeepSeek API call fails."""
    pass
