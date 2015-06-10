function add_note(event) {
  $.ajax({
    method: this.method,
    url:    this.action,
    data:   $(this).serialize(),
    success: function(response) {
      $(response).insertBefore('#add_note');
      $('#note_text_box').val("");
    },
    error: function(response) {
      document.write(response);
    }
  });
  return false;
};

function delete_note(event) {
  $.ajax({
    method: this.method,
    url:    this.action,
    data:   $(this).serialize(),
    success: function(response) {
      $("#mnote-".concat(response)).remove();
    },
    error: function(response) {
      document.write(response);
    }
  });
  return false;
};

$(document).ready(function() {

  // Provide ajax submission support
  $('#add_note').submit(add_note)

  $('#notes').on('submit', '.delete_note', delete_note)

});

