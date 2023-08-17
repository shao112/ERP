document.getElementById("approval_btn").onclick = handleApproval;

function handleApproval() {
    var statusValue = document.getElementById("status").value;
    var feedbackValue = document.getElementById("feedback").value;
    
    console.log("Status: " + statusValue);
    console.log("Feedback: " + feedbackValue);

    var formData = {
        status:statusValue,
        feedback:feedbackValue,
        Approval_id:Approval_id
    };

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
        success: function (response) {
            alert("操作成功");
        },
        error: function(error) {
            console.log('Error fetching events:', error);
        }
    });
};
