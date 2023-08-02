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




function showSwal(title, text, icon, showCancelButton) {
    setting_dict = {
        title: title,
        html: text,
        icon: icon,
    }
    console.log(showCancelButton)
    if (showCancelButton) {
        setting_dict.showCloseButton = true;
        setting_dict.showCancelButton = true;
        setting_dict.confirmButtonText = "確認";
        setting_dict.cancelButtonText = "取消";
    }
    console.log(setting_dict)
    return Swal.fire(setting_dict);
}


function cleanform() {
    $("[id*='_select2']").each(function () {
        var id = $(this).attr("id");
        if (id.endsWith("_select2")) {
            $('#' + id).val(null).trigger('change');
        }
    });
    $("#form")[0].reset();
    $("#form").attr("data-method", "POST");
}

// 新增表單時使用post
$("#sys_new").on("click", function () {
    cleanform()
});



//  獲取資料並帶入

document.querySelectorAll('.sys_get').forEach(element => {
    // console.log("ee")
    element.addEventListener('click', GET_handleClick.bind(element));
});

function GET_handleClick(event) {
    cleanform()
    const clickedElement = event.target.closest('[data-id]');
    const url = "/restful/" + clickedElement.getAttribute('data-url');
    const id = clickedElement.getAttribute('data-id');

    console.log(`URL: ${url}, ID: ${id}`);

    formData = { id: id, };

    $.ajax({
        type: "GET",
        url: url,
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: formData,
        success: function (response) {

            jsonData = response.data
            for (var key in jsonData) {
                var input = document.getElementsByName(key)[0];
                if (input) {
                    let get_value = jsonData[key];

                    if (key == "attendance_date") {
                        if (jsonData[key] == null) {
                            continue;
                        }
                        for (var i = 0; i < get_value.length; i++) {
                            var dateStr = get_value[i];
                            var option = new Option(dateStr, dateStr, true, true);
                            input.appendChild(option);
                        }
                        $('#attendance_date_select2').select2();
                        continue;
                    }


                    if (typeof (jsonData[key]) == "object" && get_value != null) {
                        // 如果是陣列，先取得對應的options，以及select2的欄位
                        const options = input.options;
                        selectname = `#${key}_select2`
                        console.log("GET_" + key + "=> " + selectname);
                        console.log(get_value)
                        get_value = Object.values(get_value);
                        console.log(get_value)
                        for (let i = 0; i < options.length; i++) {
                            const option = options[i];
                            const option_id = option.value;

                            var containsValue = false;
                            // = get_value.find(item => item == option_id);
                            console.log(typeof (get_value[0]))
                            if (typeof (get_value[0]) == "object") {

                                containsValue = get_value.find(item => item.id == option_id);
                            } else {
                                containsValue = get_value.find(item => item == option_id);
                            }
                            console.log(get_value)
                            console.log(option_id)
                            console.log(containsValue)
                            if (containsValue) {
                                option.selected = true;
                            }
                        }
                        $(selectname).trigger('change');
                    } else {
                        input.value = jsonData[key];
                        // console.log("帶資料:" + input.value);
                    }

                    if (key == "editor_content") { //觸發change事件
                        editor.setData(jsonData[key]);
                    }

                    const select2_change_key = ["project_confirmation", "project_job_assign", "vehicle"];


                    if (select2_change_key.includes(key)) { //觸發change事件
                        const event = new Event("change");
                        input.dispatchEvent(event);
                    }

                } else {
                    console.log("Input not found for key:", key);
                }
            }

            $("#form").attr("data-method", "put");
            $("#form").attr("data-id", id);



        },
        error: function (xhr, textStatus, errorThrown) {
            if (xhr.status === 400) {
                var errorMessage = xhr.responseJSON.error;
                console.log(errorMessage)
                showSwal('操作失敗', errorMessage, 'error', false)
            } else {
                alert("系統發生錯誤");
                console.log(errorThrown)
            }
        }
    });

}

$("form").on("submit", function (event) {
    console.log("新增 or 修改")
    event.preventDefault();

    var form = $(this);
    var url = form.attr("action");
    var formData = form.serialize();
    console.log("add form");


    form.find(":input").each(function () {
        var inputElement = $(this);
        var inputType = inputElement.attr("type");
        var inputName = inputElement.attr("name");
        if (inputType === "file") {
            var fileInput = inputElement[0];
            var modal = inputElement.data("modal");
            var idValue = form.find('input[name="id"]').val()
            var formData = new FormData();
            formData.append("uploaded_file", fileInput.files[0]);
            formData.append("name", inputName);
            formData.append("modal", modal);
            formData.append("id", idValue);
            for (var pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }
            $.ajax({
                type: "POST",
                url: "/restful/formuploadfile",
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': getcsrftoken()
                },
                success: function(response){
                    console.log("上傳成功",response)
                },
                error: function(xhr, status, error){
                    console.log("上傳失敗",error)
                }
            })
        }
    });

    var method = form.data("method");


    $.ajax({
        type: method,
        url: url,
        data: formData,
        headers: {
            'X-CSRFToken': getcsrftoken()
        },
        success: function (response) {
            jsonData = response.data

            showSwal('操作說明', jsonData, 'success', false).then(() => {
                // location.reload();
            })
        },
        error: function (xhr, textStatus, errorThrown) {
            if (xhr.status === 400) {
                var errorMessage = xhr.responseJSON.error;
                console.log(errorMessage)
                var errorMessageHTML = "<ul>";
                Object.entries(errorMessage).map(([key, errors]) => {
                    errors.forEach(error => {
                        errorMessageHTML += "<li>" + error + "</li>";
                    });
                });
                errorMessageHTML += "</ul>";
                console.log(errorMessageHTML)


                showSwal('操作失敗', errorMessageHTML, 'error', false)
            } else {
                alert("系統發生錯誤");
                console.log(errorThrown)
            }
        }
    });

});

// 刪除

document.querySelectorAll('.sys_del').forEach(element => {
    element.addEventListener('click', DELETE_handleClick.bind(element));
});



async function DELETE_handleClick(event) {
    const result = await showSwal('確認刪除', '你確定要刪除該項目嗎？', 'warning', true);

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
            'X-CSRFToken': csrftoken  // 在請求標頭中包含 CSRF token
        },
        data: formData,
        success: function (response) {
            showSwal('操作說明', "成功刪除", 'success', false)
            location.reload();
        },
        error: function (xhr, textStatus, errorThrown) {
            if (xhr.status === 400) {
                var errorMessage = xhr.responseJSON.error;
                showSwal('操作失敗', errorMessage, 'error', false)
            } else {
                alert("系統發生錯誤" + xhr.responseJSON.error);
                console.log(errorThrown)
            }
        }
    });



}