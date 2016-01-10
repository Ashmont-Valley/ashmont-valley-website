$(document).ready(function() {
  connect_table_ajax();
});

function connect_table_ajax() {
  $('[data-table-ajax]').each(function() {
    $(this).click(run_table_ajax);
  });
}

function run_table_ajax() {
  var url = $(this).data('table-ajax');
  var table = $(this).closest('table');

  $.get( url, function(data) {
    $(table).html( data );
    connect_table_ajax();
  });
  return false;
}
