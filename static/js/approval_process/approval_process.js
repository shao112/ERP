$("#approval_process_form").on("submit", function (event) {
    alert("#approval_process_form送出")
    event.preventDefault();
    var form = $(this);
    var formData = form.serialize();

    console.log("form data");
    console.log(formData);
    $.ajax({
        type: "post",
        url: "/restful/approval_process",
        data: formData,
        headers: {
            'X-CSRFToken': csrftoken
        },
        cache: false, 
        processData: false,
        contentType: false,
        success: function (response) {
            alert("操作成功");
        },
        error: function(error) {
            console.log('Error fetching events:', error);
        }
    });

});