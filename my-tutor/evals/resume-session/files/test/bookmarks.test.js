import test from 'node:test';
import assert from 'node:assert/strict';
import { addBookmark, listBookmarks } from '../src/bookmarks.js';

test('addBookmark stores a bookmark with an id', () => {
  const bookmark = addBookmark({ url: 'https://example.com', title: 'Example' });
  assert.equal(bookmark.id, 1);
  assert.equal(bookmark.url, 'https://example.com');
});

test('listBookmarks returns a copy', () => {
  const all = listBookmarks();
  all.push({ id: 99 });
  assert.equal(listBookmarks().length, 1);
});
