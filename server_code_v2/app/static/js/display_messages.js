//For deleting a message
//May have to make this more secure
function delete_msg(id) {
    $.post("/delete-msg", {"id":id}, function(result) {
        window.location.replace('/')
    })
}
