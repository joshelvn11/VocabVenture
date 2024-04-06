// Mobile Nav Controls
const sideBarNav = $("#sidebar-nav");
const menuBackgroundOverlay = $("#menu-background-overlay");

$("#mobile-nav-open").on("click", () => {
  sideBarNav.addClass("active");
  menuBackgroundOverlay.removeClass("hidden");
});

$("#mobile-nav-close").on("click", () => {
  sideBarNav.removeClass("active");
  menuBackgroundOverlay.addClass("hidden");
});

menuBackgroundOverlay.on("click", () => {
  sideBarNav.removeClass("active");
  menuBackgroundOverlay.addClass("hidden");
});

const alertModalContainer = $("#alert-modal-container");

function showAlertModal(type, message) {
  console.log("Showing alert modal");
  const alertModal = $(`
  <div id="alert-modal" class="${type.toLowerCase()}">
    <p id="alert-title">${type}</p>
    <p id="alert-message">${message}</p>
    <button id="alert-modal-close-button" class="close-button">x</button>
  </div>`);

  const alertModalCloseButton = alertModal.find("#alert-modal-close-button");

  alertModalCloseButton.on("click", () => {
    closeAlertModal(alertModal);
  });

  // Add the alert modal to the container
  alertModalContainer.prepend(alertModal);

  // Close the modal after eight seconds
  setTimeout(() => {
    closeAlertModal(alertModal);
  }, 8000);
}

function closeAlertModal(alertModal) {
  // Remove the modal from the DOM
  alertModal.remove();
}

const profileButton = $("#nav-profile-button");
const profileSubMenu = $("#nav-profile-submenu");

profileButton.on("click", () => {
  console.log("toggling");
  profileSubMenu.toggleClass("hidden");
});

window.addEventListener("resize", () => {
  const originalHeight = window.innerHeight;
  document.body.style.height = originalHeight + "px";
});
