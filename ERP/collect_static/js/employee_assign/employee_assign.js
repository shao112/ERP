var set_project_employee_assign_form = document.querySelector(
  'form[name="project_employee_assign"]'
);

var project_job_assign_IdControl = document.getElementById(
  "project_job_assign_id"
);
$('#project_job_assign_id').on('select2:select', function (e) {
  console.log("selectd")
  Load_Job_Assign();

});

project_job_assign_IdControl.addEventListener("change", Load_Job_Assign);

function Load_Job_Assign() {
  var selectedOptionIndex = project_job_assign_IdControl.selectedIndex;
  var selectedOption =
    project_job_assign_IdControl.options[selectedOptionIndex];
  var selectedId = selectedOption.value;

  console.log("選中的選項 id 為: " + selectedId);
  if (selectedId == -1) {
    return;
  }

  const url = "/restful/job_assign";
  formData = { id: selectedId };

  $.ajax({
    type: "GET",
    url: url,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formData,
    success: function (response) {
      jsonData = response.data;
      console.log(jsonData)
      var msgDiv = document.getElementById('employee_assign_show_msg');

      // 從jsonData中獲取相關資料
      var vehicles = jsonData["vehicle"];
      console.log("vehicles: "+vehicles)
      var leadEmployees = jsonData["lead_employee"];
      var workEmployees = jsonData["work_employee"];
      var leadEmployeeNames = leadEmployees.map(function(employee) {
        return employee.full_name;
      }).join(", ");
      
      var workEmployeeNames = workEmployees.map(function(employee) {
          return employee.full_name;
      }).join(", ");
      var htmlContent = `         
          帶班主管: ${leadEmployeeNames}
          <br/>
          檢測人員: ${workEmployeeNames}
      `;

      msgDiv.innerHTML = htmlContent;


      var project_confirmation = jsonData["project_confirmation"];
      var quotation_dict = jsonData["quotation_dict"];

      var q_id = set_project_employee_assign_form.querySelectorAll(
        '[id="quotation_id"]'
      )[0];
      q_id.value = quotation_dict["q_id"];     
      document.getElementsByName("project_name")[0].value =
        quotation_dict["project_name"];
      document.getElementsByName("client_name")[0].value =
        quotation_dict["client_name"];
      document.getElementsByName("requisition")[0].value =
        jsonData["requisition_name"];
      document.getElementsByName("location")[0].value = jsonData["location"];
      document.getElementsByName("vehicle")[0].value = jsonData["vehicle"];


      var vehicle_select2_DOM = document.getElementById("vehicle_select2");
      SetSelect2(vehicle_select2_DOM,"vehicle",vehicles);
      

    },
    error: function (xhr, textStatus, errorThrown) {
      alert("job_assign js error");
      console.log("get error");
    },
  });
}
