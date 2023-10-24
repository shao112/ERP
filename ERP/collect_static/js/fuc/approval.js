function submitApproval(event) {
  event.preventDefault();

  const submitApprovalButton = event.target;
  // 物件id
  const id = submitApprovalButton.getAttribute("data-id");
  const model = submitApprovalButton.getAttribute("data-model");

  const data = {
    id: id,
    model: model,
  };
  console.log(data);

  $.ajax({
    type: "post",
    url: "/restful/approval_view_process",
    data: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    cache: false,
    success: function (response) {
      alert("操作成功");

      location.reload();
    },
    error: function (error) {
      var errorMessage = error.responseJSON.error;
      alert(errorMessage);
      console.log("Error fetching events:", errorMessage);
    },
  });
}

function DelApproval(event) {
  event.preventDefault();

  const submitApprovalButton = event.target;
  // 物件id
  const id = submitApprovalButton.getAttribute("data-id");
  const model = submitApprovalButton.getAttribute("data-model");

  const data = {
    id: id,
    model: model,
  };
  console.log(data);

  $.ajax({
    type: "delete",
    url: "/restful/approval_view_process",
    data: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    cache: false,
    success: function (response) {
      alert("操作成功");
      location.reload();
    },
    error: function (error) {
      //   alert("簽核失敗");
      console.log(error);
      var errorMessage = error.responseJSON.error;
      console.log("Error fetching events:", errorMessage);
    },
  });
}
