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

function showSwal(title, text, icon) {
    return Swal.fire({
        title: title,
        text: text,
        icon: icon,
        showCancelButton: true,
        confirmButtonText: '確定',
        cancelButtonText: '取消',
    });
}



// 新增表單時使用post
$("#sys_new").on("click", function () {
    $("#form")[0].reset();
    $("#form").attr("data-method", "POST");

    //清除select2的資訊
    $("[id*='_select2']").each(function () {
        var id = $(this).attr("id");
        if (id.endsWith("_select2")) {
            $('#' + id).val(null).trigger('change');
        }
    });

});



//  獲取資料並帶入

document.querySelectorAll('.sys_get').forEach(element => {
    element.addEventListener('click', GET_handleClick.bind(element));
});

function GET_handleClick(event) {


    const clickedElement = event.target.closest('[data-id]');
    const url = "/restful/" + clickedElement.getAttribute('data-url');
    const id = clickedElement.getAttribute('data-id');

    console.log(`URL: ${url}, ID: ${id}`);

    formData = { id: id, };

    $.ajax({
        type: "GET",
        url: url,
        headers: {
            'X-CSRFToken': getcsrftoken()
        },
        data: formData,
        success: function (response) {

            if (response.status == 200) {
                jsonData = response.data
                for (var key in jsonData) {
                    var input = document.getElementsByName(key)[0];
                    if (input) {
                        let get_value = jsonData[key];

                        if (typeof (jsonData[key]) == "object" && get_value != null) {
                            // 如果是陣列，先取得對應的options，以及select2的欄位
                            console.log("GET_" + key)
                            const options = input.options;
                            selectname = `#${key}_select2`
                            for (let i = 0; i < options.length; i++) {
                                //取出單一optons的id，在get_value比對id是不是匹配
                                const option = options[i];
                                const id = option.value;
                                const matchedItem = get_value.find(item => item.id === Number(id));
                                if (matchedItem) {
                                    option.selected = true;
                                }
                            }
                            $(selectname).trigger('change');


                        } else {
                            input.value = jsonData[key];
                        }


                        if (key == "project_confirmation") { //觸發change事件
                            const event = new Event("change");
                            input.dispatchEvent(event);
                        }

                    } else {
                        console.log("Input not found for key:", key);
                    }
                }

                //   更改form method
                $("#form").attr("data-method", "put");
                $("#form").attr("data-id", id);


            } else {
                $("#error-message").text(response.error);
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("get error");
        }
    });

}

// 新增 or 修改(帶pk?)

$("form").on("submit", function (event) {
    console.log("新增 or 修改")
    event.preventDefault();


    var form = $(this);
    var url = form.attr("action");
    var formData = form.serialize();
    console.log(formData);

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
            } else {
                $("#error-message").text(response.error); // 在错误消息显示区域显示错误消息
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("系統發生錯誤");
            console.log(errorThrown)
        }
    });

});

// 刪除

document.querySelectorAll('.sys_del').forEach(element => {
    element.addEventListener('click', DELETE_handleClick.bind(element));
});



async function DELETE_handleClick(event) {
    const result = await showSwal('確認刪除', '你確定要刪除該項目嗎？', 'warning');

    if (!result.isConfirmed) {
        return;
    }

    const clickedElement = event.target.closest('[data-id]'); // 有時候會失敗抓不到data-id，懷疑是冒泡事件
    // const clickedElement = event.target; // 誰觸發這個 event -> 刪除 btn
    const url = "/restful/" + clickedElement.getAttribute('data-url');
    const id = clickedElement.getAttribute('data-id');

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
                alert(response.error);
                // $("#error-message").text(response.error); // 在错误消息显示区域显示错误消息
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            // var errorMessage = form.get_error_messages(); // 获取后端返回的错误消息
            alert("系統發生錯誤"); // 在错误消息显示区域显示错误消息
        }
    });



}