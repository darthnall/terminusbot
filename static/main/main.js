const defaultFormat = "'s Ride";
let autoUpdateEnabled = true;
const toggleOptionalFieldsButton = document.getElementById('toggleOptionalFields');

function updateAssetName() {
  let firstNameValue = document.getElementById("firstName").value;

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
});
