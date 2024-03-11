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

alertModalCloseButton.on("click", () => {
  closeAlertModal();
});

function showAlertModal(type, message) {
  // Add a class based on the message type
  switch (type) {
    case "INFO":
      alertModal.addClass("info");
      break;
    case "SUCCESS":
      alertModal.addClass("success");
      break;
    case "WARNING":
      alertModal.addClass("warning");
      break;
    case "ERROR":
      alertModal.addClass("error");
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
