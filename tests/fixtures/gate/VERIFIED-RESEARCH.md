# Verified research — test reporter JSON shapes used by check-gate.py

Checked via context7 (`/microsoft/playwright`, `/vitest-dev/vitest`) and the reporter source files on `main`.

| Claim | Source | Date |
|---|---|---|
| Playwright JSON report top level is `{ config, suites, errors, stats }`; `config` carries `projects[]`. | https://github.com/microsoft/playwright/blob/main/packages/playwright/types/testReporter.d.ts (`JSONReport`) | 2026-10-02 |
| `JSONReportSuite` = `{ title, file, line, column, specs: JSONReportSpec[], suites?: JSONReportSuite[] }` — suites nest, specs can appear at any level. | same file (`JSONReportSuite`) | 2026-10-02 |
| `JSONReportSpec` = `{ tags, title, ok, tests: JSONReportTest[], id, file, line, column }` — one `tests[]` entry per project. | same file (`JSONReportSpec`) | 2026-10-02 |
| `JSONReportTest` = `{ timeout, annotations, expectedStatus, projectName, projectId, results[], status: 'skipped' \| 'expected' \| 'unexpected' \| 'flaky' }`. | same file (`JSONReportTest`) | 2026-10-02 |
| `JSONReportTestResult` has `status: TestStatus`, `retry`, `errors[]`, `annotations[]`, etc.; results are in retry order, so the last entry is the final attempt. | same file (`JSONReportTestResult`) | 2026-10-02 |
| `TestStatus = 'passed' \| 'failed' \| 'timedOut' \| 'skipped' \| 'interrupted'`; annotations are `{ type, description?, location? }`. | https://github.com/microsoft/playwright/blob/main/packages/playwright/types/test.d.ts | 2026-10-02 |
| A clean pass is `status: 'expected'`, `expectedStatus: 'passed'`, one result with `retry: 0`, `status: 'passed'`. `flaky` = failed then passed on retry. | testReporter.d.ts (context7 snippet "JSON report test fields identifying a passed test") | 2026-10-02 |
| `test.fixme()` marks a test that Playwright will not run; it is reported with a `fixme` annotation and skipped status (`expectedStatus`/`status` `skipped`). | https://github.com/microsoft/playwright/blob/main/docs/src/test-annotations-js.md | 2026-10-02 |
| Playwright JSON is written to stdout with `--reporter=json`, or to a file via `PLAYWRIGHT_JSON_OUTPUT_FILE` / `outputFile`. | https://github.com/microsoft/playwright/blob/main/docs/src/test-reporters-js.md | 2026-10-02 |
| Vitest JSON reporter output is Jest `--json` compatible: `{ numTotalTests, numPassedTests, …, success, testResults[], snapshot, coverageMap? }`. | https://github.com/vitest-dev/vitest/blob/main/docs/guide/reporters.md ; https://github.com/vitest-dev/vitest/blob/main/packages/vitest/src/node/reporters/json.ts (`JsonTestResults`) | 2026-10-02 |
| Each `testResults[]` entry = `{ assertionResults[], startTime, endTime, status: 'failed' \| 'passed', message, name }` (`name` = test file path). | json.ts (`JsonTestResult`) and docs example | 2026-10-02 |
| Each `assertionResults[]` entry = `{ ancestorTitles, fullName, status, title, duration, failureMessages, location, meta }`; `title` is the test's own name, `fullName` joins ancestors + title. | json.ts (`JsonAssertionResult`) | 2026-10-02 |
| Assertion `status` is `'passed' \| 'failed' \| 'skipped' \| 'pending' \| 'todo' \| 'disabled'` (task state map: pass→passed, fail→failed, skip→skipped, todo→todo, run/only/queued→pending). | json.ts (`Status`, `StatusMap`) | 2026-10-02 |
| Vitest: `npx vitest --reporter=json --outputFile=./test-output.json`; default file `.vitest/json/output.json`. | https://github.com/vitest-dev/vitest/blob/main/docs/guide/reporters.md | 2026-10-02 |

## How check-gate.py applies this

- Format detection: object with `config` + `suites` list → Playwright; object with `testResults` list → Vitest; anything else fails.
- Playwright pass = test `status` in `expected|flaky`, `expectedStatus == passed`, and last result `status == passed`. If the status or expectedStatus is `skipped`, or it has a `fixme`/`skip` annotation, it counts as fixme/skipped. Anything else counts as failed, including `test.fail()` tests, whose expectedStatus is `failed`.
- Vitest pass = assertion `status == passed`. `failed` counts as failed. `skipped|pending|todo|disabled` are not passes.
- Matching uses the test's own `title` (Playwright spec title / Vitest assertion title), not suite titles.
