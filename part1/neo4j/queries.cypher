// ******************************************************************************************************
// Dotaz 1 - pocet nehod v dane mestske casti serazene od nejvyssiho poctu pro zobrazeni prvních 20-ti záznamu
// ******************************************************************************************************
MATCH (mc:MC)<-[:NALEZI]-(:ZSJ)<-[:SPADA_DO]-(:Misto)<-[:LOKACI_V]-(:Nehoda)
RETURN mc.mc_val  AS mestska_cast, count(mc) AS pocet
ORDER BY count(mc) DESC
LIMIT 20;

// ******************************************************************************************************
// Dotaz 2 - nehody, ktere se staly v noci pri zhorsene viditelnosti vlivem povetrnostnich podminek
// ******************************************************************************************************
MATCH (v:Viditelnost {viditelnost_val: 'v noci - s veřejným osvětlením, zhoršená viditelnost vlivem povětrnostních podmínek (mlha, déšť, sněžení apod.)'})<-[p:PRI]-(n:Nehoda)
RETURN *;

// ******************************************************************************************************
// Dotaz 3 - nehody, ktere se staly v mestske casti Brno-Královo pole
// ******************************************************************************************************
MATCH path = (:MC {mc_val: 'Brno-Královo Pole'})<-[:NALEZI]-(:ZSJ)<-[:SPADA_DO]-(:Misto)<-[:LOKACI_V]-(:Nehoda)
RETURN path;

// ******************************************************************************************************
// Dotaz 4 - mista v mestske casti Brno-Královo pole, kde doslo k nehode z duvodu zavady na komunikaci
// ******************************************************************************************************
MATCH path = (:MC {mc_val: 'Brno-Královo Pole'})<-[:NALEZI]-(:ZSJ)<-[:SPADA_DO]-(:Misto)<-[:LOKACI_V]-(:Nehoda)-[:Z_DUVODU]-(:Zavineni {zavineni_val: 'závadou komunikace'})
RETURN path;

// ******************************************************************************************************
// Dotaz 5 - nehody, jejich mista a zakladni sidelni jednotky v mestske casti Brno-střed, ve kterych
// se stala dopravni nehoda, ktere se zucastnila tramvaj, pricemz nehoda byla zavinena ridicem motoroveho
// vozidla (at jiz tramvaje ci druheho vozidla)
// ******************************************************************************************************
MATCH path = (:MC {mc_val: 'Brno-střed'})<-[:NALEZI]-(:ZSJ)<-[:SPADA_DO]-(:Misto {situovani: 'na kolejích tramvaje'})<-[:LOKACI_V]-(:Nehoda)-[:Z_DUVODU]-(:Zavineni {zavineni_val: 'řidičem motorového vozidla'})
RETURN path;

