// init canvas element
var canvas = document.getElementById('mycanvas')
var ctx = canvas.getContext("2d")
var settingid =""
const fileListElement = $("#fileList");


function setSettingId(id) {
  settingid = id; // 設定 settingid 變數的值
  console.log("Setting Id:", settingid);
  LoadFileList();
}

function LoadFileList() {
  $.ajax({
    type: "GET",
    url: "/restful/project_employee_assign",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: { id: settingid },
    success: function (response) {
      fileListElement.empty();
      jsonData = response.data.uploaded_files;
      jsonData.forEach((file) => {
        const listItem = $("<li></li>");
        listItem.addClass(
          "list-group-item d-flex justify-content-between align-items-center"
        );

        const fileLink = $("<a></a>");
        fileLink.attr("href", file.file);
        fileLink.attr("target", "_blank");
        fileLink.text(file.name || "未命名");

        const deleteButton = $("<button></button>");
        deleteButton.addClass("btn btn-danger btn-sm");
        deleteButton.text("刪除");
        deleteButton.click(function () {
          $.ajax({
            type: "DELETE",
            url: `/restful/delete_uploaded_file/project_employee_assign/${settingid}/${file.id}`,
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


let width = canvas.width;
let height = canvas.height;

if (window.devicePixelRatio) {
  canvas.style.width = width + "px";
  canvas.style.height = height + "px";
  canvas.height = height * window.devicePixelRatio;
  canvas.width = width * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
}


// mouse
function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

function mouseMove(evt) {
  var mousePos = getMousePos(canvas, evt);
  ctx.lineCap = "round";
  ctx.lineWidth = 2;
  ctx.lineJoin = "round";
  ctx.shadowBlur = 1; // 邊緣模糊，防止直線邊緣出現鋸齒 
  ctx.shadowColor = 'black';// 邊緣顏色
  ctx.lineTo(mousePos.x, mousePos.y);
  ctx.stroke();
}

canvas.addEventListener('mousedown', function (evt) {
  var mousePos = getMousePos(canvas, evt);
  ctx.beginPath();
  ctx.moveTo(mousePos.x, mousePos.y);
  evt.preventDefault();
  canvas.addEventListener('mousemove', mouseMove, false);
});

canvas.addEventListener('mouseup', function () {
  canvas.removeEventListener('mousemove', mouseMove, false);
}, false);


// touch
function getTouchPos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.touches[0].clientX - rect.left,
    y: evt.touches[0].clientY - rect.top
  };
}

function touchMove(evt) {
  // console.log("touchmove")
  var touchPos = getTouchPos(canvas, evt);
  // console.log(touchPos.x, touchPos.y)

  ctx.lineWidth = 2;
  ctx.lineCap = "round"; // 繪制圓形的結束線帽
  ctx.lineJoin = "round"; // 兩條線條交匯時，建立圓形邊角
  ctx.shadowBlur = 1; // 邊緣模糊，防止直線邊緣出現鋸齒 
  ctx.shadowColor = 'black'; // 邊緣顏色
  ctx.lineTo(touchPos.x, touchPos.y);
  ctx.stroke();
}

canvas.addEventListener('touchstart', function (evt) {
  // console.log('touchstart')
  // console.log(evt)
  var touchPos = getTouchPos(canvas, evt);
  ctx.beginPath(touchPos.x, touchPos.y);
  ctx.moveTo(touchPos.x, touchPos.y);
  evt.preventDefault();
  canvas.addEventListener('touchmove', touchMove, false);
});

canvas.addEventListener('touchend', function () {
  canvas.removeEventListener('touchmove', touchMove, false);
}, false);


// clear
document.getElementById('clear').addEventListener('click', function () {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}, false);


// convertToImage
document.getElementById('convertToImage').addEventListener('click', function () {


  console.log("convertToImage")
  var image = canvas.toDataURL("image/png");
  // console.log(image)


  var selectElement = document.getElementById('name_select_id'); 
  var selectedValue = selectElement.value;
  console.log(selectedValue)

  var formData = new FormData();
  formData.append("uploaded_files", image);
  formData.append("id", settingid);
  formData.append("ManyToManyProcess", true);
  formData.append("file_name", selectedValue);
  formData.append("name", "uploaded_files");
  formData.append("modal", "Project_Employee_Assign");
  console.log(formData)

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
      LoadFileList()
    },
    error: function (xhr, status, error) {
      console.log("上傳失敗", error);
      if (xhr.status === 400) {
        var errorMessage = xhr.responseJSON.error;
        showSwal("操作失敗", errorMessage, "error", false);
      } else if (xhr.status === 403) {
        alert("無權操作，請聯絡管理員");
      } else {
        alert("系統發生錯誤" + xhr.responseJSON.error);
        console.log(errorThrown);
      }
    }})
});

