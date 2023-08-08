
let all_Equipment_checked = []

var carry_equipments_select2 = document.getElementById("carry_equipments_select2");

function update_all_Equipment_checkedArray(checkbox) {
    console.log('觸發！');
    console.log(checkbox)

    const value = checkbox.value;
    const index = all_Equipment_checked.indexOf(value);
    console.log(value)

    const option = carry_equipments_select2.querySelector(`option[value="${value}"]`);
    if (option) {
        option.selected = checkbox.checked;
    }

    if (checkbox.checked && index === -1) {
        all_Equipment_checked.push(value);
    } else if (!checkbox.checked && index !== -1) {
        all_Equipment_checked.splice(index, 1);
    }

    console.log(all_Equipment_checked)
    const options = carry_equipments_select2.options;
    for (let i = 0; i < options.length; i++) {
        console.log(`Option value: ${options[i].value}, Selected: ${options[i].selected}`);
    }

}

function syncall_Equipment_checkedRowsWithArray() {
    console.log(all_Equipment_checked)
    const checkboxes = document.getElementsByName("importcheckd");
    for (let i = 0; i < checkboxes.length; i++) {
        const checkbox = checkboxes[i];
        checkbox.checked = all_Equipment_checked.includes(checkbox.value);
    }
}


$('#Equipment_table').on('page-change.bs.table', function (e, number, size) {
    Promise.resolve().then(function () {
        syncall_Equipment_checkedRowsWithArray();
    });
});
