---
title: Drills index
type: index
track: universal
status: drafted
updated: 2026-09-02
tags: [index, practice]
---

# Drills — how you actually get good at this

Reading case files does not make you better at the round. **Designing under a timer, out loud,
then diffing against a reference** does. This folder is the practice loop.

## Where to look

| Question | File |
|---|---|
| What do I do, week by week? | [8-week-plan.md](8-week-plan.md) |
| How do I know if my answer was good? | [self-scoring-rubric.md](self-scoring-rubric.md) |
| What should I practise on? | [question-bank.md](question-bank.md) |
| What must I recall instantly? | [flashcards.md](flashcards.md) |
| Log a practice session | [../_templates/drill-log-template.md](../_templates/drill-log-template.md) |

## The loop

```
1. Pick a problem from the question bank
2. Timer 40 min. Paper or whiteboard. TALK OUT LOUD — record yourself
3. Score with the rubric BEFORE reading the reference
4. Read the reference case file. Diff. Log it
5. The diff becomes your study list for the week
6. Re-drill the same problem 7 days later. You should beat your score
```

## Rules that make the loop work

| Rule | Why |
|---|---|
| **Always use a timer** | Time pressure is the actual skill; unbounded practice trains nothing |
| **Always speak out loud** | The round is scored on communication, not on your diagram |
| **Record yourself and watch it back once** | Painful, and the fastest feedback available without a partner |
| **Score before reading the answer** | Otherwise you score your reading comprehension, not your design |
| **Re-drill, don't collect** | Doing 30 problems once is worse than doing 10 problems three times |
| **Log every session** | The pattern in your misses is your curriculum |

## Common misses, and what they mean

| You keep missing | Fix |
|---|---|
| Estimates | Drill [../01-numbers.md](../01-numbers.md) until the arithmetic is automatic |
| Data model / partition key | The highest-value 30 minutes you can spend — re-read [../02-primitives/replication-and-partitioning.md](../02-primitives/replication-and-partitioning.md) |
| Ran out of time before failure/cost | Announce the plan at minute 5 and keep to it; cut the deep dive short, never the last section |
| Silent thinking | Practise narrating; record and count your silences |
| Buzzwords without reasons | For each box, force yourself to say "because \<requirement\>" out loud |

## Mock interviews

Solo practice plateaus. Get real mocks:

- A friend reads only §1–2 of a case file and plays the interviewer with the rest open.
- Paid platforms (Exponent, Pramp, interviewing.io, Hello Interview) — see
  [../10-resources/courses-and-mocks.md](../10-resources/courses-and-mocks.md).
- Your own recording, watched a day later, is the cheapest and works better than people expect.
