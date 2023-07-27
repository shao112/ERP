
let checked = []

function updateCheckedArray(checkbox) {
    console.log('觸發！');
    console.log(checkbox)

    const value = checkbox.value;
    const index = checked.indexOf(value);
    console.log(value)


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

        console.log(checkboxes)
        console.log(checkbox.value)
        console.log(checked.includes(checkbox.value))

    }
}

function getSelectedValues() {
    console.log(checked);
}
$('#table').on('page-change.bs.table', function (e, number, size) {
    Promise.resolve().then(function () {
        syncCheckedRowsWithArray();
    });
});
