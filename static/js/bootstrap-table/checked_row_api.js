let checked = [];

function checkpage() {
  const checkboxes = document.getElementsByName("importcheckd");

  for (let i = 0; i < checkboxes.length; i++) {
    const checkboxValue = checkboxes[i].value;
    const index = checked.indexOf(checkboxValue);
    if (index === -1) {
      checked.push(checkboxValue);
    } else if (index !== -1) {
      checked.splice(index, 1);
    }
  }

  console.log(checked);
  syncCheckedRowsWithArray();
}

function updateCheckedArray(checkbox) {
  const value = checkbox.value;
  const index = checked.indexOf(value);

  if (checkbox.checked && index === -1) {
    checked.push(value);
  } else if (!checkbox.checked && index !== -1) {
    checked.splice(index, 1);
  }
  console.log(checked);
}
function syncCheckedRowsWithArray() {
  console.log(checked);
  const checkboxes = document.getElementsByName("importcheckd");
  for (let i = 0; i < checkboxes.length; i++) {
    const checkbox = checkboxes[i];
    checkbox.checked = checked.includes(checkbox.value);
  }
}

function getSelectedValues() {
  return checked;
}

$("#table").on("page-change.bs.table", function (e, number, size) {
  Promise.resolve().then(function () {
    syncCheckedRowsWithArray();
  });
});

//複製api

function Cloneapi(modelname) {
  const selectedValues = getSelectedValues();
  $.ajax({
    url: "/restful/ClonePost",
    type: "POST",
    contentType: "application/json",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: JSON.stringify({
      selectedValues: selectedValues,
      modelname: modelname,
    }),
    success: function (data) {
      console.log(data);
      Swal.fire("操作成功", "完成").then(() => {
        location.reload();
      });
    },
    error: function (error) {
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        console.log(errorMessage);

        var errorMessageHTML = "<ul>";

        if (typeof errorMessage == "string") {
          errorMessageHTML += "<li>" + errorMessage + "</li>";
        } else {
          Object.entries(errorMessage).map(([key, errors]) => {
            errors.forEach((error) => {
              errorMessageHTML += "<li>" + error + "</li>";
            });
          });
        }

        errorMessageHTML += "</ul>";
        console.log(errorMessageHTML);

        Swal.fire({
          title: "操作失敗",
          html: errorMessageHTML,
          icon: "error",
          confirmButtonText: "確定",
        });
      } else if (xhr.status === 403) {
        alert("無權獲得該頁詳細或操作，請聯絡管理員");
      } else {
        alert("系統發生錯誤");
        console.log(errorThrown);
      }
    },
  });
}

//簽核一鍵通過

function ApprovalPass() {
  const selectedValues = getSelectedValues();

  const formHtml = `
  <form>
      <label for="approvalStatus">選擇通過或不通過：</label>
      <select id="approvalStatusAPI" name="approvalStatus">
          <option value="approved">通過</option>
          <option value="rejected">不通過</option>
      </select>
      <br>
      <label for="feedback">填寫意見：</label>
      <input type="text" id="feedbackApi" name="feedback" placeholder="輸入反饋意見...">
  </form>
`;

  Swal.fire({
    title: "一鍵處理",
    icon: "question",
    html: formHtml,
    showCancelButton: true,
    confirmButtonText: "確定",
    cancelButtonText: "取消",
    preConfirm: () => {
      const status = document.getElementById("approvalStatusAPI").value;
      const feedback = document.getElementById("feedbackApi").value;
      console.log(status, feedback);
      return $.ajax({
        url: "/restful/Approval_Process_Pass",
        type: "POST",
        contentType: "application/json",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        data: JSON.stringify({
          selectedValues: selectedValues,
          status: status,
          feedback: feedback,
        }),
        success: function (data) {
          console.log(data);
          Swal.fire("操作成功", "完成").then(() => {
            location.reload();
          });
        },
        error: function (error) {
          if (xhr.status === 400) {
            var errorMessage = xhr.responseJSON.error;
            console.log(errorMessage);

            var errorMessageHTML = "<ul>";

            if (typeof errorMessage == "string") {
              errorMessageHTML += "<li>" + errorMessage + "</li>";
            } else {
              Object.entries(errorMessage).map(([key, errors]) => {
                errors.forEach((error) => {
                  errorMessageHTML += "<li>" + error + "</li>";
                });
              });
            }

            errorMessageHTML += "</ul>";
            console.log(errorMessageHTML);

            Swal.fire({
              title: "操作失敗",
              html: errorMessageHTML,
              icon: "error",
              confirmButtonText: "確定",
            });
          } else if (xhr.status === 403) {
            alert("無權獲得該頁詳細或操作，請聯絡管理員");
          } else {
            alert("系統發生錯誤");
            console.log(errorThrown);
          }
        },
      });
    },
  });
}
