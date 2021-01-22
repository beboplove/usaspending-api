CREATE UNIQUE INDEX idx_e4637983$8ce_id_temp ON mv_grant_award_search_temp USING BTREE(award_id) WITH (fillfactor = 97);
CREATE INDEX idx_e4637983$8ce_action_date_temp ON mv_grant_award_search_temp USING BTREE(action_date DESC NULLS LAST) WITH (fillfactor = 97);
CREATE INDEX idx_e4637983$8ce_recipient_location_county_code_temp ON mv_grant_award_search_temp USING BTREE(recipient_location_county_code) WITH (fillfactor = 97) WHERE recipient_location_county_code IS NOT NULL;
