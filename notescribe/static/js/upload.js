/**
 * Removes "Confirm form resubmission on reload"
 */
const removeFormVerification = () => {
  if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }
}

removeFormVerification();

/**
 * Verifies file upload form
 * @param  {FormData} form
 * @return {boolean}
 */
const verifyUpload = (form) => {
  // add file verification here
  return true;
};
