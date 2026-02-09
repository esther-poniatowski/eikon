"""Rendering pipeline for eikon figures.

Orchestrates the full figure lifecycle: style resolution, layout building,
panel drawing, and post-processing.

Public API
----------
render_figure
    Main pipeline entry point — renders a FigureSpec to a FigureHandle.
FigureHandle
    Lightweight wrapper around a rendered figure.
RenderContext
    Internal mutable state for the pipeline.
PlotFunction
    Protocol for plot functions.
"""

from eikon.render._handle import FigureHandle
from eikon.render._pipeline import render_figure
from eikon.render._protocols import DataTransform, FigurePostProcessor, PlotFunction

__all__ = [
    "DataTransform",
    "FigureHandle",
    "FigurePostProcessor",
    "PlotFunction",
    "render_figure",
]
