// Get all the tour hint close buttons on the page

$(".tour-hint-close-button").on("click", function () {
  // Hide the hint element
  $(this).parent().addClass("hidden");

  fetch(`/api/user-meta/update-hint?hint-id=${$(this).attr("hint-id")}`, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        console.log("Error in response");
      }
      return response.json(); // Parse the response body as JSON
    })
    .then((data) => {
      responseData = data.data;
      console.log(responseData);
    });
});
