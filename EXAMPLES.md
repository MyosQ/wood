# API Usage Examples

This document shows how to use the Skogsstyrelsen API endpoints from the frontend.

## Quick Start

1. **Start the backend:**
   ```bash
   uv run skog-api
   ```

2. **Start the frontend:**
   ```bash
   cd frontend && npm run dev
   ```

3. **Visit http://localhost:5173** and try the interactive examples!

## Example Components

Two example components are included in the frontend:

- **GrunddataExample** - Forest metrics (biomass, volume)
- **AbinExample** - Browsing inventory data

## Available Endpoints

### Forest Metrics (Grunddata)

All endpoints in `/api/grunddata`:

#### Basic Statistics
- `POST /biomassa` - Biomass (ton dry substance/ha)
- `POST /volym` - Timber volume (m³sk/ha)
- `POST /grundyta` - Basal area (m²/ha)
- `POST /medelhojd` - Mean height (m)
- `POST /medeldiameter` - Mean diameter (cm)

#### Histograms
- `POST /biomassa/histogram`
- `POST /volym/histogram`
- `POST /grundyta/histogram`
- `POST /medelhojd/histogram`
- `POST /medeldiameter/histogram`

#### Projection
- `GET /valid-dates` - Get valid projection dates
- `POST /volym-framskriven` - Project volume to future date

### Browsing Inventory (ABIN)

All endpoints in `/api/abin`:

#### National
- `GET /helalandet` - National summary
- `GET /helalandet/geometri` - National summary with WKT

#### Regional
- `GET /landsdel/metadata` - List regions
- `GET /landsdel/{code}` - Region summary
- `GET /landsdel/{code}/geometri` - Region with WKT

#### County
- `GET /landsdel/{region}/lan/metadata` - List counties
- `GET /lan/{code}` - County summary
- `GET /lan/{code}/geometri` - County with WKT

#### ÄFO (Moose Management)
- `GET /landsdel/{region}/lan/{county}/afo/metadata` - List ÄFO areas
- `GET /lan/{county}/afo/{number}` - ÄFO summary
- `GET /lan/{county}/afo/{number}/geometri` - ÄFO with WKT

#### Stratum (Sub-areas)
- `GET /landsdel/{region}/lan/{county}/afo/{afo}/stratum/metadata`
- `GET /lan/{county}/afo/{afo}/stratum/{number}`
- `GET /lan/{county}/afo/{afo}/stratum/{number}/geometri`

### Raster (Sentinel-2)

All endpoints in `/api/raster`:

- `POST /scl/histogram-date-summary` - Find available dates
- `POST /scl/histogram-by-bkid` - SCL histogram for grid
- `GET /api-info` - API metadata

## Usage Examples

### TypeScript/Frontend

```typescript
import { getBiomassa, getVolym } from './lib/services/grunddata';
import { EXAMPLE_SMALL_AREA, LAND_TYPES } from './lib/examples';

// Calculate forest metrics
const result = await getBiomassa({
  geometri: EXAMPLE_SMALL_AREA,
  marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
  pixelstorlek: 2,
});

console.log(result.data);
```

### cURL

```bash
# Get national browsing data
curl http://localhost:8000/api/abin/helalandet

# Calculate biomass
curl -X POST http://localhost:8000/api/grunddata/biomassa \
  -H "Content-Type: application/json" \
  -d '{
    "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
    "marktyp": ["ProduktivSkogsmark"],
    "pixelstorlek": 2
  }'

# Get valid projection dates
curl http://localhost:8000/api/grunddata/valid-dates
```

### Python

```python
import httpx

# Get browsing data for Stockholm
response = httpx.get("http://localhost:8000/api/abin/lan/01")
data = response.json()
print(data)

# Calculate volume
response = httpx.post(
    "http://localhost:8000/api/grunddata/volym",
    json={
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "marktyp": ["ProduktivSkogsmark"],
        "pixelstorlek": 2,
    }
)
data = response.json()
print(data)
```

## Test Data

### Example WKT Geometries

All in SWEREF 99 TM (SRID 3006):

```typescript
// Small area (~50 ha) - Quick tests
EXAMPLE_SMALL_AREA = 'POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))';

// Medium area (~200 ha) - Histograms
EXAMPLE_MEDIUM_AREA = 'POLYGON ((633000 6580000, 634500 6580000, 634500 6581500, 633000 6581500, 633000 6580000))';

// Large area (~1000 ha) - Use pixelstorlek: 10
EXAMPLE_LARGE_AREA = 'POLYGON ((475000 6750000, 478000 6750000, 478000 6753000, 475000 6753000, 475000 6750000))';
```

### Land Types

```typescript
LAND_TYPES = {
  PRODUCTIVE_FOREST: 'ProduktivSkogsmark',
  UNPRODUCTIVE_FOREST: 'ImproduktivSkogsmark',
  ALL_FOREST: 'AllSkogsmark',
  OTHER_LAND: 'OvrigMark',
  ALL_LAND: 'AllMark',
};
```

### Common Counties

```typescript
COUNTIES = {
  STOCKHOLM: '01',
  UPPSALA: '03',
  SODERMANLAND: '04',
  DALARNA: '20',
  VASTERBOTTEN: '24',
  NORRBOTTEN: '25',
  // ... see frontend/src/lib/examples.ts for full list
};
```

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

All endpoints return structured errors:

```json
{
  "detail": "Error message",
  "type": "api_error",
  "status_code": 502
}
```

Error types:
- `authentication_error` - OAuth2 failed
- `api_error` - Skogsstyrelsen API error
- `configuration_error` - Missing credentials
- `network_error` - Connection failed

## Tips

1. **For large areas** (>100 ha): Use `pixelstorlek: 10` for better performance
2. **Histograms**: Adjust `klassBredd` and `antalKlasser` for desired granularity
3. **Scanning period**: Leave `omdrev` empty to use latest available data
4. **Land types**: Start with `ProduktivSkogsmark` for forest metrics
5. **Development**: Use `DEBUG=true uv run skog-api` for detailed logging
