if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
/**
 *
 * @param {FormData} form
 * @returns {boolean}
 */
const verifyUpload = (form) => {
  // add file verification here
  return true;
};
