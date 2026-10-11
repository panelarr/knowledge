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
  string id = 1;                 // stable, e.g. "store-refresh", "source-health", "sync:mangabaka:dump", "rebuild-entries"
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

message JobParam { string name = 1; string type = 2; /* bool|string|string_list */ string description = 3; bool required = 4; }

enum JobRunStatus { JOB_RUN_STATUS_UNSPECIFIED = 0; RUNNING = 1; SUCCEEDED = 2; FAILED = 3; CANCELLED = 4; SKIPPED = 5; }
enum JobTrigger   { JOB_TRIGGER_UNSPECIFIED = 0; SCHEDULE = 1; MANUAL = 2; STARTUP = 3; }

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
message RunJobResponse { JobRunSummary run = 1; }   // ALREADY_EXISTS (HTTP 409) with the current run id when running
```

## Rules

- **admin** scope only. Errors: unknown job → `NOT_FOUND`, already running → `ALREADY_EXISTS` (409, details carry `current_run_id`), not cancellable → `FAILED_PRECONDITION`.
- **Retention:** last 100 runs per job by default (configurable); counts and notes are bounded.
- **Restart:** runs left `RUNNING` at startup become `FAILED` with message "interrupted".
- **Metrics** (ADR-0027): `<svc>_job_runs_total{job,status,trigger}`, `<svc>_job_duration_seconds{job}`, `<svc>_job_running{job}`.
- **meta:** a provider sync is a job per provider and ingestion kind (`sync:<provider>:<kind>`, param `force`); the existing sync-run API keeps working (map it onto job runs).
- **Parameterised jobs** declare `params`; the UI renders a small form before "Run now".
