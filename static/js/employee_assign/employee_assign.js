var set_project_employee_assign_form = document.querySelector(
  'form[name="project_employee_assign"]'
);

var project_job_assign_IdControl = document.getElementById(
  "project_job_assign_id"
);

project_job_assign_IdControl.addEventListener("change", function () {
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
      console.log(jsonData);
      project_confirmation = jsonData["project_confirmation"];
      quotation_dict = jsonData["quotation_dict"];

      var q_id = set_project_employee_assign_form.querySelectorAll(
        '[id="quotation_id"]'
      )[0];
      console.log(set_project_employee_assign_form);
      console.log(q_id);
      q_id.value = quotation_dict["q_id"];

      document.getElementById("project_name").value =
        quotation_dict["project_name"];
      document.getElementById("client").value = quotation_dict["client_name"];
      document.getElementById("requisition").value =
        project_confirmation["requisition"];
    },
    error: function (xhr, textStatus, errorThrown) {
      alert("job_assign js error");
      console.log("get error");
    },
  });
});
