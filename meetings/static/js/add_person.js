(function ($) {
function add_person(event) {
  var htmlid = this.getAttribute('data-htmlid');
  var target = this.getAttribute('data-target');

  var textBox = $("#" + htmlid + "_text");
  $(textBox[0]).trigger('didAddPopup', '1', 'It Works');
  return false;

  if($("#" + htmlid + "_text").val()) {
    $.ajax({
      method: 'post',
      url:    target,
      data:   {
        name: $("#" + htmlid + "_text").val(),
      },
      success: function(data) {
        //the trigger doesn't seem to be working
        //$("#" + htmlid).trigger('didAddPopup', [data['pk'], data['name']]);
        //$(textBox[0]).trigger('didAddPopup', data['pk'], data['name']);
        //$("#" + htmlid + "_wrapper").trigger('didAddPopup', [data['pk'], data['name']]);
        //$("#" + htmlid + "_on_deck").trigger('didAddPopup', [data['pk'], data['name']]);
        alert('post successful');
      },
      error: function(response) {
        alert('There was an error' + response.status);
        //document.write(response);
      },
    });
  }
}

$(document).ready(function() {
  $(".add_person_btn").click(add_person);

  $('.autoselect').each(function() {
    var html_id = this.getAttribute('id');

  //$("#" + html_id + "_on_deck").empty();

  $(document).click(function(event) {
    var textbox = $("#" + html_id + "_text");
    var add_person_btn = $("#" + html_id + "_add_person_btn");
    if (!textbox.is(event.target) && !add_person_btn.is(event.target)) {
      $("#" + html_id + "_on_deck span").remove();
      textbox.val($("#" + html_id + "_on_deck").text());
    }
  });

  $("#" + html_id + "_text").keypress(function(event) {
    if(event.keyCode == 13) {
      //event.preventDefault();
      //if the enter key is pressed when inside a textbox
      var btn = $("#" + html_id + "_wrapper .add_person_btn");
      add_person.call(btn[0]);
      return false;
    }
  }); //.bind('keyup keydown', function(event) {return event.keyCode != 13});

  //the following works with the admin but not with the front end for some reason
  /*$("#" + html_id + "_on_deck").on('added', function(event, pk, item) {
    $(this).empty();
    var textbox = $("#" + html_id + "_text");
    textbox.val(item.repr);
    textbox.data('current-repr', item.repr);
  });*/
});
});

//the following functions make csrf tokens work with ajax requests
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
