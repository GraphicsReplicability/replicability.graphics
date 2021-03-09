/**
 *  Sorts all arrays together with the first. Pass either a list of arrays, or a map. Any key is accepted.
 *     Array|Object arrays               [sortableArray, ...otherArrays]; {sortableArray: [], secondaryArray: [], ...}
 *     Function comparator(?,?) -> int   optional compareFunction, compatible with Array.sort(compareFunction)
  Source: https://gist.github.com/boukeversteegh/3219ffb912ac6ef7282b1f5ce7a379ad
 */
function sortArrays(arrays, comparator = (a, b) => (a < b) ? -1 : (a > b) ? 1 : 0) {
  let arrayKeys = Object.keys(arrays);
  let sortableArray = Object.values(arrays)[0];
  let indexes = Object.keys(sortableArray);
  let sortedIndexes = indexes.sort((a, b) => comparator(sortableArray[a], sortableArray[b]));

  let sortByIndexes = (array, sortedIndexes) => sortedIndexes.map(sortedIndex => array[sortedIndex]);

  if (Array.isArray(arrays)) {
    return arrayKeys.map(arrayIndex => sortByIndexes(arrays[arrayIndex], sortedIndexes));
  } else {
    let sortedArrays = {};
    arrayKeys.forEach((arrayKey) => {
      sortedArrays[arrayKey] = sortByIndexes(arrays[arrayKey], sortedIndexes);
    });
    return sortedArrays;
  }
}
