(function ($) {

function add_person(event) {
  var htmlid = this.getAttribute('data-htmlid');
  var target = this.getAttribute('data-target');
  
  $('.ui-autocomplete').empty();

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
    var textbox = $("#" + html_id + "_text");
    var wrapper = $("#" + html_id + "_wrapper");
    var deck = $("#" + html_id + "_on_deck");

    textbox.keypress(function(event) {
      if(event.keyCode == 13) {
        //if the enter key is pressed when inside a textbox
        var btn = $("#" + html_id + "_wrapper .add_person_btn");
        add_person.call(btn[0]);
        return false;
      } 
    }); //.bind('keyup keydown', function(event) {return event.keyCode != 13});

    var select = $("#" + html_id).data('ajax-select');
    $('.ui-icon-trash').addClass('close').removeClass('ui-icon ui-icon-trash');

    if(select === 'autocompleteselectmultiple') {
      deck.on('added', function(event, pk, item) {
        $('.ui-icon-trash').addClass('close').removeClass('ui-icon ui-icon-trash');
      });
    } else if(select === 'autocompleteselect') {
      function addSuccess() {
        wrapper.addClass('has-success');
        wrapper.removeClass('has-error');
        $("#" + html_id + "_wrapper .red-remove").addClass('hidden');
        $("#" + html_id + "_wrapper .green-ok").removeClass('hidden');
      }

      function rmSuccess() {
        wrapper.addClass('has-error');
        wrapper.removeClass('has-success');
        $("#" + html_id + "_wrapper .green-ok").addClass('hidden');
        $("#" + html_id + "_wrapper .red-remove").removeClass('hidden');
      }

      if(!(deck.is(':empty'))) {
        addSuccess();
      } else {
        rmSuccess();
      }

      $(document).click(function(event) {
        var add_person_btn = $("#" + html_id + "_add_person_btn");
        if(!textbox.is(event.target) && !add_person_btn.is(event.target)) {
          if(textbox.val()) {
            textbox.val($.trim(deck.text().substring(1)));
          } else {
            //remove current person from position if textbox is blank
            $("#" + html_id + "_on_deck span").click();
          }
        }
      });

      deck.on('added', function(event, pk, item) {
        textbox.val(item.repr);
        addSuccess();
      });


      textbox.keyup(function(event) {
        if(!(deck.is(':empty'))) {
          var current_name = $.trim(deck.text().substring(1));
          var new_name = textbox.val();
          if(!(new_name === current_name)) {
            //remove current person from position
            $("#" + html_id + "_on_deck span").click();
            rmSuccess();
            textbox.val(new_name);
          }
        }
      });
    }
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
