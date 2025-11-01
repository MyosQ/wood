UPDATE THIS FILE when making architectural changes, adding patterns, or changing conventions.

# Skogsstyrelsen API Gateway

Full-stack application: FastAPI backend proxies Skogsstyrelsen APIs, Svelte frontend consumes backend.

## Architecture Pattern

**Three-tier**: Svelte frontend → FastAPI gateway → Skogsstyrelsen OAuth2 APIs

## Project Structure

```
backend/
  main.py              - FastAPI app with lifespan, middleware, CORS
  core/                - Core infrastructure
    config.py          - Pydantic Settings (cached singleton)
    dependencies.py    - DI container (auth, client factories)
    exceptions.py      - Custom exception hierarchy
    logging.py         - Logging setup
    middleware.py      - Global error handler
  api/                 - Route handlers using dependency injection
    raster.py          - Example with Pydantic models
  services/            - Business logic
    auth.py            - OAuth2 token management
    skogsstyrelsen_client.py - HTTP client with error handling
  models/              - Pydantic request/response models
    requests.py        - API request schemas with validation
    responses.py       - API response schemas
frontend/
  src/
    lib/api.ts         - Typed HTTP client with ApiException
    App.svelte         - Main component with error display
apidocs/               - OpenAPI specs (read-only reference)
```

## Backend Patterns

### Configuration (Settings Pattern)

`backend/core/config.py`: Pydantic Settings
- Singleton via `@lru_cache` decorator on `get_settings()`
- Env var loading with validation
- All services receive Settings via dependency injection
- NEVER access os.getenv directly, ALWAYS use Settings

### Dependency Injection

`backend/core/dependencies.py`: Factory functions
- `get_auth_service()` - Cached singleton auth instance
- `get_api_client()` - Fresh client per request with shared auth
- Use FastAPI `Depends()` in route signatures

### Authentication Service

`backend/services/auth.py`: `SkogsstyrelsenAuth(settings: Settings)`
- Dependency-injected Settings
- Auto-refresh: tokens cached with 5-min buffer
- Structured logging on auth events
- Raises `AuthenticationError` on failure

### API Client Pattern

`backend/services/skogsstyrelsen_client.py`: `SkogsstyrelsenClient(auth, settings)`
- Dependency-injected auth and settings
- Structured error handling: catches httpx exceptions → raises `APIError`
- Debug logging on requests
- NEVER instantiate directly, use `get_api_client()` dependency

### Exception Hierarchy

`backend/core/exceptions.py`: Custom exceptions
- Base: `SkogsstyrelsenError(message, status_code)`
- `AuthenticationError` (401), `APIError` (502), `ConfigurationError` (500)
- ALWAYS raise specific exception types
- Middleware catches and converts to JSON responses

### Route Handler Pattern

`backend/api/raster.py`: Modern pattern with DI
- Use Pydantic models for request/response validation
- Inject `SkogsstyrelsenClient` via `Depends(get_api_client)`
- NO try/except needed (middleware handles all errors)
- Use `.model_dump(by_alias=True, exclude_none=True)` for serialization

ALWAYS follow this pattern for new API domains.

## Frontend Patterns

### API Client with Typed Errors

`frontend/src/lib/api.ts`: Typed HTTP client
- Base URL from `VITE_API_BASE_URL` env var
- Functions: `get<T>(endpoint)`, `post<T>(endpoint, data)`
- Throws `ApiException` with statusCode, errorType
- Parses backend error responses (detail, type fields)
- Handles network errors separately

ALWAYS catch `ApiException` in components for structured error display.

### Component Structure

`App.svelte`: Root component
- Use `onMount` for API calls on load
- Use `{#if}` blocks for conditional rendering

## UI 

### Implementation Guidelines
PREFER Tailwind utility classes for styling

ALWAYS use CSS variables for colors - NEVER hardcode color values
ALWAYS review components for **WCAG AA/AAA contrast compliance** between text and 
ALWAYS use the WCAG contrast formula (luminance ratio) to ensure **at least 4.5:1** for normal text and **3:1** for large text.background colors.
ALWAYS colors MUST come from predefined CSS variables
ALWAYS Define color palettes in CSS custom properties (`:root` or component-level)
ALWAYS use consistent spacing scales, typography scales and color scales
ALWAYS design reusable components with single responsibility


### Design Principles

**Simplicity First**
PREFER simplicity over complexity in all design decisions
PREFER fewer elements over more elements
PREFER removing features over adding features
PREFER standard UI patterns over custom designs
PREFER plain text over formatted text when possible
PREFER whitespace over visual separators
PREFER subtle over bold
PREFER understated over attention-grabbing

**Visual Hierarchy**
PREFER clarity over decoration
PREFER invisible UI - don't add chrome unless absolutely needed
PREFER Minimalistic UI - every element must justify its existence
PREFER subtle gradients over solid backgrounds
PREFER removing visual noise over adding visual interest
PREFER native browser controls over custom-styled controls

**Functionality**
ALWAYS Allow dark and light mode
ALWAYS use semantic HTML
ALWAYS provide visible focus states for keyboard navigation
ALWAYS use ARIA attributes where semantic HTML isn't sufficient
ALWAYS question if a feature is truly needed before implementing

**Constraints**
NEVER use `<div>` for interactive elements
NEVER add decorative elements that don't serve user needs
NEVER use animations unless they improve usability
NEVER add complexity for aesthetic reasons alone

#### Map Layout Patterns
ALWAYS display map full width and full height of the viewing port. For example: `w-screen h-screen` or `w-full h-full`. Edit any parent container to allow this.
ALWAYS let UI elements overlay the map and be liquid glass
NEVER use side-by-side or split-screen layouts with the map

#### Liquid Glass (Glassmorphism)
- Frosted glass effect with backdrop blur
- Semi-transparent backgrounds with subtle opacity
- Layered depth with soft shadows
- Light borders for definition
- Smooth transitions and animations
- Apply glassmorphism: `backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)]`

### UI Review Checklist

When reviewing UI implementations, prioritize these questions in order:

1. **Can it be simpler?** - Remove elements, reduce complexity
2. **Is every element necessary?** - Justify each component's existence
3. **Can we use standard patterns?** - Avoid custom designs when possible
4. **Is it accessible?** - WCAG compliance, keyboard navigation, ARIA
5. **Does it work in both themes?** - Light and dark mode support
6. **Are colors from CSS variables?** - No hardcoded colors
7. **Is the hierarchy clear?** - Visual importance matches functional importance
8. **Can animations be removed?** - Only keep if they improve usability


## Configuration

### Backend

- `.env` at project root
- Required: `SKOGSSTYRELSEN_CLIENT_ID`, `SKOGSSTYRELSEN_CLIENT_SECRET`
- Optional: `DEBUG=true`, `REQUEST_TIMEOUT=30.0`
- Loaded via Pydantic Settings, validated on startup
- Access via `get_settings()` dependency

### Frontend

- `.env` in `frontend/` directory
- `VITE_API_BASE_URL=http://localhost:8000`
- Access via `import.meta.env.VITE_*`

## API Integration Flow

1. Frontend calls `get('/api/raster/...')`
2. Hits FastAPI route in `backend/api/raster.py`
3. FastAPI injects `SkogsstyrelsenClient` via `Depends(get_api_client)`
4. Client calls `auth.get_token()` (singleton, cached if valid)
5. Client makes authenticated request to Skogsstyrelsen
6. On error: raises `APIError` → middleware converts to JSON response
7. On success: response proxied back to frontend
8. Frontend catches `ApiException` with typed error info

## External API Details

Base URL: `https://api.skogsstyrelsen.se/sksapi`
Auth URL: `https://auth.skogsstyrelsen.se/connect/token`

### Raster API (Sentinel-2)

- POST `/raster/v1/scl/histogramdatesummary` - Date availability
- POST `/raster/v1/SclHistogramByBkid` - Grid histogram
- GET `/raster/v1/api-info` - API metadata

### ABIN API (Browsing Inventory)

Hierarchical: country → landsdel → län → ÄFO → stratum
- GET endpoints with path params
- Append `/geometri` for WKT data
- Metadata endpoints list available codes

### Grunddata API (Forest Metrics)

- POST `/skogligagrunddata/v1/{Biomassa|Volym|Grundyta|Medelhojd|Medeldiameter}`
- All accept `geometri` (WKT), `marktyp[]`, `pixelstorlek`, `omdrev`
- Histogram endpoints: add `/Histogram` suffix with `klassBredd`, `antalKlasser`

### Common Parameters

- `geometri`: WKT POLYGON/MULTIPOLYGON in SWEREF 99 TM (SRID 3006)
- `marktyp`: Array from `ProduktivSkogsmark`, `ImproduktivSkogsmark`, `AllSkogsmark`, `OvrigMark`, `AllMark`
- `omdrev`: 1=2008-2016, 2=2018-2025, 3=2025-2032
- Dates: ISO 8601 `YYYY-MM-DDTHH:MM:SS`

## Critical Rules

- NEVER commit `.env` files (already gitignored)
- NEVER expose client secret to frontend
- ALWAYS use backend as proxy, NEVER call Skogsstyrelsen directly from frontend
- ALWAYS validate WKT geometry before sending to APIs
- ALWAYS handle HTTPException in routes, return meaningful errors

## Running

Backend: `uv run skog-api` (port 8000)
Frontend: `cd frontend && npm run dev` (port 5173)

Development mode: `DEBUG=true uv run skog-api` (enables auto-reload and debug logging)

Run both simultaneously in separate terminals.

## Adding New API Domain

1. Create Pydantic request models in `backend/models/requests.py`
2. Create `backend/api/{domain}.py` with APIRouter
3. Add routes: inject client via `Depends(get_api_client)`, use Pydantic models
4. Import and register in `backend/main.py`: `app.include_router({domain}.router)`
5. Call from Svelte components via `api.ts`, catch `ApiException` for errors

## Logging

Backend uses structured logging via `backend/core/logging.py`:
- `setup_logging(debug)` called in app lifespan
- `get_logger(__name__)` in each module
- Auth service logs token refresh events
- Client logs request/response at DEBUG level
- Middleware logs all unhandled errors

Frontend errors display in UI with error type/message.

# Development Guidelines

## Always

- ALWAYS put imports at the top
- ALWAYS document all params
- ALWAYS adhere to DRY, SOLID, YAGNI principles
- ALWAYS create unit tests for new functions, in the correct location
- ALWAYS use logging instead of print statements
- ALWAYS make sure code works on all platforms (Windows, macOS, Linux)

## Prefer

- PREFER to let exceptions propagate naturally instead of catching everything locally
- PREFER to avoid fallbacks in case stuff doesn't work, generally assume that it works
- PREFER early exit in functions (guard clauses)
- PREFER raising an exception instead of using asserts
- PREFER composition over inheritance
- PREFER explicit over implicit behavior
- PREFER immutable data structures when possible
- PREFER specific exception types over generic Exception

## Python-Specific Guidelines

### Always

- ALWAYS use uv for python and package management. (When adding package, don't just change pyproject.toml, run uv add ...)
- ALWAYS use type hints for function parameters and return values
- ALWAYS use built-in types for hints (dict, list, set) instead of typing.Dict, typing.List, typing.Set
- ALWAYS use `from __future__ import annotations` if forward references are needed
- ALWAYS follow PEP 8 and project-specific formatting rules (configured in pyproject.toml)

### Prefer

- PREFER logging.verbose over info, logger.exception over logger.error

### Hints

- Use custom dev scripts defined in pyproject.toml for checking, testing etc.

## Svelte-Specific Guidelines

You are able to use the Svelte MCP server, where you have access to comprehensive Svelte 5 and SvelteKit documentation. Here's how to use the available tools effectively:

### Available MCP Tools:

#### 1. list-sections

Use this FIRST to discover all available documentation sections. Returns a structured list with titles, use_cases, and paths.
When asked about Svelte or SvelteKit topics, ALWAYS use this tool at the start of the chat to find relevant sections.

#### 2. get-documentation

Retrieves full documentation content for specific sections. Accepts single or multiple sections.
After calling the list-sections tool, you MUST analyze the returned documentation sections (especially the use_cases field) and then use the get-documentation tool to fetch ALL documentation sections that are relevant for the user's task.

#### 3. svelte-autofixer

Analyzes Svelte code and returns issues and suggestions.
You MUST use this tool whenever writing Svelte code before sending it to the user. Keep calling it until no issues or suggestions are returned.

#### 4. playground-link

Generates a Svelte Playground link with the provided code.
After completing the code, ask the user if they want a playground link. Only call this tool after user confirmation and NEVER if code was written to files in their project.
