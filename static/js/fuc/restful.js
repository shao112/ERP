// 共用事件
function getcsrftoken() {
    var name = "csrftoken";
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// 新增表單時使用post
$("#sys_new").on("click", function () {
    $("#form")[0].reset();
    $("#form").attr("data-method", "POST");
});

//  獲取資料並帶入

function GET_handleClick(get_id,get_url){
    const url = "/restful/" + get_url;
    const id = get_id;

    formData = { id: id, };

    $.ajax({
        type: "GET",
        url: url,
        headers: {
            'X-CSRFToken': getcsrftoken()  // 在請求標頭中包含 CSRF token
        },
        data: formData,
        success: function (response) {
            console.log(response.data);
            jsonData=response.data
            if (response.status == 200) {
                // alert("成功");
                console.log(response);
                for (var key in jsonData) {
                    if (jsonData.hasOwnProperty(key)) {
                      var input = document.getElementsByName(key)[0];
                      if (input) {
                        input.value = jsonData[key];
                      } else {
                        console.log("Input not found for key:", key);
                      }
                    }
                  }

                //   更改form method
                $("#form").attr("data-method", "put");
                $("#form").attr("data-id", id);

                
            } else {
                $("#error-message").text(response.error); // 在错误消息显示区域显示错误消息
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("get error");
        }
    });

}


// 新增 or 修改(帶pk?)

$("form").on("submit", function (event) {
    event.preventDefault(); // 阻止表单的默认提交行为

    var form = $(this);
    var url = form.attr("action");
    var formData = form.serialize();
    console.log(formData)

    var method = form.data("method");


    $.ajax({
        type: method,
        url: url,
        data: formData,
        headers: {
            'X-CSRFToken': getcsrftoken()  // 在請求標頭中包含 CSRF token
        },
        success: function (response) {
            if (response.status == 200) {
                alert("操作成功");
                location.reload();
            } else {
                $("#error-message").text(response.error); // 在错误消息显示区域显示错误消息
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            var errorMessage = form.get_error_messages(); // 获取后端返回的错误消息
            $("#error-message").text(errorMessage); // 在错误消息显示区域显示错误消息
        }
    });
    
});

// 刪除

function DELETE_handleClick(get_id,get_url){
    const url = "/restful/" + get_url;
    const id = get_id;

    console.log(`URL: ${url}, ID: ${id}`);

    formData = { id: id, };

    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            'X-CSRFToken': getcsrftoken()  // 在請求標頭中包含 CSRF token
        },
        data: formData,
        success: function (response) {
            if (response.status == 200) {
                alert("成功刪除");
                location.reload();
            } else {
                $("#error-message").text(response.error); // 在错误消息显示区域显示错误消息
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            // var errorMessage = form.get_error_messages(); // 获取后端返回的错误消息
            $("#error-message").text("系統發生錯誤"); // 在错误消息显示区域显示错误消息
        }
    });



}