# The roadmap's "Now" mirrors the status view's "Active"

A roadmap row is `Now` only while its work is being done or is next in line, the state the status view calls `Active`. We chose one axis because two axes let the roadmap claim work is "in flight" while the status view reports it waiting on a human, which is the drift we kept correcting by hand. A human-blocked item sits in `Next` with a note.

**Considered options:** Keep two axes, where `Now` means "committed to fund this horizon" and `Active` means "an agent is working it". Rejected: it guarantees a standing Now-versus-Active mismatch, and the commitment is already visible in the row's presence.
