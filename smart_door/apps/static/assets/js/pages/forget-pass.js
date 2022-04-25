'use strict';
$(document).ready(function() {
    console.log("Test");
    $("#forget_pass_submit").click((e) => {
        // e.preventDefault();
        let username = $("#id_username").val();
        console.log(username);
    });
});