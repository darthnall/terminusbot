const defaultFormat = "'s Ride";
const toggleOptionalFieldsButton = document.getElementById('toggleOptionalFields');

let autoUpdateEnabled = true;
let toggleOptionalFieldsButtonState = "Show";

function updateAssetName() {
  const firstNameValue = document.getElementById("firstName").value;

  if (autoUpdateEnabled) {
    document.getElementById("assetName").value = firstNameValue + defaultFormat;
  }
}

function disableAutoUpdate(event) {
  if (event.isTrusted) {
    autoUpdateEnabled = false;
  }
}

toggleOptionalFieldsButton.addEventListener('click', function() {
  const hiddenElements = document.getElementsByClassName('starts-hidden');
  for (let i = 0; i < hiddenElements.length; i++) {
    hiddenElements[i].classList.toggle('hidden');
  }
  if (hiddenElements[0].classList.contains('hidden')) {
    toggleOptionalFieldsButtonState = "Show";
    } else {
    toggleOptionalFieldsButtonState = "Hide";
    }
  toggleOptionalFieldsButton.textContent = toggleOptionalFieldsButtonState;
});
