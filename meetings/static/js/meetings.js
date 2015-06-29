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

function showNoteEdit(id) {
  var form = $('#'+id+'-update');
  if(form.hasClass('hidden')) {
    $('#'+id).addClass('hidden');
    form.removeClass("hidden");
    var el = $('#'+id+'-input')[0];
    el.selectionStart = 0;
    el.selectionEnd = el.value.length;
    el.focus();
  }
};
function hideNoteEdit(id) {
  $("#" + id + "-update").addClass("hidden");
  $("#" + id).removeClass('hidden');
}

function update_note(event) {
  var obj = $(this).prev();
  if(!$(this).hasClass('hidden')) {
    var id = obj[0].id;
    var new_text = $("#" + id + "-input").val();
    $("#" + id + "-text").text(new_text);
    obj.removeClass("bg-success").addClass("bg-danger");
    hideNoteEdit(id);
    $(this).submit()
  }
  $.ajax({
    method: this.method,
    url:    this.action,
    data:   $(this).serialize(),
    success: function(response) {
      obj.removeClass("bg-danger").addClass("bg-success");
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
  $('.note .txt').on('click', function(event) { showNoteEdit(this.parentNode.id); });
  $('.update_note').on('focusout', function() { $(this).submit(); }); 
  $('#notes').on('submit', '.update_note', update_note);
  $('#notes').on('submit', '.delete_note', delete_note);
});

