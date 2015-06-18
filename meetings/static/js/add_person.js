(function ($) {
function add_person(event) {
  var htmlid = this.getAttribute('data-htmlid');
  var target = this.getAttribute('data-target');
  if($("#" + htmlid + "_text").val()) {
    $.ajax({
      method: 'post',
      url:    target,
      data:   {
        name: $("#" + htmlid + "_text").val(),
      },
      success: function(data) {
        //the trigger doesn't seem to be working
        $("#" + htmlid).trigger('didAddPopup', [data['pk'], data['name']]);
        alert('nope');
      },
      error: function(response) {
        //This is a stopgap measure at best for making sure that we don't get dozens of person objects with the same name.
        alert('There was an error. It could be that you are trying to create a person that already exists');
        //document.write(response);
      },
    });
  }
};

$(document).ready(function() {
  $(".add_person_btn").click(add_person);
});

//the following functions make csrf token work with ajax requests
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
})(django.jQuery);
