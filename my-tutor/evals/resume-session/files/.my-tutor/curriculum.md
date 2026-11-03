# Curriculum: HTTP request handling through bookmarks

## Goals

- Build a bookmark API in Node with no framework.
- Be able to explain middleware, route params and error handling.

## Scope

A JSON-file bookmark store behind an HTTP server. No database, no frontend.

## Modules

1. The store
   - Concepts: module state, pure functions
   - Exercises: 01 List bookmarks — return a copy so callers cannot mutate the store, 02 Route params — read an id from a path
2. Access control
   - Concepts: middleware, ownership checks
   - Exercises: 03 Auth middleware — decide whether a user may open a bookmark

## Skills

## Scopes

- `store`: `src/bookmarks.js`
- `auth`: `src/auth.js`
- `learning`: exercise files, tests and curriculum edits

## Test command

`npm test`
