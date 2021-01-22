CREATE INDEX idx_47293de1$f21_award_id_temp ON subaward_view_temp USING BTREE(award_id) WITH (fillfactor = 97);
CREATE INDEX idx_47293de1$f21_award_type_temp ON subaward_view_temp USING BTREE(award_type) WITH (fillfactor = 97) WHERE award_type IS NOT NULL;
CREATE INDEX idx_47293de1$f21_ordered_fain_temp ON subaward_view_temp USING BTREE(UPPER(fain) DESC NULLS LAST) WITH (fillfactor = 97) WHERE fain IS NOT NULL;
CREATE INDEX idx_47293de1$f21_ordered_amount_temp ON subaward_view_temp USING BTREE(amount DESC NULLS LAST) WITH (fillfactor = 97);
CREATE INDEX idx_47293de1$f21_recipient_name_temp ON subaward_view_temp USING BTREE(recipient_name) WITH (fillfactor = 97) WHERE recipient_name IS NOT NULL;
CREATE INDEX idx_47293de1$f21_action_date_temp ON subaward_view_temp USING BTREE(action_date DESC NULLS LAST) WITH (fillfactor = 97);
CREATE INDEX idx_47293de1$f21_awarding_agency_id_temp ON subaward_view_temp USING BTREE(awarding_agency_id ASC NULLS LAST) WITH (fillfactor = 97) WHERE awarding_agency_id IS NOT NULL;
CREATE INDEX idx_47293de1$f21_ordered_awarding_subtier_agency_name_temp ON subaward_view_temp USING BTREE(awarding_subtier_agency_name DESC NULLS LAST) WITH (fillfactor = 97);
CREATE INDEX idx_47293de1$f21_funding_toptier_agency_name_temp ON subaward_view_temp USING BTREE(funding_toptier_agency_name) WITH (fillfactor = 97) WHERE funding_toptier_agency_name IS NOT NULL;
CREATE INDEX idx_47293de1$f21_recipient_location_state_code_temp ON subaward_view_temp USING BTREE(recipient_location_state_code) WITH (fillfactor = 97) WHERE recipient_location_state_code IS NOT NULL;
CREATE INDEX idx_47293de1$f21_recipient_location_cong_code_temp ON subaward_view_temp USING BTREE(recipient_location_congressional_code) WITH (fillfactor = 97) WHERE recipient_location_congressional_code IS NOT NULL;
CREATE INDEX idx_47293de1$f21_pop_state_code_temp ON subaward_view_temp USING BTREE(pop_state_code) WITH (fillfactor = 97) WHERE pop_state_code IS NOT NULL;
CREATE INDEX idx_47293de1$f21_pop_congressional_code_temp ON subaward_view_temp USING BTREE(pop_congressional_code) WITH (fillfactor = 97) WHERE pop_congressional_code IS NOT NULL;
CREATE INDEX idx_47293de1$f21_type_of_contract_pricing_temp ON subaward_view_temp USING BTREE(type_of_contract_pricing) WITH (fillfactor = 97) WHERE type_of_contract_pricing IS NOT NULL;
CREATE INDEX idx_47293de1$f21_product_or_service_code_temp ON subaward_view_temp USING BTREE(product_or_service_code) WITH (fillfactor = 97) WHERE product_or_service_code IS NOT NULL;
CREATE INDEX idx_47293de1$f21_keyword_ts_vector_temp ON subaward_view_temp USING GIN(keyword_ts_vector);
CREATE INDEX idx_47293de1$f21_treasury_account_identifiers_temp ON subaward_view_temp USING GIN(treasury_account_identifiers gin__int_ops);
