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
        $("#" + htmlid).trigger('didAddPopup', [data['pk'], data['name']]);
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

    
    if($("#" + html_id).data('ajax-select')==='autocompleteselect') {

      $(document).click(function(event) {
        var add_person_btn = $("#" + html_id + "_add_person_btn");
        var textbox = $("#" + html_id + "_text");
        if(!textbox.is(event.target) && !add_person_btn.is(event.target)) {
          if(textbox.val()) {
            $("#" + html_id + "_on_deck span").remove();
            textbox.val($("#" + html_id + "_on_deck").text());
          } else{
            //remove current person from position if blank
            $("#" + html_id + "_on_deck span").click();
          }
        }
      });

      $("#" + html_id + "_on_deck").on('added', function(event, pk, item) {
        $("#" + html_id + "_text").val(item.repr);
      });

    }

    $("#" + html_id + "_text").keypress(function(event) {
      if(event.keyCode == 13) {
        //event.preventDefault();
        //if the enter key is pressed when inside a textbox
        var btn = $("#" + html_id + "_wrapper .add_person_btn");
        add_person.call(btn[0]);
        return false;
      }
    }); //.bind('keyup keydown', function(event) {return event.keyCode != 13});

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
})(window.jQuery);
