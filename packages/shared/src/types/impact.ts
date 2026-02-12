/**
 * Impact assessment — company profile vs regulatory update
 */
export type ImpactCategory = 'direct' | 'indirect' | 'monitoring';

export interface ImpactAssessment {
  id: string;
  regulatory_update_id: string;
  company_profile_id: string;
  impact_score: number; // 0-100
  impact_category: ImpactCategory;
  reasoning: string;
  recommended_actions: string[];
  created_at: string;
}

export interface CompanyProfile {
  id: string;
  user_id: string;
  company_name?: string;
  license_types: string[];
  jurisdictions: string[];
  domains: string[];
  entity_size: string;
  services: string[];
  created_at: string;
  updated_at: string;
}
