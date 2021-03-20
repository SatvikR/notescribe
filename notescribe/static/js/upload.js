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
  if (form.file.value === '') {
    alert('No file selected.')
    return false;
  }
  return true;
};
