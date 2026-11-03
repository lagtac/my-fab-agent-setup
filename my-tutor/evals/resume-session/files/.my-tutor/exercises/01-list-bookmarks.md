# Exercise 01: List bookmarks

**Goal:** Read the whole store without letting the caller change it.

**Concepts:** module state, pure functions

**Support:** worked example

**Files:** `src/bookmarks.js`

## Your tasks

1. Store a bookmark in the module and return it with an id.
2. List every bookmark so that a caller changing the list cannot change the store.

**Done when:** `npm test` passes `addBookmark stores a bookmark with an id`, `listBookmarks returns a copy`.

**Read:** https://nodejs.org/api/esm.html
