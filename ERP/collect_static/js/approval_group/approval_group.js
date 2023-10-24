function createApprovalStageElement(jsonData) {
  var stageDiv = document.getElementById("approval_stage");
  while (stageDiv.hasChildNodes()) {
    stageDiv.removeChild(stageDiv.firstChild);
  }

  var stageArray = jsonData; // User物件的id
  console.log(stageArray);
  for (let i = 0; i < stageArray.length; i++) {
    var newDiv = document.createElement("div");
    newDiv.className =
      "form-group form-row d-flex justify-content-between align-items-center";

    var label = document.createElement("label");
    label.setAttribute("for", "stage-" + i);
    label.textContent = "第 " + (i + 1) + " 關";

    var span = document.createElement("span");
    span.textContent = stageArray[i].name;
    var employee_id = stageArray[i].id;

    var a = document.createElement("a");
    a.setAttribute("type", "button");
    a.className = "sys_del btn btn-sm btn-danger";
    var icon = document.createElement("i");
    icon.className = "far fa-sm fa-trash-alt";
    a.appendChild(icon);
    a.addEventListener("click", function () {
      $.ajax({
        type: "DELETE",
        url: "/restful/approval_group",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        data: {
          set_id: set_id,
          employee_id: employee_id,
        },
        success: function (response) {
          alert("刪除成功!");
          sendApprovalGroup(set_id);
        },
        error: function (xhr, textStatus, errorThrown) {
          alert("刪除失敗!");
          if (xhr.status === 400) {
            var errorMessage = xhr.responseJSON.error;
            showSwal("操作失敗", errorMessage, "error", false);
          } else if (xhr.status === 403) {
            alert("無權操作，請聯絡管理員");
          } else {
            alert("系統發生錯誤" + xhr.responseJSON.error);
            console.log(errorThrown);
          }
        },
      });
    });
    newDiv.appendChild(label);
    newDiv.appendChild(span);
    newDiv.appendChild(a);
    stageDiv.appendChild(newDiv);
  }
}

let read = true;
var set_id = "";
function sendApprovalGroup(id) {
  set_id = id;
  if (read) {
    Swal.fire({
      title: "嚴重告知",
      html: "只要更改資料：勾選或取消直屬簽核、刪除、新增員工都會讓該簽核<b>進行中、駁回</b>的項目取消。<br>但不會影響已經完成的簽核項目",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "確定",
      cancelButtonText: "取消",
    }).then((result) => {
      if (result.isConfirmed) {
        read = false;
        $("#approval_group-modal").modal("show");
      } else {
      }
    });
  } else {
    $("#approval_group-modal").modal("show");
  }

  $.ajax({
    type: "GET",
    url: "/restful/approval_group",
    data: {
      id: id,
    },
    success: function (response) {
      jsonData = response.data;
      for (var key in jsonData) {
        console.log("key " + key);
        if (key == "name") {
          var h5 = document.getElementById(key);
          if (h5) {
            h5.textContent = jsonData[key];
          }
        }
        if (key == "approval_order") {
          createApprovalStageElement(jsonData[key]);
        }
        if (key == "is_director") {
          var is_director = document.getElementById(key);
          if (jsonData[key]) {
            console.log("is_director.checked = true;");
            is_director.checked = true;
          } else {
            console.log("is_director.checked = false;");
            is_director.checked = false;
          }
        }
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        showSwal("操作失敗", errorMessage, "error", false);
      } else if (xhr.status === 403) {
        alert("無權操作，請聯絡管理員");
      } else {
        alert("系統發生錯誤" + xhr.responseJSON.error);
        console.log(errorThrown);
      }
    },
  });
}
document.getElementById("submitEmployeeBtn").onclick = submitEmployee;

function submitEmployee() {
  const new_stage_select = document.getElementById("new_stage");
  const new_stage_id = new_stage_select.value;
  $.ajax({
    type: "POST",
    url: "/restful/approval_group",
    data: {
      new_stage_id: new_stage_id,
      set_id: set_id,
    },
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      console.log(response);
      sendApprovalGroup(set_id);
    },
    error: function (xhr, textStatus, errorThrown) {
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        showSwal("操作失敗", errorMessage, "error", false);
      } else if (xhr.status === 403) {
        alert("無權操作，請聯絡管理員");
      } else {
        alert("系統發生錯誤" + xhr.responseJSON.error);
        console.log(errorThrown);
      }
      // 員工已被選過錯誤處理
    },
  });
}

/* --- 監聽是否勾選直屬主管，發送post請求 --- */
var is_director_checkbox = document.getElementById("is_director");
is_director_checkbox.addEventListener("change", function () {
  $.ajax({
    type: "POST",
    url: "/restful/approval_group",
    data: {
      set_id: set_id,
      is_checked: is_director_checkbox.checked,
    },
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {},
    error: function (xhr, textStatus, errorThrown) {
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        showSwal("操作失敗", errorMessage, "error", false);
      } else if (xhr.status === 403) {
        alert("無權操作，請聯絡管理員");
      } else {
        alert("系統發生錯誤" + xhr.responseJSON.error);
        console.log(errorThrown);
      }
    },
  });
});
