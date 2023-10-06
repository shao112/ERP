let api_url = window.location.href.replace("/salary/", "/restful/salary/");

function reset_salary() {
  Swal.fire({
    title: "小心執行",
    html: "準備計算系統薪資!<br><h5>此舉動會重製本頁的當月薪資! <strong>包括調整過的薪水!</strong></h5><br>如本頁無資料請放心使用",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "確定執行",
    cancelButtonText: "取消",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: api_url + "/reset",
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        contentType: "application/json",
        success: function (response) {
          alert("重製成功");
          location.reload();
        },
        error: function (xhr, textStatus, errorThrown) {
          var errorMessage = xhr.responseJSON.error;
          alert("系統發生錯誤" + errorMessage);
        },
      });
    }
  });
}

function add() {
  var selectElement = document.getElementById("salary-details-select");
  var selectedOption = selectElement.options[selectElement.selectedIndex];
  var selectedValue = selectedOption.value;
  var moneyInput = document.getElementById("money");
  var moneyValue = moneyInput.value;
  var detail_type = document.getElementById("detail_type");
  var detail_typeValue = detail_type.value;
  var checkbox = document.getElementById('five');
  var fiveisChecked = checkbox.checked;

  if(detail_typeValue<=0){
    alert("請選擇類型")
    return
  }

  var deduction = detail_typeValue.includes('加項') ? false : true;
  var tax_deduction = detail_typeValue.includes('應稅') ? true : false;
  

  data = {
    name: selectedValue,
    moneyValue: moneyValue,
    deduction: deduction,
    tax_deduction: tax_deduction,
    five:fiveisChecked,
  };  
  console.log(data);

  if(moneyValue<=0){
    alert("請輸入金額，或是輸入金額至少大於零。")
    return
  }

  $.ajax({
    url: api_url,
    method: "POST",
    data: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    contentType: "application/json",
    success: function (response) {
      alert("新增成功");
      location.reload();
    },
    error: function (xhr, textStatus, errorThrown) {
      var errorMessage = xhr.responseJSON.error;
      alert("系統發生錯誤" + errorMessage);
    },
  });
}

function del(itemid) {
  data = { itemid: itemid };
  $.ajax({
    url: api_url,
    method: "delete",
    data: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    contentType: "application/json",
    success: function (response) {
      console.log("刪除成功", response);
      alert("刪除成功");
      location.reload();
    },
    error: function (xhr, textStatus, errorThrown) {
      var errorMessage = xhr.responseJSON.error;
      alert("系統發生錯誤" + errorMessage);
    },
  });
}

function save(itemid) {
  var row = $("a[onclick=\"save('" + itemid + "')\"]").closest("tr");
  var name = row.find('input[name="name"]').val();
  var adjustmentAmount = row.find('input[name="adjustment_amount"]').val();
  var deduction = row.find('input[name="deduction"]').val();
  var deductionCheckbox = row.find('input[name="deduction"]');
  var deduction = deductionCheckbox.is(":checked");
  var tax_deductionCheckbox = row.find('input[name="tax_deduction"]');
  var tax_deduction = tax_deductionCheckbox.is(":checked");
  var fiveCheckbox = row.find('input[name="five"]');
  var five = fiveCheckbox.is(":checked");
  console.log("tax_deduction")
  console.log(tax_deduction)
  console.log(tax_deductionCheckbox)
  console.log(five)

  data = {
    name: name,
    adjustmentAmount: adjustmentAmount,
    itemid: itemid,
    deduction: deduction,
    tax_deduction: tax_deduction,
    five: five,
  };
  
  if(adjustmentAmount<=0){
    alert("輸入金額至少大於零。如需扣款請勾選為扣款項")
    return
  }
  
  $.ajax({
    url: api_url,
    method: "PUT",
    data: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    contentType: "application/json",
    success: function (response) {
      console.log("PUT 请求成功", response);
      alert("修改成功");
      location.reload();
    },
    error: function (xhr, textStatus, errorThrown) {
      var errorMessage = xhr.responseJSON.error;
      alert("系統發生錯誤" + errorMessage);
    },
  });
}
