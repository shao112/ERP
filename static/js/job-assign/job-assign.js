
var projectConfirmationIdControl = document.getElementById('project_confirmation_select2');

$('#project_confirmation_select2').on('select2:select', function (e) {
    console.log("selectd")
    LoadProjectConfirmation();
  });
  

projectConfirmationIdControl.addEventListener('change',LoadProjectConfirmation);

function LoadProjectConfirmation () {

    var selectedOptionIndex = projectConfirmationIdControl.selectedIndex;
    var selectedOption = projectConfirmationIdControl.options[selectedOptionIndex];
    var selectedId = selectedOption.value;

    
    console.log('選中的選項 id 為: ' + selectedId);
    if(selectedId ==-1){
        return;
    }

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
                var requisition = form.querySelectorAll('[name="requisition"]')[0];
                // var c_a = form.querySelectorAll('[name="c_a"]')[0];
                var client = form.querySelectorAll('[name="client"]')[0];
                projectName.value = jsonData["project_name"];
                // c_a.value = jsonData["c_a"];
                var attachment = jsonData["attachment"];
                console.log("url",attachment)
                var downloadLink = document.getElementById("super_attendance");
                
                if (attachment) {
                    downloadLink.textContent = "下載";
                    downloadLink.href = attachment; // 將下載連結設定為附件的URL
                } else {
                    downloadLink.textContent = "未提供";
                    downloadLink.href = "#"; // 將下載連結設定為錨點
                }
                requisition.value = jsonData["requisition_name"];
                client.value = jsonData["client_name"];

                
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("job_assign js error")
            console.log("get error");
        }
    });



}