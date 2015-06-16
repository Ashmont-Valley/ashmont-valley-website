function add_person(event) {
  var textid = this.getAttribute('data-textid');
  var target = this.getAttribute('data-target');
  if($("#" + textid).val()) {
    $.ajax({
      method: 'post',
      url:    target,
      data:   {
        name: $("#" + textid).val(),
      },
      success: function(data) {
        //this is a function in the ajax-selects js file. How can we access it? It isn't recognized right now.
        receiveResult(null, {item: {pk: data['pk'], repr: data['name']}});
      },
      error: function(response) {
        alert('error');
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
