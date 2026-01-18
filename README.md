# groceries_cli
A vibe coded helper for grocery shopping

## Structure
groceries_cli/
│
├── cli.py              # CLI entry point & command definitions
├── models.py           # Data models (Recipe, Pantry...)
├── storage.py          # Load/save data (JSON or SQLite)
├── recipes.py          # Recipe CRUD logic
├── pantry.py           # Pantry CRUD logic
├── planner.py          # Meal planning & aggregation logic
├── units.py            # Unit normalization & conversion
├── utils.py            # Shared helpers
└── data/
    └── data.json       # Persistent data

## Incremental development
### Phase 1 – MVP
 - Add/list recipes
 - Add/list pantry
 - Generate shopping list (no unit conversion)

### Phase 2
 - Better CLI UX
 - Recipe editing/deleting
 - Persistent meal plans

### Phase 3
 - Unit conversions
 - Ingredient aliases (e.g. “bell pepper” vs “capsicum”)
 - Export shopping list (CSV / Markdown)