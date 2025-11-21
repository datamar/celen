// Add load event listener.
window.addEventListener("load", loadTime, false);

function loadTime() {
  // Get current time.
  var now = new Date().getTime();
  // Calculate page load time.
  var page_load_time = now - performance.timing.navigationStart;
  var loadTimeElement = document.getElementById("loadTime");

  // Afficher le temps de chargement dans l'élément sélectionné
  loadTimeElement.innerText = page_load_time + " ms";
};