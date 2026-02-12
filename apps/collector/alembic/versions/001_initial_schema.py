"""Initial schema — Bölüm 5.1: sources, raw_contents, regulatory_updates, company_profiles, impact_assessments, alert_rules, digests.

Revision ID: 001
Revises:
Create Date: RegTech Radar

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# pgvector için; extension init-db.sql'de oluşturuluyor
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.create_table(
        "sources",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("slug", sa.Text(), nullable=False, unique=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("source_type", sa.Text(), nullable=False),
        sa.Column("jurisdiction", ARRAY(sa.Text()), nullable=False),
        sa.Column("crawl_frequency", sa.Text(), nullable=False, server_default="6h"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("last_crawled_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("config_json", JSONB),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "raw_contents",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("source_id", UUID(as_uuid=True), sa.ForeignKey("sources.id")),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("title", sa.Text()),
        sa.Column("raw_html", sa.Text()),
        sa.Column("extracted_text", sa.Text()),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("published_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("crawled_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("content_hash", name="raw_contents_content_hash_key"),
    )
    op.create_index("idx_raw_hash", "raw_contents", ["content_hash"])

    op.create_table(
        "regulatory_updates",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("raw_content_id", UUID(as_uuid=True), sa.ForeignKey("raw_contents.id")),
        sa.Column("source_id", UUID(as_uuid=True), sa.ForeignKey("sources.id")),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("summary_short", sa.Text(), nullable=False),
        sa.Column("summary_long", sa.Text(), nullable=False),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("original_lang", sa.Text(), server_default="en"),
        sa.Column("domains", ARRAY(sa.Text()), nullable=False),
        sa.Column("regulations", ARRAY(sa.Text())),
        sa.Column("jurisdictions", ARRAY(sa.Text()), nullable=False),
        sa.Column("update_type", sa.Text(), nullable=False),
        sa.Column("severity", sa.Text(), nullable=False),
        sa.Column("published_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("effective_date", sa.TIMESTAMP(timezone=True)),
        sa.Column("deadline_date", sa.TIMESTAMP(timezone=True)),
        sa.Column("key_takeaways", ARRAY(sa.Text())),
        sa.Column("action_items", ARRAY(sa.Text())),
        sa.Column("affected_entities", ARRAY(sa.Text())),
        sa.Column("is_published", sa.Boolean(), server_default="false"),
        sa.Column("published_in_digest", UUID(as_uuid=True)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )
    op.execute("ALTER TABLE regulatory_updates ADD COLUMN embedding vector(1536);")
    op.create_index("idx_updates_domains", "regulatory_updates", ["domains"], postgresql_using="gin")
    op.create_index("idx_updates_jurisdictions", "regulatory_updates", ["jurisdictions"], postgresql_using="gin")
    op.create_index("idx_updates_regulations", "regulatory_updates", ["regulations"], postgresql_using="gin")
    op.create_index("idx_updates_published", "regulatory_updates", [sa.text("published_at DESC")])
    op.create_index("idx_updates_severity", "regulatory_updates", ["severity"])
    # ivfflat: boş tabloda lists=1 ile oluşturulur; veri gelince ALTER INDEX ... SET (lists=100) yapılabilir
    op.execute(
        "CREATE INDEX idx_updates_embedding ON regulatory_updates "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 1);"
    )

    op.create_table(
        "company_profiles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("company_name", sa.Text()),
        sa.Column("license_types", ARRAY(sa.Text())),
        sa.Column("jurisdictions", ARRAY(sa.Text())),
        sa.Column("domains", ARRAY(sa.Text())),
        sa.Column("entity_size", sa.Text()),
        sa.Column("services", ARRAY(sa.Text())),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "impact_assessments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("regulatory_update_id", UUID(as_uuid=True), sa.ForeignKey("regulatory_updates.id"), nullable=False),
        sa.Column("company_profile_id", UUID(as_uuid=True), sa.ForeignKey("company_profiles.id"), nullable=False),
        sa.Column("impact_score", sa.Integer(), sa.CheckConstraint("impact_score >= 0 AND impact_score <= 100"), nullable=False),
        sa.Column("impact_category", sa.Text(), nullable=False),
        sa.Column("reasoning", sa.Text(), nullable=False),
        sa.Column("recommended_actions", ARRAY(sa.Text())),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("regulatory_update_id", "company_profile_id", name="impact_assessments_update_profile_key"),
    )

    op.create_table(
        "alert_rules",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("conditions", JSONB, nullable=False),
        sa.Column("channel", sa.Text(), nullable=False, server_default="email"),
        sa.Column("channel_config", JSONB),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("last_triggered", sa.TIMESTAMP(timezone=True)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "digests",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("week_start", sa.Date(), nullable=False),
        sa.Column("week_end", sa.Date(), nullable=False),
        sa.Column("intro_text", sa.Text()),
        sa.Column("highlight_ids", ARRAY(UUID(as_uuid=True))),
        sa.Column("stats_json", JSONB),
        sa.Column("sent_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("recipient_count", sa.Integer()),
        sa.Column("open_rate", sa.Numeric(5, 4)),
        sa.Column("click_rate", sa.Numeric(5, 4)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("digests")
    op.drop_table("alert_rules")
    op.drop_table("impact_assessments")
    op.drop_table("company_profiles")
    op.drop_index("idx_updates_embedding", table_name="regulatory_updates")
    op.drop_index("idx_updates_severity", table_name="regulatory_updates")
    op.drop_index("idx_updates_published", table_name="regulatory_updates")
    op.drop_index("idx_updates_regulations", table_name="regulatory_updates")
    op.drop_index("idx_updates_jurisdictions", table_name="regulatory_updates")
    op.drop_index("idx_updates_domains", table_name="regulatory_updates")
    op.drop_table("regulatory_updates")
    op.drop_index("idx_raw_hash", table_name="raw_contents")
    op.drop_table("raw_contents")
    op.drop_table("sources")
