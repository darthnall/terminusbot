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
  let phoneNumber = document.getElementById("phoneNumber");
  let vinNumber = document.getElementById("vinNumber");
if (phoneNumber.classList.contains("d-none")) && vinNumber.classList.contains("d-none") {
    toggleButton.innerText = "Hide Options";
    phoneNumber.classList.add("d-none");
    vinNumber.classList.add("d-none");
  } else {
    toggleButton.innerText = "Show Options";
    phoneNumber.classList.remove("d-none");
    vinNumber.classList.remove("d-none");
  }
}
