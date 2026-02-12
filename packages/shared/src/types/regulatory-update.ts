/**
 * Regulatory update entity — matches backend regulatory_updates table
 */
export type RegulatoryDomain =
  | 'AML_KYC'
  | 'PAYMENTS'
  | 'OPEN_BANKING'
  | 'CRYPTO'
  | 'DORA_ICT'
  | 'DATA_PRIVACY'
  | 'CAPITAL_PRUDENTIAL'
  | 'CONSUMER'
  | 'SUSTAINABILITY'
  | 'MESSAGING';

export type UpdateType =
  | 'new_regulation'
  | 'amendment'
  | 'rts_its'
  | 'guideline'
  | 'consultation'
  | 'enforcement'
  | 'opinion_statement'
  | 'deadline_reminder'
  | 'mutual_evaluation'
  | 'market_update';

export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info';

export interface RegulatoryUpdate {
  id: string;
  raw_content_id?: string;
  source_id: string;
  title: string;
  summary_short: string;
  summary_long: string;
  original_url: string;
  original_lang: string;
  domains: RegulatoryDomain[];
  regulations: string[];
  jurisdictions: string[];
  update_type: UpdateType;
  severity: Severity;
  published_at: string;
  effective_date?: string;
  deadline_date?: string;
  key_takeaways: string[];
  action_items: string[];
  affected_entities: string[];
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

export interface RegulatoryUpdateListItem extends Pick<
  RegulatoryUpdate,
  'id' | 'title' | 'summary_short' | 'original_url' | 'domains' | 'regulations' | 'jurisdictions' | 'update_type' | 'severity' | 'published_at'
> {}
