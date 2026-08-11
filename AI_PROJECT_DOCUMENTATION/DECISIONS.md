# Architectural Decision Records (ADRs)

## ADR-001: Workspace Layout Separation
- **Status**: Accepted
- **Context**: Decouple governance and prompt engineering documentation from core application source code.
- **Decision**: Create `AI_PROJECT_DOCUMENTATION/` alongside `Lead-Intelligence-Platform/`.
- **Consequences**: Clear separation between project governance and executable software engineering code.

## ADR-002: Python Project `src` Layout
- **Status**: Accepted
- **Context**: Avoid implicit module import collisions and ensure installable package structure.
- **Decision**: Standardize on `Lead-Intelligence-Platform/src/` layout.
- **Consequences**: Requires explicit installation (`pip install -e .`) or `PYTHONPATH` recognition; prevents accidental testing against uninstalled package code.

## ADR-003: Pure Workspace Initialization
- **Status**: Accepted
- **Context**: Ensure foundational architecture and documentation are locked before writing domain logic.
- **Decision**: Initialize workspace with empty package modules (`__init__.py`) and placeholders; defer all business logic to dedicated phase implementations.
- **Consequences**: Guaranteed clean foundation; no pre-mature code bloat.
