import { get } from '../api';

/**
 * Get national browsing inventory summary.
 */
export async function getHelalandet() {
  return get('/api/abin/helalandet');
}

/**
 * Get national browsing inventory with geometry.
 */
export async function getHelalandetGeometri() {
  return get('/api/abin/helalandet/geometri');
}

/**
 * Get metadata for all regions (landsdel).
 */
export async function getLandsdelMetadata() {
  return get('/api/abin/landsdel/metadata');
}

/**
 * Get browsing inventory for specific region.
 */
export async function getLandsdel(landsdelkod: string) {
  return get(`/api/abin/landsdel/${landsdelkod}`);
}

/**
 * Get browsing inventory for region with geometry.
 */
export async function getLandsdelGeometri(landsdelkod: string) {
  return get(`/api/abin/landsdel/${landsdelkod}/geometri`);
}

/**
 * Get metadata for counties in region.
 */
export async function getLanMetadata(landsdelkod: string) {
  return get(`/api/abin/landsdel/${landsdelkod}/lan/metadata`);
}

/**
 * Get browsing inventory for specific county.
 */
export async function getLan(lankod: string) {
  return get(`/api/abin/lan/${lankod}`);
}

/**
 * Get browsing inventory for county with geometry.
 */
export async function getLanGeometri(lankod: string) {
  return get(`/api/abin/lan/${lankod}/geometri`);
}

/**
 * Get metadata for ÄFO (moose management areas) in county.
 */
export async function getAfoMetadata(landsdelkod: string, lankod: string) {
  return get(`/api/abin/landsdel/${landsdelkod}/lan/${lankod}/afo/metadata`);
}

/**
 * Get browsing inventory for specific ÄFO.
 */
export async function getAfo(lankod: string, afonr: number) {
  return get(`/api/abin/lan/${lankod}/afo/${afonr}`);
}

/**
 * Get browsing inventory for ÄFO with geometry.
 */
export async function getAfoGeometri(lankod: string, afonr: number) {
  return get(`/api/abin/lan/${lankod}/afo/${afonr}/geometri`);
}

/**
 * Get metadata for stratum (sub-areas) in ÄFO.
 */
export async function getStratumMetadata(
  landsdelkod: string,
  lankod: string,
  afonr: number
) {
  return get(
    `/api/abin/landsdel/${landsdelkod}/lan/${lankod}/afo/${afonr}/stratum/metadata`
  );
}

/**
 * Get browsing inventory for specific stratum.
 */
export async function getStratum(
  lankod: string,
  afonr: number,
  delomradesnummer: number
) {
  return get(`/api/abin/lan/${lankod}/afo/${afonr}/stratum/${delomradesnummer}`);
}

/**
 * Get browsing inventory for stratum with geometry.
 */
export async function getStratumGeometri(
  lankod: string,
  afonr: number,
  delomradesnummer: number
) {
  return get(
    `/api/abin/lan/${lankod}/afo/${afonr}/stratum/${delomradesnummer}/geometri`
  );
}
