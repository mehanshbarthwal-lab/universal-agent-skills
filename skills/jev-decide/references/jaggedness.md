# Jev Known Failure Modes and Prevention Guidelines

Distilled from TypeSafe official documentation (docs.typesafe.ai/model-jaggedness). Read this before writing any question for jev decide. Every failure mode below has a concrete fix.

## It answers the question you wrote, not the one you meant

Scoping words, negations, and implied conditions are read literally. A question like "is this urgent?" with no further detail will get answered on whatever the default sense of urgent is, which may not match yours.

**Fix**: State the exact condition and put boundary cases directly in the instructions or in the option or level descriptions. Compare:

* Weak: `"Is this ticket urgent?"`
* Better: `"Does the ticket mention a deadline within 24 hours, an active outage, or explicit financial loss happening right now? A ticket that is merely annoying or important but not time bound is NOT urgent."`

## It is not a calculator

Jev does not count reliably: characters in a word, occurrences of a term, items in a list. It recognizes the shape of an answer rather than tallying, and the error grows with the size of what is being counted.

**Fix**: Never ask it to count. If you need a count of items matching some criteria, iterate in code and ask one yes or no question per item, then add up the answers yourself. Any arithmetic like totals, percentages, differences stays in code, not in the question.

## Dates and numeric precision

Related to the above: dates are read as text, not as ordered values, and anything needing numeric precision is unreliable. Do not ask "is date A before date B"; compute that in code and only ask semantic questions about the result if needed.

## Large state full of irrelevant detail

Accuracy decays as the state dictionary grows noisy. A big state with mostly irrelevant fields makes the small number of relevant ones harder to weigh correctly.

**Fix**: Filter first, in code, before sending state. Only include what the specific question actually needs. Truncate long text fields rather than sending everything.

## Extra levels of indirection

Jev can struggle when a question requires reasoning several steps removed from the state it is given ("does X imply that Y would probably lead to Z").

**Fix**: Break multi step reasoning into separate questions, each one hop from the state, rather than one question that chains several inferences together.

## Adversarial or untrusted content in state

Content inside state can move the answer, including content designed to manipulate decisions. If any part of the state came from an external source (a web page, a user uploaded file, an email), treat the answer with caution, and do not let a single Jev answer alone authorize something sensitive.

## Contradictory instructions and criteria

It will not reconcile a conflict between the question instructions and an option description if they disagree. Keep the two consistent when writing options or levels.

## Structural invariants are not guaranteed

Two separate calls, even about very similar situations, are not guaranteed to stay consistent with each other. Do not rely on Jev to enforce something like "exactly one of these should ever be true across calls" without checking it in code.

## It cannot generate text

No text, no drafts, no code, no explanations. If the task needs output someone will read as prose, this is not the right tool for that part of the task.
