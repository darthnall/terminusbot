const defaultFormat = "'s Ride";
let autoUpdateEnabled = true;
let toggleButton = document.getElementById("toggle");

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

function toggleOptionalFields() {
  let optionalFields = document.getElementById("optionalFields");
  if (optionalFields.classList.contains("d-none")) {
    toggleButton.innerText = "Hide Options";
    optionalFields.classList.toggle("d-none");
  } else {
    toggleButton.innerText = "Show Options";
    optionalFields.classList.toggle("d-none");
  }
}
