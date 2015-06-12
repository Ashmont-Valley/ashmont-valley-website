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
      //there seems to be a problem with the permissions here
      success: function(response) {
        alert('yay!');
        $("#" + textid).val('');
        //will uncomment below lines when I get this working as is
        //data = JSON.parse(data);
        //receiveResult(null, {item: {pk: data['pk'], repr: data['name']}});
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

