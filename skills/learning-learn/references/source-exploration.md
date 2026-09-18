# Source exploration

Use this branch only when answering the learner's question requires broad source tracing that would otherwise fill the teaching context with search residue.

Typical triggers include:

- tracing one call or data flow across several files;
- locating the real producer/consumer of a topic, service, callback, or shared value across a repository;
- reconciling several implementation sites before a source-specific mechanism can be explained;
- checking source-specific facts across enough locations that the investigation itself would distract from teaching.

Do not delegate merely because code is present. A focused question over one or a few obvious locations stays in the main context.

## Explorer contract

When the host can dispatch a temporary subagent, give it one bounded investigation question and ask for a compact evidence packet containing only:

- the question investigated;
- relevant files and symbols;
- the call/data flow when applicable;
- source-specific facts needed by the answer;
- uncertainty, conflicts, or unresolved points;
- useful precise source locations.

The explorer investigates; it does not teach. It must not:

- write or update `thread.yaml` or Question notes;
- decide what the learner should study next;
- invent a curriculum or prerequisite tree;
- produce the learner-facing explanation;
- preserve its scratch/search trail as durable learning output;
- recursively fan out into more agents unless the host's bounded investigation primitive inherently requires it.

After the explorer returns, keep only the findings that materially support the current question. The main agent then teaches normally under the existing Learn contract and remains responsible for uncertainty and source attribution.

If the host cannot dispatch a subagent, inspect the necessary sources in the main context and continue normally. Lack of subagent capability must never block learning.

## Persistence boundary

Exploration does not change V6 persistence. Record only the useful final explanation and relevant source locators. Never persist worker IDs, agent traces, search logs, or exploration scratch state.
