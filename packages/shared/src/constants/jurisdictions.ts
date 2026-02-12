/**
 * Jurisdiction codes — used in sources and filters
 */
export const JURISDICTIONS = ['EU', 'UK', 'US', 'GLOBAL'] as const;
export type Jurisdiction = (typeof JURISDICTIONS)[number];

export const JURISDICTION_LABELS: Record<Jurisdiction, string> = {
  EU: 'European Union',
  UK: 'United Kingdom',
  US: 'United States',
  GLOBAL: 'Global',
};
