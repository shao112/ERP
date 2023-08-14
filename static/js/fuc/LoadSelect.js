function SetSelect2(input, key, get_value) {
    const options = input.options;
    selectname = `#${key}_select2`
    console.log("GET_" + key + "=> " + selectname);
    // console.log(get_value)
    get_value = Object.values(get_value);
    if (get_value.length == 0) {
        return
    }
    // console.log(get_value)
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
        // console.log(get_value)
        // console.log(option_id)
        // console.log(containsValue)
        if (containsValue) {
            option.selected = true;
        }
    }
    $(selectname).trigger('change');
}