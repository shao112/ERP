$("#myTabs").hide();

$("#myModal").on("show.bs.modal", function (event) {
  var button = event.relatedTarget;
  var modalModel = button.getAttribute("data-url");
  var created_by = button.getAttribute("data-created_by");
  console.log("modalModel " + modalModel);
  console.log(created_by);

  var get_created_DOM = document.getElementById("set_author");
  if (get_created_DOM != undefined) {
    get_created_DOM.textContent = "申請人:" + created_by;
  }

  Approval_id = button.getAttribute("data-Approval_id");

  var form = document.querySelector('form[name="' + modalModel + '"]');

  GET_handleClick(button, false).then((data) => {
    // console.log(data)

    for (var key in data) {
      var input = form.querySelector('[name="' + key + '"]');
      let get_value = jsonData[key];
      if (input) {
        input.disabled = true; // 禁用
        input.setAttribute("readonly", "true"); //封印修改
        console.log(key, get_value);

        if (input.type == "file") {
          var element = form.querySelector("#" + key);
          // console.log("FILE")
          if (get_value != null) {
            element.href = get_value;
            element.target = "_blank";
            element.textContent = "下載";
          } else {
            element.href = "#";
            element.target = "_self";
            element.textContent = "未提供檔案";
          }
          continue;
        }

        if (typeof jsonData[key] == "object" && get_value != null) {
          //判斷是不是陣列
          // console.log(key)
          // console.log(input)
          SetSelect2(input, key, get_value);
          continue;
        }
        input.value = get_value;
        // console.log("key " + key + " 帶資料:" + get_value);
      } else {
        // 處理不存在input的額外特例欄位
        if (key == "carry_equipments_str") {
          eq_json_ary=get_value;
          renderEqTable();
          continue;
        }
        if (key == "test_items_str") {
          if(get_value){

            var jsonArray = JSON.parse(get_value);  
            work_tests_ary=jsonArray;
            renderTestsList();
          }else{
            worklist_tbody.innerHTML="無資料"            
          }        
          continue;
        }

      }
    }

    const change_event = new Event("change");

    if (modalModel === "leave_application") {
      // projectConfirmationIdControl.dispatchEvent(change_event);
      $("#tab1").tab("show");
    } else if (modalModel === "work_overtime_application") {
      $("#tab2").tab("show");
    } else if (modalModel === "project_employee_assign") {
      project_job_assign_IdControl.dispatchEvent(change_event);
      $("#tab3").tab("show");
    } else if (modalModel === "clock_correction_application") {
      $("#tab4").tab("show");
    } else if (modalModel === "Travel_Application") {
      console.log("xxxx");
      $("#tab5").tab("show");
    } else {
      alert("沒對應的TAB");
    }
  });
});
