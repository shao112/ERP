function SetSelect2(input, key, get_value) {
    const options = input.options;
    console.log("GET_" + key + "=> " );
    console.log(input);
    console.log(get_value)
    //CLEAN CHECK
    if (key=="vehicle"){ //多對多的選項清除
        var select2Instance = $(input).data('select2');
        
        // 取得目前所有選中的選項
        var selectedOptions = select2Instance.data();
        // 取消所有選中的選項
        selectedOptions.forEach(function(option) {
            select2Instance.trigger('unselect', {
                data: option
            });
        });
    }
   
    get_value = Object.values(get_value);
    if (get_value.length != 0) {
        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            const option_id = option.value;

            var containsValue = false;
            // console.log(typeof (get_value[0]))
            if (typeof (get_value[0]) == "object") {
                containsValue = get_value.find(item => item.id == option_id);
            } else {
                containsValue = get_value.find(item => item == option_id);
            }
            if (containsValue) {
                // console.log(option)
                option.selected = true;
            }
        }
    }
    $(`[name="${key}"]`).each(function() {
        $(this).trigger('change');
    });
    // $(selectname).trigger('change');
}