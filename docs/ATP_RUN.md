# AnswerThePublic research run

Goal: add new ideas to the "À valider" tab. Settings are in docs/ATP_SETTINGS.md. Nothing is published.

Tool: Claude in Chrome on the user's signed in AnswerThePublic account (free plan, 3 searches per day). Never expand a "People Also Ask" question (it costs 2 searches).

## Steps
1. Read docs/ATP_SETTINGS.md and the "À valider" tab (all ideas, for duplicates) and the Journal tab for the last search pairs used.
2. Pick 3 keyword and country pairs not used yet, rotating so each day covers the three services when possible (fertilité, chirurgie esthétique, optique). Countries: Côte d'Ivoire (CI), Sénégal (SN), Cameroun (CM), RD Congo (CD).
3. At https://answerthepublic.com/en type the keyword, pick French in the language box (type Fre), pick the country in the country box by its 2 letter code (for example CI), click Search. Wait about 20 seconds, then reload the report page once so the data is filled in, and read it with get_page_text.
4. Use these sections: AI Prompts (Source IA, 10 visible), Social Media (Source Réseaux sociaux), People Also Ask and Organic Searches (Source Moteurs de recherche). AI and social first.
5. Filter: drop duplicates and near duplicates of sheet ideas, price or cost questions, diagnosis style questions, other clinic or brand names, the word consultation, city lists of other countries, and results that are not about the topic.
6. Rewrite each kept idea as a short French title, no dashes. Score Potentiel social (Élevé, Moyen, Faible) on: emotional or taboo, myth versus reality, a question people ask out loud, relevance to Sub-Saharan African patients, easy to share or save.
7. Append rows to À valider: N° (next number), Idée, Service, Source, Date ajoutée (dd/mm/yyyy), Décision empty, Commentaire empty, Statut En attente, Potentiel social. Then rewrite the Rang column for all non processed rows (1 is best, Déjà traité rows last) and sort the range A2:J by column J ascending (sheetId 1001).
8. Journal line per search: date, étape "Recherche ATP", keyword and country, number of ideas added.

## Log
- 2026-10-15: pma + Côte d'Ivoire, 16 ideas added (51 to 66).
