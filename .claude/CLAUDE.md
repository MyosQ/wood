UPDATE THIS FILE when making architectural changes, adding patterns, or changing conventions.

# Architecture

**Three-tier**: Svelte 5 frontend → FastAPI gateway → Skogsstyrelsen OAuth2 APIs

## Backend (FastAPI)

### Patterns

**Dependency Injection**: `backend/core/dependencies.py`
- `get_settings()` - @lru_cache singleton, NEVER use os.getenv
- `get_auth_service()` - Cached auth singleton
- `get_api_client()` - Fresh client per request, shared auth
- Inject via `Depends()` in route signatures

**Exception Hierarchy**: `backend/core/exceptions.py`
- Base: `SkogsstyrelsenError(message, status_code)`
- `AuthenticationError` (401), `APIError` (502), `ConfigurationError` (500)
- Middleware auto-converts to JSON responses
- ALWAYS raise specific types, NEVER generic Exception

**Route Pattern**: See `backend/api/raster.py`
- Pydantic models for request/response
- Inject `SkogsstyrelsenClient` via `Depends(get_api_client)`
- NO try/except (middleware handles)
- Serialize: `.model_dump(by_alias=True, exclude_none=True)`

**Auth Pattern**: `backend/services/auth.py`
- Auto-refresh tokens, 5-min cache buffer
- Raises `AuthenticationError` on fail

**Logging**: `backend/core/logging.py`
- `setup_logging(debug)` in lifespan
- `get_logger(__name__)` per module
- PREFER logging.verbose over info

### Structure

```
backend/
  main.py              - Lifespan, middleware, CORS, router registration
  core/
    config.py          - Pydantic Settings singleton
    dependencies.py    - DI factories
    exceptions.py      - Exception hierarchy
    middleware.py      - Error handler + request ID
  api/                 - APIRouter per domain (raster, grunddata, abin)
  services/            - Business logic (auth, client)
  models/              - Pydantic schemas (requests, responses)
```

### Adding API Domain

1. Models in `backend/models/requests.py`
2. Create `backend/api/{domain}.py` with APIRouter
3. Routes inject client via `Depends(get_api_client)`
4. Register in `backend/main.py`: `app.include_router({domain}.router)`

## Frontend (Svelte 5)

### Patterns

**State Management**: Svelte 5 runes
- `$state` for reactive state
- `$props()` for component props
- `$effect()` for side effects (use sparingly)
- `$derived` for computed values

**API Client**: `frontend/src/lib/api.ts`
- Throws `ApiException(statusCode, errorType, message)`
- ALWAYS catch in components for error display
- Base URL from `VITE_API_BASE_URL` env var

**Component Structure**:
- `App.svelte` - Root with theme toggle
- `MapInterface.svelte` - Leaflet map, full viewport, overlays
- `MetricsPanel.svelte` - Glassmorphic panel with forest data
- Use `onMount` for async init, `onDestroy` for cleanup

**Map Pattern**: See `MapInterface.svelte`
- Leaflet with Canvas renderer (performance)
- Coordinate transforms: `wktToGeoJSON()` in `lib/utils/coordinates.ts`
- Services in `lib/services/map.ts` (config, styles, GeoJSON loading)
- WKT (SWEREF99 TM) ↔ GeoJSON (WGS84) via proj4

### Structure

```
frontend/src/
  lib/
    api.ts             - HTTP client with typed errors
    config.ts          - Frontend config
    examples.ts        - Test data (WKT polygons, land types)
    components/        - Svelte components
    services/          - Business logic (grunddata, abin, map)
    utils/             - Coordinate transforms (proj4)
    constants/         - API endpoints
```

## UI Design System

### Principles

**Simplicity First**
- Remove elements, reduce complexity
- Every element must justify existence
- NO instructions overlays, NO decorative elements
- PREFER standard patterns, native controls

**Accessibility**
- WCAG AA minimum (4.5:1 normal text, 3:1 large text)
- Semantic HTML (`<button>` not `<div onclick>`)
- Visible focus states, keyboard navigation
- ARIA only where semantic HTML insufficient

**Colors**: ALWAYS CSS variables, NEVER hardcoded
- Defined in `app.css` `:root` and `.dark`
- Use `var(--color-*)` everywhere
- Light + dark mode support required

**Glassmorphism**: Overlays only
- Pattern: `backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] shadow-glass`
- Utility classes: `.shadow-glass`, `.sr-only` (screen readers)

**Spacing**: Consistent scale
- Use 4px base: `space-y-4`, `pb-3`, `mb-2`, `mt-1`
- Max 3-4 different values per component

**Transitions**: Only where useful
- Theme switching, button hover
- NO global `*` transitions

**Map Layout**: ALWAYS full viewport
- `w-screen h-screen` on container
- Overlays with `absolute` + glassmorphism
- NEVER side-by-side/split layouts

### Svelte 5 Requirements

- Keys in `{#each}`: `{#each items as item (item.id)}`
- Use `$state`, `$props()`, `$effect()`, `$derived`
- Run `svelte-autofixer` MCP tool before committing

## External APIs

**Base**: `https://api.skogsstyrelsen.se/sksapi`
**Auth**: `https://auth.skogsstyrelsen.se/connect/token` (OAuth2)

### Endpoints

- **Raster**: `/raster/v1/*` (Sentinel-2 imagery)
- **ABIN**: `/abin/*` (Browsing inventory, hierarchical)
- **Grunddata**: `/skogligagrunddata/v1/{Biomassa|Volym|Grundyta|...}` (Forest metrics)

### Parameters

- `geometri`: WKT POLYGON/MULTIPOLYGON in SWEREF 99 TM (SRID 3006)
- `marktyp[]`: `ProduktivSkogsmark`, `ImproduktivSkogsmark`, `AllSkogsmark`, `OvrigMark`, `AllMark`
- `omdrev`: 1=2008-2016, 2=2018-2025, 3=2025-2032
- `pixelstorlek`: Pixel size in meters

## Configuration

**Backend**: `.env` at root
- `SKOGSSTYRELSEN_CLIENT_ID`, `SKOGSSTYRELSEN_CLIENT_SECRET` (required)
- `DEBUG=true`, `REQUEST_TIMEOUT=30.0` (optional)

**Frontend**: `.env` in `frontend/`
- `VITE_API_BASE_URL=http://localhost:8000`

## Running

```bash
# Backend (port 8000)
uv run skog-api

# Frontend (port 5173)
cd frontend && npm run dev

# Debug mode
DEBUG=true uv run skog-api
```

## Critical Rules

- NEVER commit `.env` files
- NEVER expose secrets to frontend
- ALWAYS use backend as proxy for Skogsstyrelsen APIs
- ALWAYS validate WKT geometry before API calls
- ALWAYS use type hints (Python), TypeScript strict mode
- ALWAYS use `uv add` for Python packages (not manual pyproject.toml edits)
- ALWAYS test on all platforms (Windows, macOS, Linux)

## Development

- DRY, SOLID, YAGNI principles
- Imports at top, document params
- Unit tests in correct locations
- Logging over print statements
- Guard clauses over nested conditionals
- Composition over inheritance
- Let exceptions propagate (don't catch everything)
- Specific exception types over generic