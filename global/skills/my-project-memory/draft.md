# Project memory orchestrator

Each of the four files answers one question about a different point in time. The roadmap covers the future, the status the present, the worklog the recent past, and the changelog the released past. A fact belongs in the one file whose question it answers. The others link to it.

---

The roadmap asks: what will we build next, and in what order? Why does each item matter? Which items are committed, and which are only ideas? What will we not build, and why?

A roadmap row is an initiative. A ticket belongs in the tracker. The tracker owns the blocking edges; the roadmap owns the order of investment.

---

The status asks: what works today, and what is broken? What is in progress now? What blocks progress, and who can remove the block? What must a new reader know before changing anything? When did someone last verify the file?

STATUS is rewritten in place. It always describes the current state and holds no history. It is a view over the tracker, so it holds no fact of its own.

---

The worklog asks: what did this session do? What did we try that failed, and why? What did we decide, and why? Where should the next session start?

The worklog is append-only. New entries go at the end, and earlier entries never change.

---

The changelog asks: what is new, changed, fixed, or removed in each release? Which changes break existing use, and how does a user adapt? When was each release?

The changelog holds what a user sees. Internal work stays out, and the work steps stay in the worklog.

---

#28 is the case that proves the gap. The banner landed in `d5e9913` and `494a984`, the issue closed, and only STATUS was updated. The changelog never learned about the banner, and the worklog never recorded the session.

---

#23 to #26 are the other direction. The code landed on `main`, but the issues stayed open. STATUS rendered the tracker, so the view showed work as unfinished while the code was live.

---

The four skills each said "commit this file alone". The global git rule says never commit unless the user or a skill asks. The answer: leave a memory edit uncommitted unless the session asked for commits. The skills' commit sections now say the same.

---

The orchestrating rule is a sequence. Read the status view before planning. Update the tracker when work starts, blocks, lands, or closes. Write the landed fact to its file. The per-file mapping is reference, consulted only when something lands.

---

The rule is always loaded; the four skills are loaded on demand. The rule routes. The skills hold the shapes.

---

One leading word anchors the set: "project memory". The four files are its lifecycle.
