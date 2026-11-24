# The roadmap indexes initiatives; the tracker owns tickets

A roadmap row names one initiative with one outcome and a spec link, or `no spec yet`. It never lists ticket numbers. The status view's `Next` lists every open, unblocked, unclaimed ticket, with no trimming. We chose this because the roadmap had become a second ticket list. It named #33 while STATUS omitted it, so the files disagreed about the same work.

**Considered options:** Let the roadmap name tickets when an initiative has no spec, and keep `Next` short and curated. Rejected: a ticket list in the roadmap is a cache of tracker state that goes stale silently. A curated `Next` also hides open work exactly when a reader needs it.
