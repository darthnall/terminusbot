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
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false,
    );
  });
})();
