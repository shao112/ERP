let clonedRow = $("#work_item_form_row").clone();
let clonedIndex = 0;
clonedRow.removeAttr("hidden");
clonedRow.attr("id", "");
clonedRow.addClass("new_row");


let work_id_select_id=0
$(document).on('click', '.work_list_set_id', function () {
    console.log("work_id clicked");
    var work_id = $(this).attr('id'); //獲得點選的id
    console.log(work_id);
    var parts = work_id.split('_');
    var lastPart = parts[parts.length - 1];
    var number = parseInt(lastPart);
    work_id_select_id=number;
    console.log("chosen ",work_id_select_id);
    console.log(work_id_select_id);
});



function set_work_select_id(id) { //傳入工項id
    let selectID="work_select_"+work_id_select_id;
    var choose_input = document.getElementById(selectID);
    if(!choose_input){
        alert("selectname設定錯誤");
    }
    choose_input.value = id;
    const change_event = new Event("change");
    choose_input.dispatchEvent(change_event);
    $('#work_listid').modal('hide');
}

function add_work_item() {
    console.log("click");
    clonedIndex += 1;//根據clonedIndex設定新id
    new_cloneRow = clonedRow.clone(); 
    new_cloneRow.find('a').attr('id', 'work_' + clonedIndex);
    new_cloneRow.find('select').attr('id', 'work_select_' + clonedIndex); 
    new_cloneRow.find("select").select2({
        width: '100%',
    });
    $("#quotation_input").append(new_cloneRow);

};


function deleteWorkItemRow(button) {
    var rowToDelete = button.closest('.form-row');
    rowToDelete.remove();
}