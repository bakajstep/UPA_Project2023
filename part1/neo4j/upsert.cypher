MERGE (mc:MC {mc_val: 'Brno-střed'});
MERGE (zsj:ZSJ {zsj_val: 'Zelný trh'})-[rel_nalezi:NALEZI]->(mc:MC {mc_val: 'Brno-střed'});
CREATE INDEX nehoda_index IF NOT EXISTS FOR (nehoda:Nehoda) on nehoda.id;

