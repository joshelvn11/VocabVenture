// Mobile Nav Controls

const sideBarNav = $("#sidebar-nav");

$("#mobile-nav-open").on("click", () => {
  sideBarNav.addClass("active");
});

$("#mobile-nav-close").on("click", () => {
  sideBarNav.removeClass("active");
});
