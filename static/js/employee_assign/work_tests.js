var tests_btn = document.getElementById("test_items_form_btn");
if (tests_btn) {
  tests_btn.onclick = AddProcess;
}

var worklist_tbody = document.getElementById("worklist_tbody");

let test_items_str = document.getElementById("test_items_str");

let work_tests_ary = [];

function renderTestsList() {
  worklist_tbody.innerHTML = ""; // 清空 tbody 的内容

  work_tests_ary.forEach(function (formData, index) {
    var row = document.createElement("tr");

    var fields = [
      formData.test_items,
      formData.format_and_voltage,
      formData.test_date,
      formData.level,
      formData.test_location,
      formData.number,
    ];

    fields.forEach(function (field) {
      var cell = document.createElement("td");
      cell.textContent = field;
      row.appendChild(cell);
    });
    
    var deleteButton = document.createElement("button");
    deleteButton.textContent = "刪除";
    deleteButton.onclick = function() {
      deleteItem(index);
    };
    var deleteCell = document.createElement("td");
    deleteCell.appendChild(deleteButton);
    row.appendChild(deleteCell);


    worklist_tbody.appendChild(row);
  });

  // 同步
  var work_ary_str = JSON.stringify(work_tests_ary);
  if(test_items_str){
    test_items_str.value = work_ary_str;
  }
}

function deleteItem(index) {
  work_tests_ary.splice(index, 1);
  renderTestsList();
}

function AddProcess() {
  var formData = {
    test_items: document.getElementById("test_items").value,
    test_date: document.getElementById("test_date").value,
    test_location: document.getElementById("test_location").value,
    format_and_voltage: document.getElementById("format_and_voltage").value,
    level: document.getElementById("level").value,
    number: document.getElementById("number").value,
  };
  work_tests_ary.push(formData);
  renderTestsList();
}
