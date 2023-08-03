
let all_Equipment_checked = []

function update_all_Equipment_checkedArray(checkbox) {
    console.log('觸發！');
    console.log(checkbox)

    const value = checkbox.value;
    const index = all_Equipment_checked.indexOf(value);
    console.log(value)


    if (checkbox.checked && index === -1) {
        all_Equipment_checked.push(value);
    } else if (!checkbox.checked && index !== -1) {
        all_Equipment_checked.splice(index, 1);
    }
    console.log(all_Equipment_checked)
}
function syncall_Equipment_checkedRowsWithArray() {
    console.log(all_Equipment_checked)
    const checkboxes = document.getElementsByName("importcheckd");
    for (let i = 0; i < checkboxes.length; i++) {
        const checkbox = checkboxes[i];
        checkbox.checked = all_Equipment_checked.includes(checkbox.value);

        // console.log(checkboxes)
        // console.log(checkbox.value)
        // console.log(all_Equipment_checked.includes(checkbox.value))

    }
}

$("form").on("submit", function (event) {
    console.log("dEEEEE資產送");
    console.log(all_Equipment_checked);

})

function getSelectedValues() {
    console.log("dEEEEE資產送");
    console.log(all_Equipment_checked);
}
$('#Equipment_table').on('page-change.bs.table', function (e, number, size) {
    Promise.resolve().then(function () {
        syncall_Equipment_checkedRowsWithArray();
    });
});
