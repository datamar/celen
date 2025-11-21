function showLoader() {
    // Affiche le loader et masque le contenu
    document.getElementById("loader").style.display = "block";
    document.getElementById("myDiv").style.display = "none";
}

function hideLoader() {
    // Masquer le loader et afficher le contenu
    document.getElementById("loader").style.display = "none";
    document.getElementById("myDiv").style.display = "block";

    // Invalidates Leaflet map size
    setTimeout(function () {
        if (typeof map !== 'undefined') {
            map.invalidateSize();
        }

        // Réinitialise Masonry après un délai pour s'assurer que tout est visible
        const masonryContainer = document.querySelector('[data-masonry]');
        if (masonryContainer) {
            const masonry = new Masonry(masonryContainer, {
                percentPosition: true,
            });
            masonry.layout();
        }
    }, 100); // Délai pour permettre le rendu des éléments
}

window.onload = function () {
    if (typeof mapIsLoading !== 'undefined' && mapIsLoading === true) {
        // Si une carte est en cours de chargement, on attend l'événement 'mapLoaded'
        document.addEventListener('mapLoaded', function () {
            hideLoader();
        });
    } else {
        // Pas de carte en cours de chargement, on peut cacher le loader immédiatement
        hideLoader();
    }
};

// Gestion du retour arrière (back) du navigateur
window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        hideLoader();
    }
});
