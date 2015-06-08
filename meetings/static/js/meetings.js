
$(document).ready(function() {

    // Provide ajax submission support
    $('.note_form').click(function(event) {$(this).data('clicked',$(event.target))});
    $('.note_form').submit(function(event) {
      var button = $(this).data('clicked');
      if(button.data('ajax')) {
        $.ajax({
          method: this.method,
          url:    this.action,
          data:   $(this).serialize(),
          success: function(response) {
            $(response).insertBefore('#note_form');
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
            $(this.parent).remove();
          },
          error: function(response) {
            alert("oh no!")
            //document.write(response);
          }
        });
        return false;
      }
      return true;
    });

    
       
});

