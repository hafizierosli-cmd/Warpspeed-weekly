# Weekly Warp Speed — Handoff (continue on another device)

Last updated: 2026-10-16

## 1. What this project is
First Mile "Weekly Warp Speed" breach dashboard for the Pickup Manager / Operation Excellence team.
- A single self-contained HTML page (`backend/static/index.html`) with seeded weekly data (W32–W40).
- Tracks 8 breach categories week over week, top shippers, OD pairs, drop points and drivers.
- New weeks are added by uploading a CSV in the browser (parsed locally, **not saved anywhere yet**).
- Full spec: `dashboard_master_prompt.md`.

## 2. Where everything lives
| What | Where |
|---|---|
| Original dashboard (artifact) | https://claude.ai/artifact/ATrftBRQN5fnDGT15mFQ4w |
| Repo (branch `claude/quirky-carson-w2itgj`) | https://github.com/hafizierosli-cmd/Warpspeed-weekly |
| Repo (`main`) | https://github.com/hafizierosli-cmd/Warpspeed-weekly2 |
| Substrait app | `warpspeed-weekly-2` (portal: https://app.substrait.build) |
| Substrait API URL | https://api.substrait.build |

## 3. What is done
- [x] Dashboard saved into the repo and pushed to both repos.
- [x] Substrait deploy contract scaffolded (passes `substrait-deploy.sh check`):
  - `backend/main.py` — FastAPI: serves the dashboard at `/`, `GET /health`, `GET /api/health`
  - `backend/requirements.txt`, `cicd/Dockerfile.backend` (port 8000)
  - `substrait.yaml` — description only, **no database**
  - `CLAUDE.md` — Substrait contract block (says "not linked yet")
- [x] Local test: `/health`, `/api/health`, `/` all return 200.

## 4. What is NOT done (next steps, in order)
1. **Link this folder to the Substrait app** (blocked in the cloud session: network policy blocked `api.substrait.build`).
2. **Confirm the portal app points at the right repo/branch** (`Warpspeed-weekly2` / `main`, or the branch above).
3. **Retry the build** in the portal, or run `/substrait:deploy --watch`.
4. Open the preview URL and check the dashboard loads.

## 5. How to continue on another device (Claude desktop, local)
```
git clone https://github.com/hafizierosli-cmd/Warpspeed-weekly2.git
cd Warpspeed-weekly2
```
In the built-in terminal (Ctrl+`):
```
claude plugin update substrait@substrait
```
Then in a Claude desktop session opened on that folder:
```
/substrait:ping                                  # confirm plugin works
/substrait:login https://api.substrait.build     # may say "already logged in"
/substrait:link                                  # pick existing app: warpspeed-weekly-2
/substrait:deploy --watch                        # ship it
/substrait:logs                                  # only if deployed app misbehaves
```
If git asks for credentials, sign in with your own GitHub account.

## 6. Known issues / decisions
- The first deploy failed with: *"no backend Dockerfile found"*. Fixed by the scaffold above; needs a retry.
- GitHub push from the cloud session needed the Claude GitHub App installed on the org (now fixed).
- Uploaded CSV data is browser-only. To persist weeks, either keep adding them to the seed data in `index.html`, or later add a database (`database: oceanbase` in `substrait.yaml` + Flyway migrations).
- Do not commit tokens (`sbt_…`). `.substrait/` is gitignored.
- The CSV week is bucketed by `first_attempt_date`, **not** `oc_date` (see master spec).

## 7. Quick prompt to paste into a new chat
> Continue the Weekly Warp Speed project. Read `HANDOFF.md` and `CLAUDE.md` in this repo. Goal: link to Substrait app `warpspeed-weekly-2` (API https://api.substrait.build) and deploy. Start at section 4 of HANDOFF.md.
