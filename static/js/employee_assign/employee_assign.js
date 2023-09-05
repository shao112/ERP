

var project_job_assign_IdControl = document.getElementById('project_job_assign_id');

project_job_assign_IdControl.addEventListener('change', function () {

    var selectedOptionIndex = project_job_assign_IdControl.selectedIndex;
    var selectedOption = project_job_assign_IdControl.options[selectedOptionIndex];
    var selectedId = selectedOption.value;

    console.log('選中的選項 id 為: ' + selectedId);
    if(selectedId ==-1){
        return;
    }

    const url = "/restful/job_assign";
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
            console.table(jsonData)
            project_confirmation = jsonData["project_confirmation"]
            quotation_dict = jsonData["quotation_dict"]
            document.getElementById("project_name").value = quotation_dict["project_name"];
            document.getElementById("quotation_id").value = quotation_dict["q_id"];
            document.getElementById("client").value = jsonData["client"];
            document.getElementById("requisition").value = jsonData["requisition"];


        },
        error: function (xhr, textStatus, errorThrown) {
            alert("job_assign js error")
            console.log("get error");
        }
    });



});
