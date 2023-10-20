var eq_json_ary = [];
let carry_equipments_str = document.getElementById("carry_equipments_str");

var Equipment_btn = document.getElementById("Equipment_btn");
if (Equipment_btn) {
  Equipment_btn.addEventListener("click", add_Eq);
}

function add_Eq() {
  var equipment_select = document.getElementById("equipment_select");
  var eq_status = document.getElementById("eq_status");

  var id = equipment_select.value;
  var equipment_data =
    equipment_select.options[equipment_select.selectedIndex].text;
  console.log(equipment_data);
  equipment_data = equipment_data.split(" ");
  var status = eq_status.value;

  var newEquipment = {
    id: id,
    equipment_id: equipment_data[0],
    equipment_name: equipment_data[1],
    status: status,
  };
  eq_json_ary.push(newEquipment);

  renderEqTable();
}

function renderEqTable() {
  var eq_table = document.getElementById("eq_table");
  eq_table.innerHTML = "";

  for (var i = 0; i < eq_json_ary.length; i++) {
    var equipment = eq_json_ary[i];
    var row = eq_table.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);

    cell1.innerHTML = equipment.equipment_id;
    cell2.innerHTML = equipment.equipment_name;
    cell3.innerHTML = equipment.status;

    // 添加删除按钮并为其添加点击事件
    var deleteBtn = document.createElement("button");
    deleteBtn.innerHTML = "删除";
    deleteBtn.classList.add("btn", "btn-danger", "btn-sm");
    deleteBtn.addEventListener(
      "click",
      (function (index) {
        return function () {
          deleteEquipment(index);
        };
      })(i)
    );
    if(carry_equipments_str){ //在派工單有carry_equipments_str dom ，但是在簽核頁面沒carry_equipments_str
        cell4.appendChild(deleteBtn);
    }
  }

  var eq_json_ary_str = JSON.stringify(eq_json_ary);
  if (eq_json_ary_str && carry_equipments_str) {
        carry_equipments_str.value = eq_json_ary_str;        
  }
}

// 删除eq_json_ary的函数
function deleteEquipment(index) {
  eq_json_ary.splice(index, 1);
  renderEqTable();
}

// 新增eq_json_ary的函数
function addEquipment(equipment) {
  eq_json_ary.push(equipment);
  renderEqTable();
}
