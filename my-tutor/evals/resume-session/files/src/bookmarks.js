const bookmarks = [];

export function addBookmark({ url, title }) {
  const bookmark = { id: bookmarks.length + 1, url, title };
  bookmarks.push(bookmark);
  return bookmark;
}

export function listBookmarks() {
  return [...bookmarks];
}
