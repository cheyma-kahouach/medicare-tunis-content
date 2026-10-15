# Daily Buffer scheduling run

Goal: schedule every carousel the reviewer approved into Buffer, one per day, on Instagram, Facebook and TikTok. Nothing is posted by hand.

Google Sheet ID: 1u8JFdxYABPWXKk75KIXKauFp1uHbcfzCrUeq2rzjYzk. Tab "Carrousels" columns are described in docs/PRODUCTION_RUN.md. Ignore rows whose idea starts with EXEMPLE.

## Rules
- Time zone Africa/Tunis (UTC+1, offset +01:00).
- Instagram and Facebook at 19:00, TikTok at 18:30, one carousel per day, first date 17 octobre 2026.
- Order: top row of the Carrousels tab first.
- Condition: Statut Prête AND checkbox S ticked. Only these rows.
- Never schedule a row whose Statut is Programmée, À relire, À modifier, Brouillon or Échec.

## Steps
1. Read Carrousels A to W. Find the Prête rows with S ticked, in order.
2. Find the last scheduled date: the latest date written in column T or U among Programmée rows. Each new carousel gets the next day after it. The first date is never before 2026-10-17 and never before tomorrow (Tunis).
3. Buffer: call get_account (use currentTime and the organization), then list_channels. Find the Instagram, Facebook and TikTok channels. Never guess channel IDs.
4. For each Prête row, create 3 posts with create_post, mode customScheduled and dueAt in ISO 8601 with +01:00, schedulingType automatic:
   - Instagram: text from column I, assets the 5 images from M to Q in order (each as { image: { url } }), metadata.instagram { type: "post", shouldShareToFeed: true }, dueAt date at 19:00.
   - Facebook: text from column J, same 5 images, metadata.facebook { type: "post" }, dueAt same date at 19:00.
   - TikTok: text from column K, same 5 images, metadata.tiktok { title: the hook from column D truncated to 90 characters }, dueAt same date at 18:30.
   Add altText to each image (slide number and idea).
5. If all three posts are created, update the row: R Programmée, T the date and time (for example 2026-10-17 19:00), U the TikTok date and time, V the Buffer post IDs. If a post fails, set R Échec, write the error in W, do not retry in a loop, and tell the user in the final message.
6. Append a Journal line per carousel (étape "Programmation").
7. Empty queue alert. After scheduling, compute the last scheduled date. If the last scheduled date is earlier than the day after tomorrow (Tunis), meaning less than 2 days of posts are left, send an email to cheymakahouach2@gmail.com with the subject "Medicare Tunis : plus de publication prête" and a short French body saying no approved carousel is waiting and the reviewer should approve some. If the Gmail send is refused, create a draft instead and say so.
8. Final message: short list of what was scheduled (idea, date) or "rien à programmer".
