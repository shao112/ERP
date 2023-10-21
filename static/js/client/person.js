var person_del_show = false; //在HTML 設定此變數開關

var person_btn = document.getElementById("person_form_btn");
if (person_btn) {
    person_btn.onclick = AddProcess;
}

var person_tbody = document.getElementById("person_tbody");

let person_str = document.getElementById("contact_str");

let person_ary = [];

function renderPersonsList() {
  person_tbody.innerHTML = ""; // 清空 tbody 的内容

  person_ary.forEach(function (formData, index) {
  var row = document.createElement("tr");

  var fields = [
    formData.name,
    formData.position,
    formData.telOrExt,
    formData.person_fax,
    formData.phone,
    formData.mail,
    formData.person_remark,
  ];

  fields.forEach(function (field) {
    var cell = document.createElement("td");
    cell.textContent = field;
    row.appendChild(cell);
  });
  
  if(person_del_show){

    var deleteButton = document.createElement("button");
    deleteButton.textContent = "刪除";
    deleteButton.onclick = function() {
      deleteItem(index);
    };
    var deleteCell = document.createElement("td");
    deleteCell.appendChild(deleteButton);
    row.appendChild(deleteCell);
  }


  person_tbody.appendChild(row);
});

var person_ary_str = JSON.stringify(person_ary);
if(person_str){
  person_str.value = person_ary_str;
}
}

function deleteItem(index) {
  person_ary.splice(index, 1);
  renderPersonsList();
}

function AddProcess() {
  var formData = {
    name: document.getElementById("name").value,
    position: document.getElementById("position").value,
    telOrExt: document.getElementById("telOrExt").value,
    person_fax: document.getElementById("person_fax").value,
    phone: document.getElementById("phone").value,
    mail: document.getElementById("mail").value,
    person_remark: document.getElementById("person_remark").value,
  };
  person_ary.push(formData);
  renderPersonsList();
}
