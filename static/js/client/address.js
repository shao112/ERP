var address_del_show = true; //在HTML 設定此變數開關

var address_btn = document.getElementById("address_form_btn");
if (address_btn) {
    address_btn.onclick = AddProcess;
}

var address_tbody = document.getElementById("address_tbody");

let address_str = document.getElementById("address_str");

let address_ary = [];

function renderAddressList() {
  address_tbody.innerHTML = ""; // 清空 tbody 的内容

  address_ary.forEach(function (formData, index) {
  var row = document.createElement("tr");

  var fields = [
    formData.contact_address,
    formData.address_remark,
  ];

  fields.forEach(function (field) {
    var cell = document.createElement("td");
    cell.textContent = field;
    row.appendChild(cell);
  });
  
  if(address_del_show){

    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "刪除";
    deleteButton.onclick = function() {
      deleteAddress(index);
    };
    var deleteCell = document.createElement("td");
    deleteCell.appendChild(deleteButton);
    row.appendChild(deleteCell);
  }


  address_tbody.appendChild(row);
});

var address_ary_str = JSON.stringify(address_ary);
if(address_str){
  address_str.value = address_ary_str;
}
}

function deleteAddress(index) {
  address_ary.splice(index, 1);
  renderAddressList();
}

function AddProcess() {
  var formData = {
    contact_address: document.getElementById("contact_address").value,
    address_remark: document.getElementById("address_remark").value,
  };
  address_ary.push(formData);
  renderAddressList();
  $("#person_tab input").val('');
}
