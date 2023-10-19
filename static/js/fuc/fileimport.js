function showSwal(title, text, icon) {
    return Swal.fire({
        title: title,
        html: text,
        icon: icon,
        showCancelButton: true,
        confirmButtonText: '確定',
    });
}



//匯入處理
var fileInput = document.getElementById('fileInput_file');
function importfile() {

    fileInput.click();

}

fileInput.addEventListener('change', async function () {
    // const result = await showSwal('確認上傳', '你確定要上傳嗎？', 'warning');

    // if (!result.isConfirmed) {
    //     return;
    // }

    const formData = new FormData(); // Create a new FormData object
    formData.append('fileInput', fileInput.files[0]); // Add the selected file to the FormData
    console.log(formData); // Handle the success response from Django
    model = fileInput.getAttribute('data-model');

    console.log("fileInput: ")
    console.log(fileInput)
    console.log("model: "+model)

    $.ajax({
        type: 'POST',
        url: "/restful/" + model + "/file", // Replace this with your actual Django endpoint URL
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response); // Handle the success response from Django
            Swal.fire("操作成功", "全部匯入正常").then(() => {
                location.reload();
              });
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("file error");
            if (xhr.status == 400 || xhr.status == 404) {
              var errorMessage = xhr.responseJSON.error;
              console.log(errorMessage);
              showSwal("操作失敗", errorMessage, "error", false).then(() => {
                location.reload();
              });
            } else if (xhr.status === 403) {
              alert("無權獲得該頁詳細，請聯絡管理員");
            } else {
              alert("系統發生錯誤");
              console.log(errorThrown);
            }

        }
    });

    // Handle the selected file here (e.g., read its contents, upload it, etc.)
});
