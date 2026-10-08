# First Mile Breach Dashboard — Master Spec

Paste this whole document into a new chat to rebuild, extend, or hand off this exact dashboard.

## Purpose
Interactive HTML dashboard for First Mile courier pickup breach data. Tracks 8 breach sub-categories week by week, flags which ones have a single fixable root cause, and shows shipper/route/DP/driver hotspots.

## Data source
CSV export per week, columns used (exact names, case-sensitive):

| Column | Use |
|---|---|
| `sub_breach_dept` | Category, format `FM: <category>` — strip the `FM: ` prefix |
| `first_attempt_date` | **The field that defines the reporting week** — see critical note below |
| `oc_date` | Order-created date. NOT used for week bucketing (see below) |
| `origin_hub_name` | Root-cause hub breakdown |
| `Driver name` | Root-cause driver breakdown |
| `shipper_name` | Top shippers table |
| `OD pair` | Top origin→destination region pairs table |
| `Dp name` / `DP name` | Top drop-point names table (casing varies by file — match case-insensitively) |

**Critical finding, don't repeat this mistake:** week bucketing must use `first_attempt_date`, not `oc_date`. Verified against known pivot totals — `first_attempt_date` gives a 100% match to each week's official grand total; `oc_date` spreads across multiple weeks and is wrong for this purpose.

## The 8 categories (fixed set, exact strings after stripping `FM: `)
```
KV late DP pickup, KV late pickup, KV late poh,
NKV late DP pickup, NKV late pickup, NKV late poh,
DP dropoff on PH, outlier
```

## Verified historical totals (for sanity-checking any rebuild)
| Week | Date range | Total |
|---|---|---:|
| W32 | 3–9 Aug | 29,492 |
| W33 | 10–16 Aug | 26,683 |
| W34 | 17–23 Aug | 21,587 |
| W35 | 24–30 Aug | 22,023 |
| W36 | 31 Aug–6 Sep | 24,524 |
| W37 | 7–13 Sep | 26,756 |

## Features built
1. **KPI cards** — Total breaches, KV total, NKV total, DP-on-PH, Outliers. Each shows week-over-week % change vs. the prior week (red = increase/worse, teal = decrease/better).
2. **Week picker dropdown** — every uploaded/seeded week is independently browsable (not just "current"), each with its own full KPI + breakdown, not merely a trend-line point.
3. **Weekly trend chart** — plain inline SVG (no external chart library — CDN scripts don't reliably load in this file-delivery context, learned this the hard way), shows last 4 weeks, dashed segment + diamond marker for the in-progress week if applicable.
4. **Ranked category list** — all 8 categories sorted by volume, each tagged:
   - "Quick win" (teal) — one hub/driver = 50%+ of that category
   - "Partial fix" (amber) — 30–50% concentrated
   - "Multi-cause" (grey) — spread out, no single fix
   - Click a row to expand top hubs/drivers behind it
   - Each row also shows its own week-over-week % change
5. **4 deep-dive tables**: Top 10 shippers, Top 10 OD pairs (by region), Top 10 DP names (blanks excluded), Top 10 drivers for late POH (KV+NKV combined) — this last one flags each driver's busiest single day, to distinguish a one-off batch spike from a real recurring pattern.
6. **CSV upload** — accepts multiple files at once, parses entirely client-side (vanilla JS, no libraries), auto-detects each row's true week via `first_attempt_date`, merges into whichever weeks are already loaded rather than replacing them.
7. **Live sync (partially built, pending setup)** — designed to sync uploads to a Google Sheet via a Google Apps Script Web App (`dashboard_backend.gs`, delivered separately), so other viewers see the same data automatically, with 30-second auto-refresh polling. **Status: `BACKEND_URL` in the HTML is still a placeholder — the user has not yet completed the Apps Script deployment and sent back the `/exec` URL.** Until then the dashboard works fine but stays local-only per device.
8. Previously built and then explicitly removed on request: an admin passcode gate on the upload panel. Do not re-add unless asked.

## Known dead ends (don't retry these)
- **Chart.js via CDN** — fails silently in this file-delivery context (no network access), which also broke everything downstream in the same script block. Replaced with hand-rolled SVG.
- **`window.storage` (Claude's built-in artifact storage)** — unreliable for this delivery method (downloaded/previewed file, not a live chat-created artifact); throws `Unexpected response type` intermittently. Replaced with the Google Sheets backend approach instead.

## User's standing preferences (apply throughout)
- Exact numbers, never rounded/approximate in reports
- Highlight increase/decrease and which categories/regions need attention
- Double-check numbers before presenting — mismatches erode trust since this goes to senior management
- Don't guess or narrate *why* a number moved — flag the number, let the human investigate
- Dashboard/table format over long paragraphs
- Normal professional tone

## Next step
Send the Google Apps Script `/exec` URL once deployed, so `BACKEND_URL` can be set and live cross-viewer sync goes active.
