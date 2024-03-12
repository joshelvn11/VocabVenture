// Mobile Nav Controls

const sideBarNav = $("#sidebar-nav");

$("#mobile-nav-open").on("click", () => {
  sideBarNav.addClass("active");
});

$("#mobile-nav-close").on("click", () => {
  sideBarNav.removeClass("active");
});

const alertModal = $("#alert-modal");
const alertModalCloseButton = $("#alert-modal-close-button");
const alerModalTitle = $("#alert-title");
const alerModalMessage = $("#alert-message");

alertModalCloseButton.on("click", () => {
  closeAlertModal();
});

function showAlertModal(type, message) {
  // Add a class based on the message type
  switch (type) {
    case "INFO":
      alertModal.addClass("info");
      alerModalTitle.text("Info");
      alerModalMessage.text(message);
      break;
    case "SUCCESS":
      alertModal.addClass("success");
      alerModalTitle.text("Success");
      alerModalMessage.text(message);
      break;
    case "WARNING":
      alertModal.addClass("warning");
      alerModalTitle.text("Warning");
      alerModalMessage.text(message);
      break;
    case "ERROR":
      alertModal.addClass("error");
      alerModalTitle.text("Error");
      alerModalMessage.text(message);
      break;
  }

  // Show the modal
  alertModal.removeClass("hidden");
  // Close the modal after eight seconds
  setTimeout(closeAlertModal, 8000);
}

function closeAlertModal() {
  // Remove the alert type class
  alertModal.removeClass("success info warning error");
  // Hide the modal
  alertModal.addClass("hidden");
}
