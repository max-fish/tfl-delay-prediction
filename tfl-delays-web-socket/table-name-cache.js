import lfuSet from 'collections/lfu-set.js';

const set = lfuSet([], 2000);

const addTableNameToCache = (tableName) => {
    set.add(tableName);
}

const hasTableNameInCache = (tableName) => {
    return set.has(tableName);
}

export { hasTableNameInCache, addTableNameToCache };