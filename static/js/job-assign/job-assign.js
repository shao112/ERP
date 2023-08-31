
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
                var form = document.querySelector('form[name="job_assign"]');
                var projectName = form.querySelectorAll('[name="project_name"]')[0];
                var c_a = form.querySelectorAll('[name="c_a"]')[0];
                projectName.value = jsonData["project_name"];
                c_a.value = jsonData["c_a"];
                
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("job_assign js error")
            console.log("get error");
        }
    });



});
