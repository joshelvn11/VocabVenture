// Mobile Nav Controls
const sideBarNav = $("#sidebar-nav");

$("#mobile-nav-open").on("click", () => {
  sideBarNav.addClass("active");
});

$("#mobile-nav-close").on("click", () => {
  sideBarNav.removeClass("active");
});

const alertModalContainer = $("#alert-modal-container");

function showAlertModal(type, message) {
  console.log("Showing alert modal");
  const alertModal = $(`
  <div id="alert-modal" class="${type.toLowerCase()}">
    <p id="alert-title">${type}</p>
    <p id="alert-message">${message}</p>
    <button id="alert-modal-close-button" class="icon-button">
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M61.7932 56.5976L37.6569 32L61.7178 7.40241L61.7932 7.3253C63.1509 5.78313 63.1509 3.39277 61.7178 2.00482C60.9635 1.23374 59.983 0.848193 58.927 0.848193C57.9465 0.848193 57.0414 1.31084 56.3625 2.00482L32.3017 26.6024L7.48662 1.15663C6.73236 0.385542 5.75182 0 4.69586 0C3.71533 0 2.81022 0.462651 2.13139 1.15663C1.45255 1.92771 1 2.93012 1.07543 3.93253C1.07543 4.93494 1.52798 5.86024 2.20681 6.55422L27.0219 32L2.13139 57.4458C1.37713 58.2169 1 59.2193 1 60.2988C1 61.3012 1.45255 62.2265 2.13139 62.9205C2.65937 63.3831 3.48905 64 4.77129 64C6.12895 64 6.95864 63.3831 7.48662 62.9205L32.3771 37.4747L56.438 62.0723C56.9659 62.612 57.7956 63.1518 59.1533 63.1518C60.5109 63.1518 61.3406 62.5349 61.8686 62.0723C62.6229 61.3012 63 60.2988 63 59.2193C62.9246 58.2169 62.5474 57.2916 61.7932 56.5976Z" fill="black"/>
        </svg>            
    </button>
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
