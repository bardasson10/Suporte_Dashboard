$(document).ready(function () {
  var table = $('#ticketTable').DataTable({
      "lengthMenu": [10, 25, 50, 100, 200], // Defina os valores desejados
      "pageLength": 10 // Defina o valor padrão
  });

});


  $(document).on('change', '#start_date, #end_date', function (e) {
    e.preventDefault(); 
  });

  $(document).ready(function () {
        // Obtenha o valor anteriormente selecionado do localStorage (se existir)
        var selectedOption = localStorage.getItem('is_closed_option');

        // Defina a opção selecionada no seletor
        if (selectedOption !== null) {
            $('#is_closed_option').val(selectedOption);
        }

        // Adicione um ouvinte de mudança ao seletor
        $('#is_closed_option').on('change', function () {
            // Salve a escolha do usuário no localStorage
            localStorage.setItem('is_closed_option', $(this).val());
        });
    });


    document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('exportButton').addEventListener('click', function () {
      exportTableToExcel('ticketTable');
    });

    function exportTableToExcel(tableId) {
      var wb = XLSX.utils.table_to_book(document.getElementById(tableId), { sheet: "Sheet JS" });
      var wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'binary' });

      function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
      }

      saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), 'table_tickets.xlsx');
    }
  });
