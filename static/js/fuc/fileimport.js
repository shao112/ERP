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



//匯入處理
var fileInput = document.getElementById('fileInput');
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
            location.reload();
        },
        error: function (error) {
            console.error(error); // Handle the error response, if any
        }
    });

    // Handle the selected file here (e.g., read its contents, upload it, etc.)
});
