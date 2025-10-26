import { post, get } from '../api';

export interface StatistikRequest {
  geometri: string;
  omdrev?: number;
  pixelstorlek?: number;
  marktyp?: string[];
}

export interface HistogramRequest extends StatistikRequest {
  klassBredd?: number;
  antalKlasser?: number;
}

export interface FramskrivningRequest extends StatistikRequest {
  datum?: string;
}

/**
 * Get valid dates for volume projection.
 */
export async function getValidProjectionDates(): Promise<string[]> {
  return get<string[]>('/api/grunddata/valid-dates');
}

/**
 * Calculate biomass (ton dry substance/ha) for area.
 */
export async function getBiomassa(request: StatistikRequest) {
  return post('/api/grunddata/biomassa', request);
}

/**
 * Get biomass distribution histogram.
 */
export async function getBiomassaHistogram(request: HistogramRequest) {
  return post('/api/grunddata/biomassa/histogram', request);
}

/**
 * Calculate timber volume (m³sk/ha) for area.
 */
export async function getVolym(request: StatistikRequest) {
  return post('/api/grunddata/volym', request);
}

/**
 * Get volume distribution histogram.
 */
export async function getVolymHistogram(request: HistogramRequest) {
  return post('/api/grunddata/volym/histogram', request);
}

/**
 * Calculate projected volume with growth model.
 */
export async function getVolymFramskriven(request: FramskrivningRequest) {
  return post('/api/grunddata/volym-framskriven', request);
}

/**
 * Calculate basal area (m²/ha) for area.
 */
export async function getGrundyta(request: StatistikRequest) {
  return post('/api/grunddata/grundyta', request);
}

/**
 * Get basal area distribution histogram.
 */
export async function getGrundytaHistogram(request: HistogramRequest) {
  return post('/api/grunddata/grundyta/histogram', request);
}

/**
 * Calculate mean height (m) for area.
 */
export async function getMedelhojd(request: StatistikRequest) {
  return post('/api/grunddata/medelhojd', request);
}

/**
 * Get height distribution histogram.
 */
export async function getMedelhojdHistogram(request: HistogramRequest) {
  return post('/api/grunddata/medelhojd/histogram', request);
}

/**
 * Calculate mean diameter (cm) for area.
 */
export async function getMedeldiameter(request: StatistikRequest) {
  return post('/api/grunddata/medeldiameter', request);
}

/**
 * Get diameter distribution histogram.
 */
export async function getMedeldiameterHistogram(request: HistogramRequest) {
  return post('/api/grunddata/medeldiameter/histogram', request);
}
