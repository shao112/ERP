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
    },
    error: function (xhr, textStatus, errorThrown) {
      alert("quotation  error");
      console.log("get error");
    },
  });
});
