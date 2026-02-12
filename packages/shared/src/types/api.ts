/**
 * API request/response types (BFF + Public API)
 */
import type { RegulatoryUpdate, RegulatoryUpdateListItem } from './regulatory-update';
import type { ImpactAssessment } from './impact';

export interface FeedQueryParams {
  domains?: string[];
  jurisdictions?: string[];
  severity?: string[];
  from?: string;
  to?: string;
  page?: number;
  per_page?: number;
}

export interface FeedResponse {
  items: RegulatoryUpdateListItem[];
  total: number;
  page: number;
  per_page: number;
}

export interface SearchQueryParams {
  q: string;
  type?: 'semantic' | 'keyword';
  limit?: number;
}

export interface SearchResponse {
  items: RegulatoryUpdateListItem[];
}

export interface UpdateDetailResponse extends RegulatoryUpdate {}

export interface ImpactQueryParams {
  profile_id: string;
}

export type ImpactResponse = ImpactAssessment;
