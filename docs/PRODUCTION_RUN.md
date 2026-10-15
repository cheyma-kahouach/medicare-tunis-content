# Daily production run

Goal: keep a stock of finished carousels waiting for the reviewer. Nothing here publishes anything.

Google Sheet ID: 1u8JFdxYABPWXKk75KIXKauFp1uHbcfzCrUeq2rzjYzk (use the Google Sheets connector). Times are Tunis time (Africa/Tunis, UTC+1, no daylight saving).

## Tabs
- "À valider": A N°, B Idée, C Service, D Source, E Date ajoutée, F Décision (Approuvée, Rejetée, À modifier), G Commentaire, H Statut (En attente, Carrousel créé).
- "Carrousels": A N°, B Idée, C Service, D to H Slide 1 to 5, I Légende Instagram, J Légende Facebook, K Légende TikTok, L Photo (URL), M to Q Image 1 to 5 (URLs), R Statut (Brouillon, À relire, À modifier, Prête, Programmée, Échec), S Prête (checkbox), T Publication Instagram et Facebook, U Publication TikTok, V ID Buffer, W Commentaire de la relectrice. Ignore any row whose idea starts with EXEMPLE.
- "Journal": A Date et heure Tunis, B Étape, C N° de l'idée, D Résultat, E Détail. Append one line per idea handled, skipped or failed.

## Steps
1. Read docs/brief.md in the repo fully before writing any copy.
2. Stock check. Count Carrousels rows (not EXEMPLE) with Statut À relire, À modifier or Prête. Target stock is 7. Create at most 3 new carousels per run, and none if the stock is already 7 or more. Rework requests (below) do not count toward the 3.
3. Rework first. For each Carrousels row with Statut À modifier: read the reviewer comment in column W, rewrite the affected slides or captions, rebuild the slides into a NEW folder (add a suffix like _v2 so cached images are not served), update the row (columns D to Q), set Statut À relire, tick off S (FALSE), keep the comment text.
4. New carousels. Take approved ideas in order: rows of "À valider" with Décision Approuvée and Statut En attente, lowest N° first. For each:
   a. Read the last 5 Carrousels rows for the variation rule. Write the copy per docs/brief.md and run its self check.
   b. Pick the photo using the catalog. Each service folder has a catalog.json: file name to {description, themes, subjects_black, logo, focus_y}.
      1. Update the catalog first: list the images in the idea's service folder (photos/fertilite for Fertilité, photos/chirurgie_esthetique for Chirurgie esthétique, photos/optique for Optique). For every image with no catalog entry, open it and write an entry: one sentence describing who is in it, what they do, the setting, the mood and where the empty space is; 3 to 6 theme words in French without accents; subjects_black true or false (judge by looking); logo "white" if the top centre of the photo is dark, else "dark"; focus_y (0 to 100) that keeps faces above the bottom 40 percent of a 1080x1350 slide. Commit the updated catalog with the slides. Never use an image where subjects_black is false.
      2. Exclude any photo already listed in column L of any Carrousels row (compare by file name). A used photo stays used forever.
      3. Choose from the remaining catalog entries by meaning: the best match between the idea and the description and themes, favouring a calm bottom area for the hook. Open the 1 to 3 best candidates, confirm what is really in them, and pick one. Use its logo and focus_y values as the starting point in the spec.
      4. If nothing suitable and unused remains, do not build: append a Journal line "photo manquante" and send an alert email to cheymakahouach2@gmail.com saying the library needs new photos for that service folder and theme, then stop creating carousels for this run.
   c. Write a spec JSON (see tools/build_carousel.py docstring) and run `python3 tools/build_carousel.py spec.json`. Needs python3 with playwright, chromium and ImageMagick `convert`; if playwright is missing run `pip install playwright --break-system-packages`. Output goes to slides/<N°>_<ascii_slug>/.
   d. View slide_1.jpg and slide_3.jpg. Check: text fully inside the slide and legible, hook not covering faces (if it does, adjust focus_y in the spec and rebuild), all subjects Black. Fix and recheck at most 2 times, then skip and log.
   e. `git pull --rebase`, add, commit and `git push origin main`. Image URL pattern: https://raw.githubusercontent.com/cheyma-kahouach/medicare-tunis-content/main/<path>
   f. Append a Carrousels row after the last used row: A to C from the idea, D slide 1 text (the hook), E slide 2, F slide 3, G slide 4, H the fixed CTA, a blank line, then "WhatsApp : +216 29889633 / 98757394". I, J, K the three captions. L the photo URL. M to Q the five slide URLs. R "À relire". S FALSE. Put any source for a statistic in W. Use plain Google Sheets values (no valueInputOption argument).
   g. Set "À valider" column H to Carrousel créé for that idea. Append a Journal line (built).
5. Never stop for approval between ideas. Finish with a short summary: built, reworked, skipped and why.

## Fixed CTA (slide 5, copied verbatim, added by the builder)
La Tunisie, une destination de choix pour vos soins.

Contactez-nous dès maintenant et bénéfissiez d'une prise en charge sur mesure.
