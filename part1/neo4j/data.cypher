// ******************************************************************************************************
// Nacteni csv souboru dane datove sady z oficialnich webovych stranek s datasety mesta Brno.
// ******************************************************************************************************
// Pro demonstracni ucely byla nactena datova sada omezena na 2000 zaznamu.
// Dale od zaznamu s číslem 66 975 se struktura dat lisi, jelikoz se jedna pouze o nehody,
// ve kterych figuruji chodci. Jelikoz takova struktura dat neni vhodna a bylo by velmi vhodne
// rozdelit takova data do dvou datovych sad, nebudou tyto zaznamy dale uvazovany.
LOAD CSV WITH HEADERS FROM "https://data.brno.cz/datasets/mestobrno::dopravn%C3%AD-nehody-traffic-accidents.csv" AS row WITH row LIMIT 2000

// ******************************************************************************************************
// Vytvoreni uzlu a jejich vlastnosti.
// ******************************************************************************************************
MERGE (nehoda:Nehoda {id: toInteger(row.id)}) ON CREATE SET nehoda.usmrceno_os = row.usmrceno_os, nehoda.tezce_raneno_os = row.tezce_raneno_os, nehoda.lehce_raneno_os = row.lehce_raneno_os, nehoda.nasledky = row.nasledky, nehoda.hmotna_skoda = row.hmotna_skoda
MERGE (mc:MC {mc_val: row.MC})
MERGE (zsj:ZSJ {zsj_val: row.ZSJ})
MERGE (misto:Misto {d: toFloat(row.d), e: toFloat(row.e)}) ON CREATE SET misto.x = toFloat(row.x), misto.y = toFloat(row.y), misto.misto_nehody = row.misto_nehody, misto.druh_komunikace = row.druh_komun, misto.situovani = row.situovani
MERGE (vozidlo:Vozidlo {id: toInteger(row.id + row.id_vozidla), druh_vozidla: row.druh_vozidla})
MERGE (osoba:Osoba {id: toInteger(row.OBJECTID)}) ON CREATE SET osoba.vek_skupina = row.vek_skupina IS NOT NULL, osoba.pohlavi = row.pohlavi IS NOT NULL, osoba.stav = row.stav_ridic IS NOT NULL, osoba.smrt = row.smrt, osoba.smrt_dny = row.smrt_dny, osoba.lehke_zraneni = row.lz, osoba.tezke_zraneni = row.tz, osoba.nasledek_text = row.nasledek IS NOT NULL, osoba.alkohol = row.alkohol, osoba.alkohol_vinik = row.alkohol_vinik
MERGE (hlavni_pricina:HlavniPricina {hlavni_pricina_val: row.hlavni_pricina})
MERGE (pricina:Pricina {pricina_val: row.pricina})
MERGE (povetrnostni_podm:PovetrnostniPodm {povetrnostni_podm_val: row.povetrnostni_podm})
MERGE (rozhled:Rozhled {rozhled_val: row.rozhled})
MERGE (stav_vozovky:StavVozovky {stav_vozovky_val: row.stav_vozovky})
MERGE (viditelnost:Viditelnost {viditelnost_val: row.viditelnost})
MERGE (zavineni:Zavineni {zavineni_val: row.zavineni})

// ******************************************************************************************************
// Vytvoreni vztahu a jejich vlastnosti.
// ******************************************************************************************************
MERGE (nehoda)-[rel_lokaci_v:LOKACI_V {datum: row.datum, den: row.den, mesic_t: row.mesic_t, rok: row.rok, mesic: row.mesic, doba: row.doba, cas: row.cas, hodina: row.hodina, den_v_tydnu: row.den_v_tydnu}]->(misto)
MERGE (misto)-[rel_spada_do:SPADA_DO]->(zsj)
MERGE (zsj)-[rel_nalezi:NALEZI]->(mc)
MERGE (nehoda)-[rel_se_zucastnilo:SE_ZUCASTNILO {srazka: row.srazka}]->(vozidlo)
MERGE (osoba)-[rel_patrila_k:PATRILA_K {vztah_k_vozidlu: row.osoba IS NOT NULL, ozn_osoba: row.ozn_osoba IS NOT NULL}]->(vozidlo)
MERGE (nehoda)-[rel_vznikla_z:VZNIKLA_Z]->(pricina)
MERGE (pricina)-[rel_zahrnuta:ZAHRNUTA]->(hlavni_pricina)
MERGE (nehoda)-[rel_se_stala_za:SE_STALA_ZA]->(povetrnostni_podm)
MERGE (nehoda)-[rel_odpovidal:ODPOVIDAL]->(rozhled)
MERGE (nehoda)-[rel_pri_stavu:PRI_STAVU]->(stav_vozovky)
MERGE (nehoda)-[rel_pri:PRI]->(viditelnost)
MERGE (nehoda)-[rel_z_duvodu:Z_DUVODU]->(zavineni);

// ******************************************************************************************************
// Vytvoreni indexu.
// ******************************************************************************************************
// Vytvareni RANGE indexu pro identifikator nehody.
CREATE INDEX nehoda_index IF NOT EXISTS FOR (nehoda:Nehoda) on nehoda.id;
// Vytvareni TEXT indexu.
CREATE TEXT INDEX mc_index IF NOT EXISTS FOR (mc:MC) ON mc.mc_val;
CREATE TEXT INDEX zsj_index IF NOT EXISTS FOR (zsj:ZSJ) ON zsj.zsj_val;
CREATE TEXT INDEX vozidlo_index IF NOT EXISTS FOR (vozidlo:Vozidlo) ON vozidlo.druh_vozidla;
CREATE TEXT INDEX osoba_alkohol_index IF NOT EXISTS FOR (osoba:Osoba) ON osoba.alkohol_vinik;
CREATE TEXT INDEX pricina_index IF NOT EXISTS FOR (pricina:Pricina) ON pricina.pricina;

