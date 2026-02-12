/**
 * Regulatory domain taxonomy — sync with backend
 */
export const REGULATORY_DOMAINS: Record<string, string> = {
  AML_KYC: 'AML/KYC, Sanctions, Beneficial Ownership, Transaction Monitoring',
  PAYMENTS: 'Payment Services, SCA, Instant Payments, Fraud, Chargeback',
  OPEN_BANKING: 'Open Banking, PSD2/PSD3, Data Sharing, Consent, API Standards',
  CRYPTO: 'Crypto-Assets, Stablecoins, MiCA, Travel Rule, DeFi',
  DORA_ICT: 'Digital Operational Resilience, ICT Risk, Third-Party Risk',
  DATA_PRIVACY: 'GDPR, Data Protection, Cross-Border Data Transfer',
  CAPITAL_PRUDENTIAL: 'Capital Requirements, CRD/CRR, Liquidity, Stress Testing',
  CONSUMER: 'Consumer Protection, Conduct, Complaints, Financial Inclusion',
  SUSTAINABILITY: 'ESG Disclosure, Taxonomy, Green Finance',
  MESSAGING: 'ISO 20022, SWIFT, Payment Messaging Standards',
};

export const UPDATE_TYPES: Record<string, string> = {
  new_regulation: 'Yeni düzenleme/kanun yayınlandı',
  amendment: 'Mevcut düzenlemeye değişiklik',
  rts_its: 'Teknik standart (RTS/ITS) taslağı veya finali',
  guideline: 'Kılavuz/rehber yayını',
  consultation: 'Kamuoyu görüşüne açılma (consultation paper)',
  enforcement: 'Yaptırım, ceza, enforcement action',
  opinion_statement: 'Resmi görüş/açıklama (opinion, statement, Q&A)',
  deadline_reminder: 'Uyum tarih hatırlatıcısı',
  mutual_evaluation: 'FATF karşılıklı değerlendirme sonucu',
  market_update: 'Pazar verisi, istatistik raporu',
};

export const SEVERITY_LEVELS: Record<string, string> = {
  critical: 'Acil aksiyon gerektirir; doğrudan ceza/lisans riski',
  high: '30 gün içinde değerlendirilmeli; önemli operasyonel etki',
  medium: '90 gün içinde planlanmalı; orta vadeli etki',
  low: 'Bilgilendirme; dolaylı veya uzun vadeli etki',
  info: 'Genel bilgi; doğrudan aksiyon gerektirmez',
};
