
$(document).ready(function() {

    // Provide ajax submition support
    $('form').click(function(event) {$(this).data('clicked',$(event.target))});
    $('form').submit(function(event) {
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

});

