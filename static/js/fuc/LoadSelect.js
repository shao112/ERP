function SetSelect2(input, key, get_value) {
  console.log("GET_" + key + "=> ");
  console.log(input);
  console.log(get_value);
  //CLEAN CHECK
  if (key == "vehicle") {
    //多對多的選項清除
    var select2Instance = $(input).data("select2");

    // 取得目前所有選中的選項
    var selectedOptions = select2Instance.data();
    // 取消所有選中的選項
    selectedOptions.forEach(function (option) {
      select2Instance.trigger("unselect", {
        data: option,
      });
    });
  }

  get_value = Object.values(get_value);
  console.log(get_value);
  const options = input.options;
  var option_len = 0;
  try {
    option_len = Object.keys(options).length;
    console.log("option_len: " + option_len)
  } catch (error) {}

  if (get_value.length != 0) {
    console.log("get_value.length: " + get_value.length)
    for (let i = 0; i < option_len; i++) {
      const option = options[i];
      const option_id = option.value;

      var containsValue = false;
      // console.log(typeof (get_value[0]))
      console.log("option_id: " + option_id)
      if (typeof get_value[0] == "object") {
        containsValue = get_value.find((item) => item.id == option_id);
      } else {
        containsValue = get_value.find((item) => item == option_id);
      }
      if (containsValue) {
        console.log("選中: " + option.value)
        option.selected = true;
        console.log("containsValue: " + containsValue)
        break;
      }
    }
  }
  $(`[name="${key}"]`).each(function () {
    console.log("[name=" + key + "]")
    $(this).trigger("change");
  });
  // $(selectname).trigger('change');
}
