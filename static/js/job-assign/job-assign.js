function getcsrftoken() {
    var name = "csrftoken";
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$("#attendance_date_select2").select2({
    tags: true,
    tokenSeparators: [',', ' ']
})




var projectConfirmationIdControl = document.getElementById('project_confirmation_id');

projectConfirmationIdControl.addEventListener('change', function () {

    var selectedOptionIndex = projectConfirmationIdControl.selectedIndex;
    var selectedOption = projectConfirmationIdControl.options[selectedOptionIndex];
    var selectedId = selectedOption.value;

    console.log('選中的選項 id 為: ' + selectedId);

    const url = "/restful/project_confirmation";
    formData = { id: selectedId };

    $.ajax({
        type: "GET",
        url: url,
        headers: {
            'X-CSRFToken': getcsrftoken()
        },
        data: formData,
        success: function (response) {

                jsonData = response.data
                document.getElementById("project_name").value = jsonData["project_name"];
                document.getElementById("c_a").value = jsonData["c_a"];

                
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("job_assign js error")
            console.log("get error");
        }
    });



});
