// init canvas element
var canvas = document.getElementById('mycanvas')
var ctx = canvas.getContext("2d")
var settingid =""

function setSettingId(id) {
  settingid = id; // 設定 settingid 變數的值
  console.log("Setting Id:", settingid);
}


// 抗鋸齒
// ref: https://www.zhihu.com/question/37698502
let width = canvas.width,
  height = canvas.height;
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

  $('#image').html("<img src='" + image + "' alt='from canvas'/>");

  var form = $('#form');
  var formData = new FormData();
  console.log(image)
  formData.append("enterprise_signature", image);
  formData.append("id", settingid);
  console.log(formData)

  $.ajax({
    type: "POST",
    url: "/restful/project_employee_assign_update_signature",
    data: formData,
    processData: false,
    contentType: false,
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: function (response) {
      console.log("上傳成功", response)
    },
    error: function (xhr, status, error) {
      console.log("上傳失敗", error)
    }
  })
  // $('#image').html("<img src='" + image + "' alt='from canvas'/>");
}, false);
