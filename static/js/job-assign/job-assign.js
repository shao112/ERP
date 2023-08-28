
var projectConfirmationIdControl = document.getElementById('project_confirmation_select2');

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
            'X-CSRFToken': csrftoken
        },
        data: formData,
        success: function (response) {
                jsonData = response.data
                console.log(jsonData["project_name"],jsonData["c_a"])
                document.getElementsByName("project_name")[0].value = jsonData["project_name"];
                document.getElementsByName("c_a")[0].value = jsonData["c_a"];

                
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("job_assign js error")
            console.log("get error");
        }
    });



});
