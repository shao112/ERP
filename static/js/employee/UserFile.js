document.getElementById("fileUploadBtn").onclick = handleAPI;

let employee_id = "";

function setEmployeeId(id) {
    employee_id=id;
    console.log(employee_id)
}


function handleAPI() {


    const fileNameInput = document.getElementById('fileNameInput');
    const fileNameValue = fileNameInput.value;

    const fileInput = document.getElementById('fileInput');
    var inputName = "uploaded_files";

    var file = fileInput.files[0];

    if (!file) {
        return
    }

    var modal = "employee";
    var formData = new FormData();
    formData.append(inputName, file);
    formData.append("name", inputName);
    formData.append("id", employee_id);
    formData.append("ManyToManyProcess", true);
    formData.append("modal", modal);
    formData.append("file_name", fileNameValue);
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
            'X-CSRFToken': csrftoken
        },
        success: function (response) {
            console.log("上傳成功", response)
        },
        error: function (xhr, status, error) {
            console.log("上傳失敗", error)
        }
    })

}