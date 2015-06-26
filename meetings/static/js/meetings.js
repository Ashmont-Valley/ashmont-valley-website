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

function update_note(event) {
  $.ajax({
    method: this.method,
    url:    this.action,
    data:   $(this).serialize(),
    success: function(response) {
      alert("successfully updated note");
      var new_text = $(this).children("input").val();
      $("#" + this.id + "-text").text(new_text);
    },
    error: function(response) {
      alert($(this).serialize());
      //document.write(response);
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
  $('#add_note').submit(add_note);
  $('#notes').on('submit', '.update_note', update_note);
  $('#notes').on('submit', '.delete_note', delete_note);
});

