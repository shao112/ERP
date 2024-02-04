
let checked = []

function updateCheckedArray(checkbox) {

    const value = checkbox.value;
    const index = checked.indexOf(value);


    if (checkbox.checked && index === -1) {
        checked.push(value);
    } else if (!checkbox.checked && index !== -1) {
        checked.splice(index, 1);
    }
    console.log(checked)
}
function syncCheckedRowsWithArray() {
    console.log(checked)
    const checkboxes = document.getElementsByName("importcheckd");
    for (let i = 0; i < checkboxes.length; i++) {
        const checkbox = checkboxes[i];
        checkbox.checked = checked.includes(checkbox.value);

    }
}

function getSelectedValues() {
    return checked;
}

$('#table').on('page-change.bs.table', function (e, number, size) {
    Promise.resolve().then(function () {
        syncCheckedRowsWithArray();
    });
});

//複製api

function Cloneapi(modelname) {
    const selectedValues = getSelectedValues();
    $.ajax({
        url: "/restful/ClonePost",
        type: 'POST',
        contentType: 'application/json',
        headers: {
            "X-CSRFToken": csrftoken,
          },
        data: JSON.stringify({ selectedValues: selectedValues,modelname:modelname }),
        success: function(data) {
            console.log(data);
            Swal.fire("操作成功", "完成").then(() => {
                location.reload();
              });
        },
        error: function(error) {
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
        
                Swal.fire({
                  title: '操作失敗',
                  html: errorMessageHTML,
                  icon: 'error',
                  confirmButtonText: '確定'
                });
        
              } else if (xhr.status === 403) {
                alert("無權獲得該頁詳細或操作，請聯絡管理員");
              } else {
                alert("系統發生錯誤");
                console.log(errorThrown);
              }
        }
    });
}
