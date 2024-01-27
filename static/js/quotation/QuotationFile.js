document.getElementById("fileUploadBtn").onclick= handleAPI;
let qu_id = "";
const fileListElement = $("#fileList");

function setQuotationId(id) {

  qu_id = id; 
  console.log("xxx")
  LoadFileList();
}


function LoadFileList() {
  $.ajax({
    type: "GET",
    url: "/restful/quotation",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: { id: qu_id },
    success: function (response) {
      fileListElement.empty();
      jsonData = response.data.uploaded_files;
      console.log("json");
      console.log(jsonData);
      jsonData.forEach((file) => {
        const listItem = $("<li></li>");
        listItem.addClass(
          "list-group-item d-flex justify-content-between align-items-center"
        );

        const fileName = file.file.split('/').pop();

        const fileLink = $("<a></a>");
        fileLink.attr("href", file.file);
        fileLink.attr("target", "_blank");
        fileLink.text(file.name|| fileName || "未命名");

        const deleteButton = $("<button></button>");
        deleteButton.addClass("btn btn-danger btn-sm");
        deleteButton.text("刪除");
        deleteButton.click(function () {
          $.ajax({
            type: "DELETE",
            url: `/restful/delete_uploaded_file/${"Quotation"}/${qu_id}/${file.id}`,
            headers: {
              "X-CSRFToken": csrftoken,
            },
            success: function (response) {
              alert("刪除成功!");
              LoadFileList();
            },
            error: function (error) {
              alert("刪除失敗!");
              console.log("Error:", error);
            },
          });
        });

        listItem.append(fileLink);
        listItem.append(deleteButton);
        fileListElement.append(listItem);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        console.log(errorMessage);
        showSwal("操作失敗", errorMessage, "error", false);
      } else {
        alert("系統發生錯誤");
        console.log(errorThrown);
      }
    },
  });
}



function handleAPI() {
  const fileNameInput = document.getElementById("fileNameInput");
  const fileNameValue = fileNameInput.value;

  const fileInput = document.getElementById("fileInput");

  var inputName = "uploaded_files";

  var file = fileInput.files[0];

  if (!file) {
    return;
  }

  var newFileName = "Quotation_" + file.name;

  file = new File([file], newFileName, { type: file.type });

  var modal = "Quotation";
  var formData = new FormData();
  formData.append(inputName, file);
  formData.append("name", inputName);
  formData.append("id", qu_id);
  formData.append("ManyToManyProcess", true);
  formData.append("modal", modal);
  formData.append("file_name", fileNameValue);
  for (var pair of formData.entries()) {
    console.log(pair[0] + ": " + pair[1]);
  }
  $.ajax({
    type: "POST",
    url: "/restful/formuploadfile",
    data: formData,
    processData: false,
    contentType: false,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      console.log("上傳成功", response);
      LoadFileList();
    },
    error: function (xhr, status, error) {
      console.log("上傳失敗", error);
    },
  });
}
