document.getElementById("approval_btn").onclick = handleApproval;

let Approval_id="";


function handleApproval() {
    var statusValue = document.getElementById("status").value;
    var feedbackValue = document.getElementById("feedback").value;
    
    console.log("Status: " + statusValue);
    console.log("Feedback: " + feedbackValue);

    var formData = {
        status:statusValue,
        feedback:feedbackValue,
        Approval_id:Approval_id
    };

    console.log("form data");
    console.log(formData);
    $.ajax({
        type: "post",
        url: "/restful/approval_process_log",
        data: formData,
        headers: {
            'X-CSRFToken': csrftoken
        },
        cache: false, 
        success: function (response) {
            alert("操作成功");
            location.reload();
        },
        error: function(error) {
            alert("簽核失敗")
            console.log('Error fetching events:', error);
        }
    });

};


$('#myTabs').hide();


$('#myModal').on('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var modalModel = button.getAttribute('data-url');
    console.log("modalModel " + modalModel);
    Approval_id = button.getAttribute('data-Approval_id');
    // console.log(Approval_id)
    var form = document.querySelector('form[name="' + modalModel + '"]');
    // console.log(form);

    GET_handleClick(button, false).then((data) => {
        // console.log(data)
        for (var key in data) {
            var input = form.querySelector('[name="' + key + '"]');
            if (input) {
                let get_value = jsonData[key];
                input.disabled = true;  // 禁用
                input.setAttribute("readonly", "true"); //封印修改

                if (input.type == 'file') {
                    var element = document.getElementById(key);
                    if (get_value != "") {
                        element.href = get_value;
                        element.target = "_blank";
                        element.textContent = "下載";
                    } else {
                        linkElement.href = "#";
                        linkElement.target = "_self";
                        element.textContent = "未提供";
                    }
                    continue
                }

                if (typeof (jsonData[key]) == "object" && get_value != null) {//判斷是不是陣列
                    // console.log(key)
                    // console.log(input)
                    SetSelect2(input, key, get_value);
                    continue
                }
                input.value = get_value;
                // console.log("key " + key + " 帶資料:" + get_value);

            } else {
                // console.log("Input not found for key:", key);
            }
        }

        const change_event = new Event("change");


        if (modalModel === 'Leave_Application') {
            // projectConfirmationIdControl.dispatchEvent(change_event);
            $('#tab1').tab('show');
        } else if (modalModel === 'work_overtime_application') {
            $('#tab2').tab('show');
        } else if (modalModel === 'project_employee_assign') {
            project_job_assign_IdControl.dispatchEvent(change_event);
            $('#tab3').tab('show');
        } else if (modalModel === 'clock_correction_application') {
            $('#tab4').tab('show');
        }

    });


});