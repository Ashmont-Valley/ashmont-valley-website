
$(document).ready(function() {

    // Provide ajax submition support
    $('form').click(function(event) {$(this).data('clicked',$(event.target))});
    $('form').submit(function(event) {
      var button = $(this).data('clicked');
      if(button.data('ajax')) {
        $.ajax({
          method: this.method,
          url:    this.target,
          data:   $(this).serialize(),
          success: function(response) {
            //form.find('.form_result').html(response);
            $(button).html("Saved!");
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

