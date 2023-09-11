function showSwal(title, text, icon, showCancelButton) {
  setting_dict = {
    title: title,
    html: text,
    icon: icon,
  };
  // console.log(showCancelButton)
  if (showCancelButton) {
    setting_dict.showCloseButton = true;
    setting_dict.showCancelButton = true;
    setting_dict.confirmButtonText = "確認";
    setting_dict.cancelButtonText = "取消";
  }
  console.log(setting_dict);
  return Swal.fire(setting_dict);
}

function get_all_input() {
  const allElements = document.querySelectorAll("input, select, textarea");
  return allElements;
}

function unlock_input() {
  const get_input = get_all_input();
  console.log(get_input);
  get_input.forEach((input) => {
    if (!input.classList.contains("readonly")) {
      input.removeAttribute("readonly");
      input.disabled = false;
    }
  });
}

function lock_input() {
  const get_input = get_all_input();

  get_input.forEach((input) => {
    input.setAttribute("readonly", "readonly");
    input.disabled = true;
  });
}

function cleanform() {
  $("[id*='_select2']").each(function () {
    var id = $(this).attr("id");
    if (id.endsWith("_select2")) {
      $("#" + id)
        .val(null)
        .trigger("change");
    }
  });

  var inputElements = document.querySelectorAll('form input[type="file"]');

  for (var i = 0; i < inputElements.length; i++) {
    var inputElement = inputElements[i];
    var name = inputElement.name;
    var linkElement = document.getElementById(name);
    if (linkElement) {
      linkElement.href = "#";
      linkElement.target = "_self";
      linkElement.textContent = "未上傳資料";
    }
  }

  $("#form")[0].reset();
  $("#form").attr("data-method", "POST");
}

// 新增表單時使用post
$("#sys_new").on("click", function () {
  cleanform();
});

//  獲取資料並帶入

document.querySelectorAll(".sys_get").forEach((element) => {
  // console.log("ee")
  element.addEventListener("click", GET_handleClick.bind(element));
});

/**
 * 說明
 * @param {event} param1 - 點擊的btn event
 * @param {bringdata} param2 - true由該事件帶入表單，false 不由GET_handleClick處理(目前沒使用到，但保留彈性)
 * @returns {type} 會回傳取得的data
 */
async function GET_handleClick(event, bringdata = true) {
  cleanform();

  try {
    var clickedElement = event.target.closest("[data-id]");
    var url = "/restful/" + clickedElement.getAttribute("data-url");
    var id = clickedElement.getAttribute("data-id");
  } catch (error) {
    // console.error("An error occurred:", error);
    var modalType = event.getAttribute("data-modal");
    var id = event.getAttribute("data-id");
    var url = "/restful/" + event.getAttribute("data-url");
  }

  $("#form").attr("data-method", "put");
  $("#form").attr("data-id", id);
  // console.log(`URL: ${url}, ID: ${id}`);

  formData = { id: id };
  return new Promise((resolve, reject) => {
    $.ajax({
      type: "GET",
      url: url,
      headers: {
        "X-CSRFToken": csrftoken,
      },
      data: formData,
      success: function (response) {
        jsonData = response.data;
        delete jsonData.created_date;
        delete jsonData.update_date;
        delete jsonData.modified_by;
        delete jsonData.author;

        resolve(jsonData);
        if (bringdata == false) {
          return; //設定回傳資料
        }

        for (var key in jsonData) {
          var input = document.getElementsByName(key)[0];
          if (input) {
            let get_value = jsonData[key];
            if (input.type == "file" && get_value != null) {
              console.log(get_value);
              var element = document.getElementById(key);
              element.href = get_value;
              element.target = "_blank";
              element.textContent = "下載";

              continue;
            }

            if (typeof jsonData[key] == "object" && get_value != null) {
              //判斷是不是陣列
              SetSelect2(input, key, get_value);
              continue;
            }

            input.value = get_value;
            // console.log("key " + key + " 帶資料:" + get_value);
          } else {
            // console.log("Input not found for key:", key);
          }
        }
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
  });
}

$("form").on("submit", function (event) {
  console.log("新增 or 修改");
  event.preventDefault();

  var form = $(this);
  var url = form.attr("action");
  var formData = form.serialize();
  var method = form.data("method");

  console.log("form data");
  console.log(formData);
  console.log(method);

  var idValue = form.find('input[name="id"]').val();

  $.ajax({
    type: method,
    url: url,
    data: formData,
    async: false,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      jsonData = response.data;

      if (method == "POST") {
        idValue = response.id;
      }

      showSwal("操作說明", jsonData, "success", false).then(() => {
        // location.reload();
      });
    },
    error: function (xhr, textStatus, errorThrown) {
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

        showSwal("操作失敗", errorMessageHTML, "error", false);
      } else {
        alert("系統發生錯誤");
        console.log(errorThrown);
      }
    },
  });

  form.find(":input").each(function () {
    var inputElement = $(this);
    var inputType = inputElement.attr("type");
    var inputName = inputElement.attr("name");
    // inputType === "file"，inputName === "attachment"
    if (inputType === "file" && inputElement[0] != undefined) {
      var fileInput = inputElement[0];
      var file = fileInput.files[0];
      if (!file) {
        return;
      }

      console.log(fileInput);
      var modal = inputElement.data("modal");
      console.log("idValue: " + idValue);
      var formData = new FormData();
      formData.append(inputName, file);
      formData.append("name", inputName);
      formData.append("id", idValue);
      formData.append("modal", modal);
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
        },
        error: function (xhr, status, error) {
          console.log("上傳失敗", error);
        },
      });
    }
  });
});

// 刪除

document.querySelectorAll(".sys_del").forEach((element) => {
  element.addEventListener("click", DELETE_handleClick.bind(element));
});

async function DELETE_handleClick(event) {
  const result = await showSwal(
    "確認刪除",
    "你確定要刪除該項目嗎？",
    "warning",
    true
  );

  if (!result.isConfirmed) {
    return;
  }

  const clickedElement = event.target.closest("[data-id]"); // 有時候會失敗抓不到data-id，懷疑是冒泡事件
  // const clickedElement = event.target; // 誰觸發這個 event -> 刪除 btn
  const url = "/restful/" + clickedElement.getAttribute("data-url");
  const id = clickedElement.getAttribute("data-id");
  const approvalStatus = clickedElement.getAttribute("data-approval");

  // console.log(`URL: ${url}, ID: ${id}`);
  // console.log(`URL:${approvalStatus}`);

  if (approvalStatus == "in_progress" || approvalStatus == "completed") {
    return showSwal(
      "刪除異常",
      "此單正在簽核中或是已完成，請先收回。如果已完成請通知主管處理。",
      "error",
      false
    );
  }

  formData = { id: id };

  $.ajax({
    type: "DELETE",
    url: url,
    headers: {
      "X-CSRFToken": csrftoken, // 在請求標頭中包含 CSRF token
    },
    data: formData,
    success: function (response) {
      showSwal("操作說明", "成功刪除", "success", false);
    },
    error: function (xhr, textStatus, errorThrown) {
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        showSwal("操作失敗", errorMessage, "error", false);
      } else {
        alert("系統發生錯誤" + xhr.responseJSON.error);
        console.log(errorThrown);
      }
    },
  });
}
