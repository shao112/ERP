var quotation_select = document.getElementById("quotation_id");

quotation_select.addEventListener("change", function () {
  var selectedOptionIndex = quotation_select.selectedIndex;
  var selectedOption = quotation_select.options[selectedOptionIndex];
  if (selectedOption == undefined) {
    return;
  }

  var selectedId = selectedOption.value;
  console.log('選中的選項 id 為: ' + selectedId);

  const url = "/restful/quotation";
  // formData = { id: getdata["quotation"] };
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
      // console.log(jsonData["customer_name"])
      document.getElementsByName("project_name")[0].value =
        jsonData["project_name"];
      document.getElementById("client_id").value = jsonData["client_name"];
      document.getElementById("requisition_id").value = jsonData["requisition_name"];
    },
    error: function (xhr, textStatus, errorThrown) {
      alert("quotation  error");
      console.log("get error");
    },
  });
});


function set_select_id(id,selectname) {
  console.log("set_select_id")
  // console.log(id, selectname);
  var choose_input = document.getElementById(selectname);
  choose_input.value = id;
  $('#listid').modal('hide'); 
  const change_event = new Event("change");
  choose_input.dispatchEvent(change_event);
}
// );