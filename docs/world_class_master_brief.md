# ONE-LINER

**CaseProof Analyst** — автономный AI-аналитик для SIFT, который не просто ищет подозрительные артефакты, а строит доказательную книгу расследования: каждое утверждение связано с источником, каждое сомнение проверяется, каждая ошибка видимо исправляется до финального отчёта.

# ORIGINAL IDEA / RAW INPUT

Пользователь просит изучить текущий проект `Find Evil!`, условия конкурса и создать идею полноценного проекта мирового класса, которую не стыдно показать и с которой можно претендовать на победу.

Исходный контекст проекта:

- текущий проект уже называется `Evidence-Locked Self-Correcting Disk Triage MCP`;
- выбранная основа — read-only Custom MCP Server для Windows disk triage;
- публичная сила проекта — доказательная безопасность, self-correction, claim verification и execution logs;
- текущий статус — частичная готовность: есть код, контракт, синтетический accuracy report и локальные проверки, но нет реального SIFT validation, demo video, public repo proof и финального Devpost story;
- конкурс требует working software application, real evidence demo, self-correction, accuracy validation, analytical narrative, architecture diagram, dataset docs, accuracy report and agent execution logs.

# IDEA SUMMARY

CaseProof Analyst превращает текущий проект из “безопасного MCP wrapper для SIFT” в полноценный продуктовый опыт для incident responders: автономный аналитик проводит первичное расследование, строит доказательную цепочку, проверяет собственные выводы и выпускает отчёт, которому можно доверять.

Главная идея: выиграть не шириной обёрток вокруг инструментов, а качеством доказательного мышления — судья должен видеть, как агент думает, ошибается, ловит ошибку, перепроверяет, понижает уверенность или исправляет вывод.

# FINAL GOAL

Финальный продукт должен выглядеть как профессиональный defensive AI co-analyst для SIFT, а не как демонстрация отдельных команд.

Желаемый результат:

- автономный запуск на реальном case data внутри SIFT-compatible environment;
- расследовательский отчёт с ясной историей атаки, а не просто лог команд;
- evidence book, где каждое finding можно раскрыть до конкретного артефакта, файла, offset, log entry или другого проверяемого источника;
- correction ledger, где видно, какие утверждения агент отверг, перепроверил или понизил до inference;
- accuracy package, честно показывающий confirmed findings, inferred findings, unsupported dropped claims, missed artifacts and known limits;
- demo story, где self-correction является центральной сценой, а не скрытой внутренней проверкой;
- public repository package, который другой practitioner может понять, запустить и расширить.

# FULL PRODUCT VISION

CaseProof Analyst — это не общий “AI for cybersecurity”. Это узкий, доказательно-закрытый автономный аналитик для первичного incident response triage.

Основные модули продукта:

- **Case Intake**: пользователь указывает case, evidence source и рабочую область; система фиксирует, что оригинальные evidence остаются входом, а не местом записи.
- **Autonomous Investigation**: агент сам выбирает следующую проверку внутри разрешённой forensic-поверхности, реагирует на ошибки и не продолжает финальный отчёт без evidence support.
- **Evidence Book**: отдельная человекочитаемая доказательная книга, где findings связаны с source references и проверочным статусом.
- **Correction Ledger**: видимый журнал ошибочных или спорных утверждений: что было заявлено, почему отклонено, какая проверка была запущена, чем закончилась.
- **Analyst Narrative Report**: итоговая история расследования на языке senior analyst: что произошло, какие следы найдены, что подтверждено, что только предполагается, что требует человека.
- **Accuracy & Trust Pack**: judge-facing пакет с честной оценкой точности, ограничениями, missed artifacts, hallucination controls and spoliation test.
- **Replayable Run Record**: структурированная история запуска, по которой можно восстановить путь от final finding до конкретной tool execution.

Режимы работы:

- **Contest Demo Mode**: короткий, воспроизводимый сценарий для видео и judging review.
- **Practitioner Triage Mode**: обычный запуск по case data с отчётом и доказательной книгой.
- **Challenge Mode**: агент намеренно проверяет собственные strongest findings на unsupported assumptions, conflicts and missing evidence.
- **Readiness Mode**: продукт показывает, готова ли среда к реальному запуску, не раскрывая секреты и не притворяясь готовым, если evidence/tools отсутствуют.

Типы пользователей:

- incident responder, которому нужен быстрый первый разбор;
- DFIR practitioner, который должен доверять evidence trail;
- junior analyst, который учится видеть reasoning опытного аналитика;
- hackathon judge, который оценивает autonomy, accuracy, constraints and auditability;
- open-source contributor, который хочет расширить проект без разрушения trust model.

# TARGET USER

Primary target user:

- DFIR / incident response practitioner, который работает с case evidence и должен быстро понять, есть ли признаки компрометации.

Secondary users:

- senior analyst, который хочет быстро проверить первичные выводы и audit trail;
- junior analyst, которому важно видеть ход расследовательского мышления;
- SIFT/Protocol SIFT community contributor, который хочет безопасно расширять autonomous workflows;
- hackathon judge, которому нужен ясный proof that the agent self-corrects and does not hallucinate unsupported findings;
- security team lead, которому нужен reproducible and defensible first triage package.

Ключевой пользовательский контекст:

- время ограничено;
- ошибочный confidence опасен;
- сырые логи и длинные terminal transcripts плохо помогают быстро принять решение;
- доверие появляется только там, где можно проследить вывод до конкретного evidence;
- для adoption важнее честная неопределённость, чем впечатляющие, но неподтверждённые claims.

# CORE PROBLEM

Главная проблема: autonomous AI может ускорить incident response, но без доказательной дисциплины он создаёт новый риск — быстрые, уверенные, но неподтверждённые выводы.

Проблема в деталях:

- текущий разрыв между скоростью атакующих и ручной работой аналитика слишком велик;
- существующий AI-assisted DFIR может hallucinate, особенно когда получает большие, шумные outputs;
- prompt-only restrictions недостаточно убедительны для forensic evidence integrity;
- обычный final report скрывает, какие выводы были проверены, а какие являются догадками;
- judges and practitioners need trust, not just automation;
- без replayable logs невозможно понять, почему агент сделал вывод и где он мог ошибиться;
- без честного accuracy report проект выглядит как demo magic, а не как serious IR capability.

# POSITIONING

Возможные позиционирования:

1. **Evidence-locked AI triage analyst**  
   ASSUMPTION: жизнеспособно, потому что конкурс явно ценит architectural guardrails and evidence integrity.

2. **Self-correcting DFIR co-analyst**  
   ASSUMPTION: жизнеспособно, потому что tiebreaker — autonomous execution quality and real-time self-correction.

3. **Claim-verification layer for Protocol SIFT**  
   ASSUMPTION: жизнеспособно, потому что hallucination control is a central pain, but alone may feel too narrow.

4. **Forensic proof book generator**  
   ASSUMPTION: жизнеспособно, потому что audit trail quality is judging-critical and practitioners need defensible output.

5. **Read-only SIFT safety boundary**  
   ASSUMPTION: жизнеспособно, потому что constraint implementation is a scoring criterion, but it sounds more architectural than product-led.

6. **Junior analyst training companion**  
   ASSUMPTION: жизнеспособно for education, but less directly aimed at winning the strongest technical judging categories.

7. **Accuracy-first incident response agent**  
   ASSUMPTION: жизнеспособно, but could be mistaken for a benchmark rather than a working triage product.

8. **Replayable autonomous investigation system**  
   ASSUMPTION: жизнеспособно, because judges need traceability and the community needs reproducible AI runs.

9. **Machine-speed first responder with human-grade evidence discipline**  
   ASSUMPTION: strongest emotional and product promise, because it ties the contest mission to practitioner trust.

10. **Courtroom-style evidence chain for AI findings**  
    ASSUMPTION: memorable and differentiated, but “courtroom” could overpromise legal defensibility if not framed carefully.

RECOMMENDED positioning:

**Machine-speed first responder with human-grade evidence discipline.**

Reasoning:

- it directly matches the contest’s speed-vs-trust narrative;
- it does not reduce the project to wrappers or tooling;
- it gives judges a simple reason to care: fast enough for AI-speed threats, disciplined enough for real DFIR;
- it preserves the current technical advantage without turning the brief into architecture;
- it creates a strong demo arc: fast triage, detected mistake, correction, evidence-backed report.

Supporting promise:

> CaseProof Analyst helps responders move at machine speed without accepting machine hallucinations.

# PROJECT SHAPE

Допустимые shape-варианты:

1. **Terminal-first autonomous analyst with generated evidence dossier**  
   Fits the contest’s live terminal demo requirement and keeps the product focused on SIFT workflows. Strongest fit for first release.

2. **Full visual investigation cockpit**  
   More impressive as a product surface, but risks dragging the first release into UI polish instead of real evidence validation.

3. **Benchmark and accuracy framework first**  
   Very useful for the community, but weaker as a complete autonomous response agent unless paired with real triage.

RECOMMENDED shape:

**Hybrid terminal-first product: autonomous run + generated evidence dossier + judge/practitioner documentation.**

Product form:

- primary surface is a local investigation run;
- output surfaces are report, evidence book, correction ledger, accuracy report and execution logs;
- public repository is part of the product because the contest judges and open-source community must deploy and build on it;
- no account system is needed for first release;
- no public web dashboard is required for first release;
- admin surface is replaced by practitioner configuration and readiness checks;
- future visual review panel is possible, but not required to win the first release.

# FIRST RELEASE SCOPE (не MVP)

PROPOSED first release scope:

Must-have:

- real evidence run inside a SIFT-compatible environment;
- one deep Windows disk triage lane with enough artifact depth to produce a meaningful investigation narrative;
- visible autonomous self-correction sequence;
- every confirmed finding passes through claim verification;
- every finding links to evidence references;
- unsupported claims are shown as rejected or dropped, not silently ignored;
- original evidence remains read-only by product boundary;
- generated case report reads like a senior analyst narrative;
- generated evidence book supports judge traceability;
- generated correction ledger supports self-correction proof;
- generated accuracy report clearly separates real results from synthetic fixture results;
- structured execution logs are complete enough to replay the investigation path;
- repository documentation supports local judge execution.

Nice-to-have:

- a compact “judge summary” at the top of the final report;
- a “why this is trustworthy” section explaining evidence boundaries in plain English;
- a small curated demo case script that reliably shows correction without faking evidence;
- practitioner-friendly glossary for non-experts reviewing the repository;
- comparison against baseline Protocol SIFT behavior if a fair baseline can be created.

Consciously out of first release:

- broad wrapping of all SIFT tools;
- memory-forensics lane unless it becomes necessary for the chosen real case;
- network-capture lane;
- remote/live environment triage;
- multi-case enterprise workflow;
- account system, billing, team management or public hosted service;
- polished visual dashboard unless the core evidence proof is already complete;
- any claim of production-grade accuracy without real validation.

# FUTURE SCOPE

Future product directions:

- disk + memory contradiction checking for stronger multi-source confidence;
- broader case data support once the first lane is validated;
- visual evidence graph for reviewers who do not want to read structured logs;
- analyst review annotations on findings and evidence references;
- case comparison across repeated runs;
- curated training mode that explains reasoning for junior analysts;
- community plugin model for additional evidence families;
- richer accuracy benchmark library with known-answer datasets;
- practitioner-ready report templates for different response contexts;
- long-term improvement loop based on reviewed outcomes, without hiding uncertainty.

What should remain stable:

- no confirmed finding without evidence;
- no original evidence mutation;
- uncertainty stays visible;
- execution trace remains replayable;
- first release depth should not be sacrificed for shallow breadth.

# USER FLOWS

Primary practitioner flow:

1. User starts a case with an evidence source and a case workspace.
2. Product checks readiness and clearly reports blockers before pretending to run.
3. Agent opens evidence in read-only mode and begins initial triage.
4. Agent gathers filesystem, timeline, persistence and event context for the chosen lane.
5. Agent drafts candidate findings.
6. Agent verifies each candidate finding against collected evidence.
7. Agent detects unsupported or conflicting claims and re-checks targeted evidence.
8. Agent writes final report, evidence book, correction ledger, accuracy summary and execution log.
9. User reviews the report from top-level narrative down to source evidence references.
10. User can rerun or refine the case with a narrower question if needed.

Judge demo flow:

1. Judge sees a live terminal run against real case data.
2. Product shows environment readiness and case start.
3. Agent makes an initial incomplete or wrong assumption.
4. Verification rejects or downgrades the unsupported claim.
5. Agent runs a targeted follow-up check.
6. Final report shows corrected output.
7. Judge opens the evidence book and sees the source chain behind the finding.
8. Judge opens execution logs and confirms the tool sequence.

Return flow:

- user returns to the case workspace;
- user reads final summary first;
- user drills into evidence references only for contested findings;
- user checks correction ledger to see what the AI refused to claim;
- user uses accuracy report to understand known limits before relying on output.

# ADMIN / POWER USER FLOWS

Power user flow:

- choose or prepare a case dataset;
- define the case workspace;
- run readiness checks;
- inspect product limitations before execution;
- review unsupported claims and parser warnings;
- compare final findings with known ground truth where available;
- update dataset documentation with what was tested and what was found;
- package run artifacts for judges or peer review.

Project maintainer flow:

- preserve public tool names unless a documented decision changes them;
- add new artifact families only when they strengthen the evidence story;
- update accuracy documentation when a real case run replaces a synthetic fixture;
- prevent public README and Devpost copy from overstating readiness;
- keep demo assets aligned with what the software actually does.

No separate admin panel is required for first release.

# CORE ENTITIES

Core product entities:

- **Case**: the investigation unit with a name, source evidence and generated outputs.
- **Evidence Source**: original forensic input that must remain read-only.
- **Case Workspace**: location where outputs, reports and logs are created.
- **Tool Execution**: one bounded forensic action requested by the agent.
- **Evidence Record**: normalized observation extracted from source evidence.
- **Candidate Claim**: a possible investigative conclusion before verification.
- **Finding**: a claim that has been verified, downgraded or rejected.
- **Evidence Reference**: link between a finding and the source artifact that supports it.
- **Correction Event**: moment where the agent changes direction because a claim failed, evidence conflicted or a parser failed.
- **Final Report**: analyst-readable narrative of the case.
- **Evidence Book**: traceable supporting dossier.
- **Accuracy Report**: self-assessment of correctness and limits.
- **Execution Log**: structured replay record of the run.

# ROLES & PERMISSIONS

First release roles:

- **Operator**: runs the case, provides evidence path and reviews outputs.
- **Reviewer**: reads reports, evidence book and logs without changing evidence.
- **Maintainer**: updates project docs, contracts and future evidence families.
- **Judge**: tests the public submission and evaluates traceability, safety and autonomy.

Access principles:

- original evidence is input-only;
- generated case outputs can be reviewed and packaged;
- findings can be interpreted, but confirmed status should not be manually faked;
- unsupported claims should remain visible in correction history where useful;
- public materials must not include secrets or private case data;
- future collaborative roles should preserve the same evidence integrity model.

# WHAT WE WANT

We want a product that:

- feels like a senior analyst working through evidence, not a chatbot summarizing logs;
- produces a clear investigative narrative;
- visibly catches its own unsupported claims;
- treats uncertainty as a feature, not a weakness;
- gives every confirmed finding a traceable evidence basis;
- makes architectural safety understandable to non-engineer judges;
- is honest about what has been validated and what remains unvalidated;
- can be run by another practitioner from the repository instructions;
- demonstrates one deep lane exceptionally well;
- leaves a credible foundation for broader DFIR expansion.

Key product experience:

- “I can see what the agent did.”
- “I can see why it changed its mind.”
- “I can see what evidence supports the final claim.”
- “I can see what it refused to claim.”
- “I can run this myself and build on it.”

# PRODUCT MODULES

Product modules:

- **Readiness Check**: verifies that required local conditions are present before a real run.
- **Case Intake**: defines case identity, evidence source and workspace.
- **Investigation Planner**: chooses the next bounded investigation step based on current evidence and gaps.
- **Artifact Collection**: gathers the selected forensic evidence families for the first release lane.
- **Claim Drafting**: turns observations into candidate investigative claims.
- **Claim Verification**: checks candidate claims against available evidence records.
- **Self-Correction Loop**: handles unsupported claims, parser failures and contradictions.
- **Evidence Book Builder**: turns evidence records into reviewable source chains.
- **Narrative Report Builder**: produces the final analyst-readable report.
- **Accuracy Pack Builder**: records correctness, hallucinations, missed artifacts and limits.
- **Execution Replay Log**: preserves the sequence of actions and corrections.
- **Submission Pack**: keeps judge-facing artifacts aligned with contest requirements.

# SCREENS / SURFACES

First release surfaces:

- **Run surface**: local command execution and status output.
- **Readiness surface**: pass/fail readiness output for environment, evidence and provider configuration.
- **Final report surface**: human-readable investigation narrative.
- **Evidence book surface**: support chain for findings.
- **Correction ledger surface**: rejected, downgraded and corrected claims.
- **Accuracy report surface**: result quality, limits and validation status.
- **Execution log surface**: structured replayable run history.
- **Dataset documentation surface**: what evidence was tested and what was found.
- **Architecture explanation surface**: trust boundaries and data movement.
- **Repository README surface**: try-it-out instructions and honest current status.

Future surfaces:

- visual case review panel;
- side-by-side finding and evidence view;
- run comparison view;
- analyst annotation surface.

# SCREEN STATES

Key states for first release surfaces:

- **Ready**: environment and evidence are sufficient for a real run.
- **Blocked**: missing local prerequisites, missing evidence or unavailable required tools.
- **Running**: investigation is active and current step is visible.
- **Partial**: some evidence was parsed, but a family failed or produced incomplete output.
- **Correcting**: a claim failed verification or evidence conflict requires a targeted check.
- **Completed**: final report and evidence artifacts are produced.
- **No confirmed findings**: product reports that no supported malicious finding was confirmed.
- **Unsupported claim rejected**: product explicitly shows that a candidate claim was not allowed into confirmed output.
- **Needs human review**: evidence is suggestive or incomplete and should not be overclaimed.
- **Synthetic-only warning**: current run is not a real dataset validation.
- **Permission denied / unsafe action blocked**: requested action violates read-only evidence boundary.

# WHAT WE DO NOT WANT

We do not want:

- a generic AI security chatbot;
- a demo that only prints terminal commands;
- broad SIFT coverage with shallow, unverified output;
- confident claims that lack source evidence;
- hidden correction logic that judges cannot see;
- prompt-only safety framed as architectural evidence protection;
- mutation of original evidence;
- public claims of real accuracy based on synthetic data;
- UI polish that distracts from missing real validation;
- unsupported vendor or tool promises not required by the contest;
- a final report that reads like raw logs;
- a “world-class” narrative that overstates current readiness.

# INTEGRATIONS

Required or relevant integrations at product level:

- SIFT-compatible forensic workstation environment;
- Protocol SIFT-compatible agent workflow;
- local forensic evidence sources such as disk images;
- external AI service for autonomous reasoning;
- local case workspace for generated outputs;
- public repository hosting for judging and open-source review;
- public video hosting for required demo;
- contest submission page for final materials;
- optional external communication/community channels for support and feedback.

Integration principles:

- integrations should support reproducibility;
- integrations should not introduce evidence mutation risk;
- secrets must not appear in logs, reports or public docs;
- external service dependency should be documented honestly;
- if an integration is optional, the product should say so.

# CONSTRAINTS

Contest constraints:

- project must extend Protocol SIFT autonomous incident response capability;
- project must run on or integrate with SIFT Workstation environment;
- final submission requires all mandatory components;
- demo video must show live execution against real evidence and at least one self-correction sequence;
- repository must be public and open source with an accepted license;
- README must include setup instructions;
- accuracy report must honestly document false positives, missed artifacts, hallucinated claims and evidence integrity;
- execution logs must allow traceability from finding to tool execution;
- English submission materials are required or must have English translation.

Project constraints:

- original evidence path must remain read-only;
- eight public tool names should be preserved unless a decision is recorded;
- current synthetic accuracy report must not be treated as real SIFT validation;
- real SIFT validation remains a blocker;
- first release should avoid scope expansion that weakens depth;
- product claims must match actual verified behavior;
- API keys and secrets must remain local and redacted.

# NON-FUNCTIONAL REQUIREMENTS

Quality requirements:

- **Trustworthiness**: confirmed findings require evidence support.
- **Safety**: original evidence must not be modified.
- **Reproducibility**: another practitioner should be able to follow the same setup and inspect run artifacts.
- **Transparency**: uncertainty, failures and corrections must be visible.
- **Auditability**: findings must trace back to specific execution records.
- **Clarity**: reports should be understandable without reading source code.
- **Resilience**: parser failures should produce honest partial results, not silent success.
- **Bounded autonomy**: the agent should not loop indefinitely or keep trying unbounded actions.
- **Privacy and secret hygiene**: secret values must never be printed in public-facing outputs.
- **Maintainability**: future evidence families should extend the product without weakening the core trust model.

# IMPORTANT DETAILS

Source basis reviewed:

- local `УСЛОВИЯ.txt`;
- current live Devpost page for FIND EVIL!;
- `README.md`;
- `docs/STATE.md`;
- `docs/EXEC_PLAN.md`;
- `docs/DECISIONS.md`;
- `docs/hackathon_strategy.md`;
- `docs/research_sift_mcp.md`;
- `docs/mcp_architecture.md`;
- `docs/architecture.md`;
- `docs/accuracy_report.md`;
- `docs/submission_readiness_audit.md`.

Important contest facts:

- one explicit mission: make Protocol SIFT a fully autonomous incident response agent;
- quality of autonomous execution matters more than data type;
- supported paths include custom MCP server and self-correcting agent;
- custom MCP server is described as the soundest architecture but most work;
- required outputs include code repo, demo video, architecture diagram, written description, dataset docs, accuracy report, try-it-out instructions and execution logs;
- judging includes autonomous execution quality, IR accuracy, breadth/depth, constraint implementation, audit trail quality and usability/documentation;
- tie-breaking starts with autonomous execution quality.

Important project facts:

- current code has contract-first public tool surface;
- current artifact set is strong but not final-submission complete;
- Groq/OpenRouter keys may be configured locally, but they are not the product idea;
- current runtime readiness has improved, but real SIFT binaries and real evidence validation remain central gaps;
- public narrative must stay honest about synthetic vs real validation.

# DATA MODEL HINTS

Conceptual relationships:

- a case has one or more evidence sources;
- evidence sources produce evidence records through bounded investigation actions;
- evidence records support, weaken or fail to support candidate claims;
- candidate claims become confirmed findings, inferred findings, unsupported claims or human-review items;
- correction events connect failed claims to follow-up investigation actions;
- final report summarizes findings and links to evidence book entries;
- evidence book entries point back to source references and execution records;
- accuracy report summarizes the quality and limitations of a run;
- execution log preserves the order and rationale of the run;
- dataset documentation explains the origin and expected scope of tested evidence.

Source of truth principles:

- original evidence is the source of forensic truth;
- evidence records are the product’s normalized observations;
- verified findings are the reportable conclusions;
- correction ledger is the source of truth for self-correction proof;
- execution log is the source of truth for replaying the agent’s behavior.

# DATA LIFECYCLE

Lifecycle:

- evidence is registered as an input source;
- case workspace is created for outputs;
- bounded investigation actions extract observations;
- observations become evidence records;
- candidate claims are created from observations;
- claims are checked against evidence records;
- unsupported claims are rejected, downgraded or marked for human review;
- correction events are recorded when the agent changes direction;
- final outputs are generated from verified findings and recorded uncertainty;
- public submission artifacts are produced from real run outputs and clearly labelled;
- obsolete or incorrect generated outputs should be replaced only when a newer run is clearly identified.

Deletion and recovery principles:

- original evidence is never deleted by the product;
- generated case outputs should be removable from the workspace by the user outside the evidence source;
- important run artifacts should remain recoverable for review until the user intentionally removes them;
- conflicts between outputs should be resolved by run identity and clear labeling, not silent overwrite;
- exported artifacts should retain enough context to remain understandable outside the workspace.

# RISKS

Key risks:

- first release tries to cover too many data types and loses depth;
- real evidence validation is delayed and the project remains synthetic-only;
- self-correction becomes a staged-looking demo instead of genuine behavior;
- claim verification is too shallow and misses semantic support or contradiction;
- reports become too technical for judges to understand quickly;
- product overclaims “production-ready” despite contest-stage limitations;
- evidence references are too vague to satisfy audit trail expectations;
- dependency on local environment makes judge setup brittle;
- generated logs expose secrets or private paths;
- future feature additions weaken the read-only boundary;
- demo video fails to show the product’s unique correction moment.

# PRODUCT DEATH RISKS

Reasons users or judges would not trust or return:

- final findings look impressive but cannot be traced to evidence;
- the agent never admits uncertainty;
- the demo hides errors instead of showing correction;
- setup fails and README does not clearly explain blockers;
- accuracy report feels like marketing rather than measurement;
- synthetic results are presented as real validation;
- product tries to be a full DFIR platform before proving one excellent lane;
- output is raw log dump rather than investigation narrative;
- evidence safety depends on “the AI was told not to” instead of product boundary;
- practitioners cannot extend the project without understanding the trust model.

# PRIORITIES

Must:

- real evidence validation;
- visible self-correction;
- evidence-linked confirmed findings;
- read-only evidence boundary;
- final report, evidence book, correction ledger, accuracy report and execution logs;
- honest public packaging.

Should:

- strong demo storyline;
- plain-English trust explanation;
- dataset documentation with real observed results;
- clear setup and readiness checks;
- evidence references usable by non-authors.

Could:

- visual evidence graph;
- baseline comparison;
- junior analyst explanation mode;
- broader artifact families;
- contributor extension guide.

Won't for first release:

- full SIFT tool suite;
- live environment integrations;
- memory/network lane unless necessary;
- hosted product account system;
- polished dashboard before real validation;
- claims of production-grade reliability.

# DECISIONS NEEDED

Critical decisions:

- choose the real evidence dataset for final demo and accuracy report;
- choose the exact first-release case story: persistence, suspicious execution, timeline anomaly or another evidence-backed narrative;
- decide whether first release stays disk-only or includes one carefully limited second source only if real case demands it;
- decide final project name for public submission: `CaseProof Analyst` is RECOMMENDED;
- decide whether visual evidence graph is deferred or included only as generated documentation;
- decide final wording for what is real validation vs synthetic fixture;
- decide final demo path that reliably shows one genuine correction sequence.

Can be deferred:

- broader data types;
- visual review panel;
- community extension model;
- training mode;
- long-term benchmark library.

Critical blocker:

- no final winning submission should be made without real SIFT-compatible evidence run and updated accuracy report.

# ACCEPTANCE / NO-GO

Ready for next stage when:

- the product idea is clearly framed as evidence-disciplined autonomous triage;
- first release scope is narrow and deep;
- all contest-required artifacts are mapped to product outputs;
- real validation path is explicit;
- public claims do not overstate current readiness;
- self-correction is central to the demo story.

No-go for final contest submission if:

- demo uses only synthetic fixture;
- no real evidence run exists;
- final report includes unsupported confirmed claims;
- accuracy report does not distinguish real and synthetic results;
- original evidence can be modified through the product surface;
- execution logs cannot trace findings back to actions;
- README cannot guide a judge through setup;
- public submission lacks any mandatory component.

# ASSUMPTIONS

ASSUMPTION: the strongest path to winning is depth and trust, not maximum feature count.

ASSUMPTION: judges will reward visible self-correction more than hidden validation.

ASSUMPTION: a deep Windows disk triage lane is enough if the evidence story is real, traceable and well-documented.

ASSUMPTION: a terminal-first product is acceptable because the contest explicitly asks for live terminal execution.

ASSUMPTION: a visual dashboard is not necessary for first release if generated reports and evidence book are excellent.

ASSUMPTION: the final public story should emphasize practitioner trust and community usefulness, not only hackathon compliance.

ASSUMPTION: current local project structure is a valid base and should be sharpened rather than replaced.

# OPEN QUESTIONS

1. Which real evidence dataset will be used for final validation and video?
2. What is the strongest confirmed attack story available in that dataset?
3. Can the demo show a genuine correction without artificially forcing an error?
4. Will the public project name be `CaseProof Analyst` or a variant?
5. Is the first release strictly disk-only, or does the chosen real case require one additional source?

# SUCCESS CRITERIA

The idea is successful if:

- a judge can explain the project in one sentence after seeing it;
- the demo clearly shows autonomous investigation and self-correction;
- every confirmed finding is traceable to evidence;
- unsupported claims are caught and visibly handled;
- the report reads like an analyst narrative, not a transcript;
- the accuracy report is honest and specific;
- the execution logs are useful, not decorative;
- the architecture boundary is understandable at a glance;
- another practitioner can run or inspect the project from public materials;
- the product feels like a credible open-source foundation after the contest.

# PRODUCT READINESS

Ready for design when:

- name, positioning and first-release evidence story are chosen;
- output surfaces are fixed: report, evidence book, correction ledger, accuracy report, logs;
- demo narrative is selected.

Ready for architecture when:

- product boundaries are clear;
- first-release data lane is frozen;
- claim/evidence/correction concepts are stable;
- no new broad data types are being added casually.

Ready for development when:

- real dataset is accessible;
- environment readiness blockers are understood;
- current contract boundaries remain valid;
- output expectations are written clearly.

Ready for testing when:

- real run can complete;
- expected findings or ground-truth notes exist;
- unsupported claim controls are included;
- generated artifacts can be reviewed for traceability.

Ready for launch/submission when:

- all mandatory contest artifacts are complete;
- demo video matches actual behavior;
- repository is public and licensed;
- accuracy report reflects real validation;
- no public copy overstates readiness.

# HANDOFF CHECKLIST

Completeness check:

- goal and value are clear: yes;
- target users are clear: yes;
- modules are clear: yes;
- entities and relationships are clear: yes;
- output surfaces are clear: yes;
- integrations are clear at product level: yes;
- risks are explicit: yes;
- constraints are explicit: yes;
- next decisions are explicit: yes;
- brief can be handed to design and architecture without re-explaining the idea: yes.

Main handoff warning:

- do not let the next stage turn this into broad tool wrapping; the product wins by proving trustworthy autonomous reasoning on a real evidence lane.

# DECISION LANGUAGE

Use these labels:

- `RECOMMENDED` for the chosen direction that still needs user confirmation;
- `PROPOSED` for first-release scope;
- `ASSUMPTION` for product bets that are reasonable but not externally proven;
- `NEEDS CONFIRMATION` for unresolved decisions;
- `DRAFT` for public copy until final evidence validation is complete.

Avoid these labels until truly verified:

- `approved`;
- `confirmed`;
- `settled`;
- `production-ready`;
- `real accuracy proven`;
- `complete`.

# LAUNCH / OPS READINESS

Contest launch readiness:

- public repository must be available and licensed;
- README must include honest setup and try-it-out instructions;
- demo video must show live execution, real evidence and visible correction;
- written project description must explain product value, design choices, challenges, learnings and next steps;
- architecture diagram must show trust boundaries;
- dataset documentation must explain source, scope and results;
- accuracy report must separate confirmed, inferred, unsupported and missed areas;
- execution logs must be included and reviewable;
- synthetic artifacts must be labelled as synthetic if still present;
- final submission should not rely on hidden local state.

Operational principles after contest:

- keep evidence safety as the non-negotiable product promise;
- document every new evidence family with its trust and limitation notes;
- treat failure modes as useful learning, not embarrassment;
- preserve reproducibility over flashy claims;
- maintain contributor clarity so the project can live beyond the hackathon.

# PHASES

Phase 1 — Product and evidence story freeze:

- choose final name and positioning;
- choose real dataset and case narrative;
- freeze first-release scope;
- define required output artifacts.

Phase 2 — Real validation preparation:

- confirm local environment readiness;
- confirm evidence accessibility;
- define expected findings or review baseline;
- prepare honest validation checklist.

Phase 3 — First release completion:

- produce real run artifacts;
- update final report, evidence book, correction ledger and logs;
- replace or clearly separate synthetic accuracy material;
- verify the self-correction sequence.

Phase 4 — Submission package:

- finalize public README;
- finalize architecture diagram;
- write Devpost-style project story;
- record demo video;
- verify all links and required files.

Phase 5 — Post-submission continuation:

- add broader evidence families only after the first lane is trusted;
- improve review surfaces;
- invite community validation;
- evolve benchmark coverage.

# LONG-TERM ROADMAP

v1:

- CaseProof Analyst for one deep Windows disk triage lane;
- evidence book;
- correction ledger;
- real accuracy report;
- judge-ready demo and documentation.

v1.1:

- stronger report readability;
- clearer contributor guidance;
- improved finding review experience;
- richer dataset documentation.

v2:

- carefully selected second evidence source if it improves contradiction detection;
- visual evidence graph;
- analyst annotation workflow;
- expanded accuracy benchmark examples.

Future ideas:

- training mode for junior analysts;
- community evidence-family extensions;
- run comparison across cases;
- organization-friendly review packaging;
- stronger long-term trust metrics.

What can be delayed without losing the core:

- full visual cockpit;
- hosted service model;
- broad multi-source support;
- complete SIFT tool coverage;
- enterprise user management.
