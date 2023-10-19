// 初始化一个空的eq_json_ary数组
var eq_json_ary = [];

// 新增纪录仪器项目的按钮点击事件处理程序
document.getElementById("Equipment_btn").addEventListener("click", function() {
    var equipment_select = document.getElementById("equipment_select");
    var eq_status = document.getElementById("eq_status");

    var equipment_id = equipment_select.value;
    var equipment_name = equipment_select.options[equipment_select.selectedIndex].text;
    var status = eq_status.value;

    // 创建一个新的对象，并将其添加到eq_json_ary数组中
    var newEquipment = {
        equipment_id: equipment_id,
        equipment_name: equipment_name,
        status: status
    };
    eq_json_ary.push(newEquipment);

    // 重新渲染eq_table
    renderEqTable();
});

// 重新渲染eq_table的函数
function renderEqTable() {
    var eq_table = document.getElementById("eq_table");
    eq_table.innerHTML = '';

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
        deleteBtn.addEventListener("click", (function(index) {
            return function() {
                deleteEquipment(index);
            };
        })(i));
        cell4.appendChild(deleteBtn);
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
