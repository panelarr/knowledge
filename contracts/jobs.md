---
title: Jobs API (shared shape)
status: draft
tags: [contract, jobs, admin]
related: [planning/features/FEAT-0002-jobs-page-in-every-admin.md, contracts/mihon-source-api.md, contracts/metadata-plugin.md]
inputs: [IN-0032]
updated: 2026-10-11
---

# Jobs API (shared shape)

## Summary

The one job and run model every Panelarr admin uses ([FEAT-0002](../planning/features/FEAT-0002-jobs-page-in-every-admin.md)). Each service declares it in its own admin package (`panelarr.mihon.v1.MihonJobsService`, `panelarr.meta.v1.MetaJobsService`) with **identical messages and REST paths**, so a shared `panelarr.jobs.v1` can be extracted later without breaking clients. Draft: the first implementing session refines it and REPORTs; the second copies it.

## Service sketch

```proto
service JobsService {                                   // MihonJobsService / MetaJobsService
  rpc ListJobs(ListJobsRequest) returns (ListJobsResponse);             // GET  /v1/admin/jobs
  rpc GetJob(GetJobRequest) returns (GetJobResponse);                   // GET  /v1/admin/jobs/{job_id}
  rpc ListJobRuns(ListJobRunsRequest) returns (ListJobRunsResponse);    // GET  /v1/admin/jobs/{job_id}/runs?page_size&page_token&status
  rpc GetJobRun(GetJobRunRequest) returns (GetJobRunResponse);          // GET  /v1/admin/job-runs/{run_id}
  rpc RunJob(RunJobRequest) returns (RunJobResponse);                   // POST /v1/admin/jobs/{job_id}:run
  rpc CancelJobRun(CancelJobRunRequest) returns (CancelJobRunResponse); // POST /v1/admin/job-runs/{run_id}:cancel
}

message Job {
  string id = 1;                 // stable, ^[a-z0-9][a-z0-9._-]*$ (no ":"), e.g. "store-refresh", "source-health", "sync.mangabaka.dump", "rebuild-entries"
  string name = 2;               // human label
  string description = 3;
  Schedule schedule = 4;
  bool running = 5;
  string current_run_id = 6;     // when running
  JobRunSummary last_run = 7;
  google.protobuf.Timestamp next_run_at = 8;  // unset if manual-only or disabled
  bool cancellable = 9;
  repeated JobParam params = 10; // what RunJob accepts (e.g. force, store_id, source_ids)
  string group = 11;             // UI grouping, e.g. "Stores", "Providers", "Maintenance"
}

message Schedule {
  oneof kind { string cron = 1; google.protobuf.Duration interval = 2; }  // neither = manual only
  bool enabled = 3;
  string source = 4;             // where it is configured, e.g. "MIHON_STORE_REFRESH_INTERVAL" (read-only in the UI)
}

message JobParam { string name = 1; string type = 2; /* bool|int|string|string_list */ string description = 3; bool required = 4; string default = 5; }

enum JobRunStatus { JOB_RUN_STATUS_UNSPECIFIED = 0; JOB_RUN_STATUS_RUNNING = 1; JOB_RUN_STATUS_SUCCEEDED = 2; JOB_RUN_STATUS_FAILED = 3; JOB_RUN_STATUS_CANCELLED = 4; JOB_RUN_STATUS_SKIPPED = 5; }
enum JobTrigger   { JOB_TRIGGER_UNSPECIFIED = 0; JOB_TRIGGER_SCHEDULE = 1; JOB_TRIGGER_MANUAL = 2; JOB_TRIGGER_STARTUP = 3; JOB_TRIGGER_SYSTEM = 4; }

message JobRunSummary {
  string id = 1; string job_id = 2;
  JobRunStatus status = 3; JobTrigger trigger = 4;
  google.protobuf.Timestamp started_at = 5; google.protobuf.Timestamp finished_at = 6;
  string message = 7;            // one-line outcome or error
  map<string, int64> counts = 8; // e.g. {"stores": 2, "updates": 5} or {"upserts": 564155, "merges": 258068}
  string triggered_by = 9;       // principal (admin, client name) for manual runs
}

message JobRun {
  JobRunSummary summary = 1;
  map<string, string> params = 2;          // what it ran with
  repeated JobRunNote notes = 3;           // bounded (e.g. 200): warnings, errors, notable events
  JobProgress progress = 4;                // while running
}

message JobRunNote { google.protobuf.Timestamp at = 1; string level = 2; string message = 3; string ref = 4; }
message JobProgress { string phase = 1; int64 done = 2; int64 total = 3; string unit = 4; }

message RunJobRequest { string job_id = 1; map<string, string> params = 2; }
message RunJobResponse { JobRunSummary run = 1; }   // ALREADY_EXISTS (HTTP 409) with detail JobAlreadyRunning when running
message JobAlreadyRunning { string current_run_id = 1; } // google.rpc error detail
// ListJobRunsRequest.status is a JobRunStatus (REST ?status=JOB_RUN_STATUS_FAILED)
```

## Rules

- **Job IDs** match `^[a-z0-9][a-z0-9._-]*$` and **never contain `:`**: `google.api.http` transcoding treats `:x` in the last path segment as a custom verb (as in `:run`), so `/jobs/sync:mangabaka:dump` 404s, even percent-encoded (verified through vanguard by the meta session, 2026-10-11).
- **admin** scope only. Errors: unknown job → `NOT_FOUND`, already running → `ALREADY_EXISTS` (409, detail `JobAlreadyRunning{current_run_id}`), not cancellable → `FAILED_PRECONDITION`.
- **Retention:** last 100 runs per job by default (configurable); counts and notes are bounded.
- **Restart:** runs left `RUNNING` at startup become `FAILED` with message "interrupted".
- **Metrics** (ADR-0027): `<svc>_job_runs_total{job,status,trigger}`, `<svc>_job_duration_seconds{job}`, `<svc>_job_running{job}`.
- **meta:** a provider sync is a job per provider and ingestion kind (`sync.<provider>.<kind>`, param `force`); the existing sync-run API keeps working (map it onto job runs).
- **Parameterised jobs** declare `params`; the UI renders a small form before "Run now".
- **Scheduled runs use the params' defaults**, so a job's configured selection (e.g. languages, sample) shows as its params' defaults; the UI shows them as the schedule's selection ("Runs with …"). A manual run that leaves a param out gets its default.

## Changes

- 2026-10-11: from the meta session building GOAL-0008: no `:` in job IDs (dotted `sync.<provider>.<kind>`), prefixed enum values (buf lint), `JobParam.default`, `int` param type, typed `status` filter, a `JobAlreadyRunning` error detail.
- 2026-10-11: as built in meta (`743e687`): a scheduled run that finds its job busy is recorded as `SKIPPED` (trigger schedule); `:run`/`:cancel` accept an empty body. mihon-source should match.
- 2026-10-11: as built in mihon-source (`898723f`): `JobParam.choices = 6` (allowed values; the UI shows checkboxes for a string_list with choices) and, on the 409, an ErrorInfo (reason `ALREADY_RUNNING`, metadata `current_run_id`) next to `JobAlreadyRunning`. meta to copy. Note: Armeria's transcoding passes `a:b` through to the handler (vanguard 404s); the ID rule still applies everywhere.
- 2026-10-11: from meta (GOAL-0006): `JOB_TRIGGER_SYSTEM = 4` for runs the service starts on its own while running (e.g. a rebuild after a backlog or a settings change). meta also adopted `JobParam.choices` and the ErrorInfo on 409. mihon-source to add SYSTEM.
- 2026-10-11: **server** implements the same job and run model in its own REST API (`/api/v1/jobs`, `/jobs/{id}/run`, `/job-runs/{id}/cancel`, lowercase enum values, matching the rest of `/api/v1`), since that API isn't proto transcoding. The colon-verb paths above apply to the gRPC-transcoded admin APIs of meta and mihon-source.
- 2026-10-12, *proposed, not built*: an optional display `label` on `JobParam` (additive; UIs fall back to the name turned into words, as the web app does since `e56a72b`). From `panelarr-web`; would apply to meta, mihon-source and the server alike.
- 2026-10-12: the server starts meta syncs through `RunJob("sync.<provider>.<kind>")` (server `97055ae`), falling back to the legacy `RunSync` on an older meta. *Proposed, not built:* an optional `RunJobRequest.on_behalf_of` (string), honoured only for admin-scope clients and recorded as `triggered_by` "<client> (<on_behalf_of>)", so meta's history names the Panelarr user who started a run.
- 2026-10-12: **source plugins** get the same model as an optional `PLUGIN_CAPABILITY_JOBS` in source.v1 (source-api `ab7a019`), with the entities in a shared `panelarr.jobs.v1` package (wire-identical to this contract and to mihon.v1). `RunJobRequest.on_behalf_of` is built for plugins (recorded as triggered_by); meta may adopt it later. Plugin job history from the SDK runner is in memory (100 runs a job).
- 2026-10-12: **convention, per-source jobs:** a job that declares a `source_ids` param of type string_list can be run for chosen sources; hosts may offer it from a source ("Check now") by passing that source's ID. No job ID is assumed (mihon-source's `source-health` follows this).
