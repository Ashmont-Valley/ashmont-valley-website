<script>
$(document).ready(function(){
    $("#new_note_btn").click(add_new_note())
});

function add_new_note() {
    $("#notes").before({% include "meetings/note.html" %})}
</script>
