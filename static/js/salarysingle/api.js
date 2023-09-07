let api_url = window.location.href.replace("/salary/", "/restful/salary/")

function add() {
    var selectElement = document.getElementById("salary-details-select");
    var selectedOption = selectElement.options[selectElement.selectedIndex];
    var selectedValue = selectedOption.value;
    var moneyInput = document.getElementById("money");
    var moneyValue = moneyInput.value;



    var deductionValue = salaryDetails.find(detail => detail.name === selectedValue)?.deduction;
    if (deductionValue == undefined) {
        deductionValue = false
    }
    data = { "name": selectedValue, "moneyValue": moneyValue, "deductionValue": deductionValue }

    console.log("Selected Value: " + selectedValue);
    console.log("deductionValue Value: " + deductionValue);
    console.log("Money Value: " + moneyValue);
    console.log(data);

    $.ajax({
        url: api_url,
        method: 'POST',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken,
        },
        contentType: 'application/json',
        success: function (response) {
            alert("新增成功");
            location.reload();
        },
        error: function (xhr, textStatus, errorThrown) {
            var errorMessage = xhr.responseJSON.error;
            alert("系統發生錯誤" + errorMessage);
        }
    });

}
function del(itemid) {
    data = { "itemid": itemid }
    $.ajax({
        url: api_url,
        method: 'delete',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken,
        },
        contentType: 'application/json',
        success: function (response) {
            console.log('刪除成功', response);
            alert("刪除成功");
            location.reload();
        },
        error: function (xhr, textStatus, errorThrown) {
            var errorMessage = xhr.responseJSON.error;
            alert("系統發生錯誤" + errorMessage);
        }
    });

}

function save(itemid) {
    var row = $('a[onclick="save(\'' + itemid + '\')"]').closest('tr');
    var name = row.find('input[name="name"]').val();
    var adjustmentAmount = row.find('input[name="adjustment_amount"]').val();
    var deduction = row.find('input[name="deduction"]').val();
    var deductionCheckbox = row.find('input[name="deduction"]');
    var deduction = deductionCheckbox.is(':checked');

    data = { "name": name, "adjustmentAmount": adjustmentAmount, "itemid": itemid, "deduction": deduction }
    $.ajax({
        url: api_url,
        method: 'PUT',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken,
        },
        contentType: 'application/json',
        success: function (response) {
            console.log('PUT 请求成功', response);
            alert("修改成功");
            location.reload();
        },
        error: function (xhr, textStatus, errorThrown) {
            var errorMessage = xhr.responseJSON.error;
            alert("系統發生錯誤" + errorMessage);
        }
    });

}



