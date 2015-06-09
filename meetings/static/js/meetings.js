
$(document).ready(function() {

    // Provide ajax submission support
    $('#add_note').click(function(event) {$(this).data('clicked',$(event.target))});
    $('#add_note').submit(function(event) {
      var button = $(this).data('clicked');
      if(button.data('ajax')) {
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
      }
      return true;
    });

    $('.delete_note').click(function(event) {$(this).data('clicked',$(event.target))});
    $('.delete_note').submit(function(event) {
      var button = $(this).data('clicked');
      if(button.data('ajax')) {
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
      }
      return true;
    });

});

