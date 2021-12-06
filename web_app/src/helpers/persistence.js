const DB_NAME = 'roadsafety-digital-forms';
const DB_VERSION = 1;
const FORMS_OBJECT_STORE = 'forms'

import { openDB } from 'idb';


const dbPromise = openDB(DB_NAME, DB_VERSION, {
  upgrade(db) {
    db.createObjectStore(FORMS_OBJECT_STORE)
  },
});

async function all() {
	return (await dbPromise).getAll(FORMS_OBJECT_STORE);
}

async function get(key) {
	return (await dbPromise).get(FORMS_OBJECT_STORE, key);
}

async function updateOrCreate(key, value) {
  return (await dbPromise).put(FORMS_OBJECT_STORE, value, key);
}

async function del(key) {
  return (await dbPromise).delete(FORMS_OBJECT_STORE, key);
}

async function clear() {
  return (await dbPromise).clear(FORMS_OBJECT_STORE);
}

async function keys() {
  return (await dbPromise).getAllKeys(FORMS_OBJECT_STORE);
}

export default { get, updateOrCreate, del, clear, keys, all}