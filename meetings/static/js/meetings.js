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

$.fn.showNoteEdit = function() {
  var update_note_form = $(this).children(".update_note");
  if(update_note_form.hasClass('hidden')) {
    update_note_form.removeClass("hidden");
    $(this).children('.txt').addClass('hidden');
    var el = update_note_form.children('input')[1];
    var elemLen = el.value.length;
    el.selectionStart = elemLen;
    el.selectionEnd = elemLen;
    el.focus();
  }
};
$.fn.hideNoteEdit = function(id) {
  $("#" + id).addClass("hidden");
  $("#" + id + "-text").removeClass('hidden');
};

function update_note(event) {
  var id = this.getAttribute('id');
  $.ajax({
    method: this.method,
    url:    this.action,
    data:   $(this).serialize(),
    success: function(response) {
      var new_text = $("#" + id + "-input").val();
      $("#" + id + "-text").text(new_text);
      $(this).hideNoteEdit(id);
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
  $('#add_note').submit(add_note);
  $('.note').on('click', function(event) {
    $(this).showNoteEdit()
  });
  $('.note .update_note').on('focusout', function() { 
    if(!$(this).hasClass('hidden')) {
      var id = this.id;
      var new_text = $("#" + id + "-input").val();
      $("#" + id + "-text").text(new_text);
      $(this).hideNoteEdit(id);
      $(this).submit()
    }
  });
  $('#notes').on('submit', '.update_note', update_note);
  $('#notes').on('submit', '.delete_note', delete_note);
});

