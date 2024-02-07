function performSearch() {
    // Obter o valor da pesquisa
    var query = document.getElementById('searchInput').value.toLowerCase();

    // Obter todos os cards
    var cards = document.querySelectorAll('.card');

    // Iterar sobre os cards e mostrar ou ocultar com base na pesquisa
    cards.forEach(function(card) {
        var title = card.querySelector('.card-title').innerText.toLowerCase();

        if (title.includes(query)) {
            card.style.display = 'block';  // Mostrar o card se a pesquisa for encontrada no título
        } else {
            card.style.display = 'none';  // Ocultar o card se a pesquisa não for encontrada no título
        }
    });
}