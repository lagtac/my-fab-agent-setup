import test from 'node:test';
import assert from 'node:assert/strict';
import { checkAccess } from '../src/auth.js';

const owner = { id: 7, name: 'dimitris' };
const stranger = { id: 8, name: 'sam' };

test('a public bookmark is open to anyone', () => {
  const bookmark = { id: 1, ownerId: 7, public: true };
  assert.equal(checkAccess(bookmark, stranger), true);
});

test('a private bookmark is open to its owner', () => {
  const bookmark = { id: 2, ownerId: 7, public: false };
  assert.equal(checkAccess(bookmark, owner), true);
});

test('a private bookmark is closed to a stranger', () => {
  const bookmark = { id: 3, ownerId: 7, public: false };
  assert.equal(checkAccess(bookmark, stranger), false);
});
