function createApprovalStageElement(jsonData){
    // 先清除子元素
    var stageDiv = document.getElementById("approval_stage");
    while(stageDiv.hasChildNodes()){
        stageDiv.removeChild(stageDiv.firstChild);
    }

    var stageArray = jsonData // User物件的id
    console.log(stageArray)
    for (let i = 0; i < stageArray.length; i++) {
        var newDiv = document.createElement("div");
        newDiv.className = "form-group form-row d-flex justify-content-between align-items-center";

        var label = document.createElement("label");
        label.setAttribute("for", "stage-" + i);
        label.textContent = "第 " + (i+1) + " 關";

        var span = document.createElement("span");
        span.textContent = stageArray[i].name;
        var employee_id = stageArray[i].id;

        var a = document.createElement("a")
        a.setAttribute("type", "button")
        a.className = "sys_del btn btn-sm btn-danger";
        var icon = document.createElement("i");
        icon.className = "far fa-sm fa-trash-alt";
        a.appendChild(icon);
        a.addEventListener("click",function(){
            $.ajax({
                type: "DELETE",
                url: "/restful/approval_group",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                data:{
                    set_id:set_id,
                    employee_id:employee_id,
                },
                success: function (response) {
                    alert("刪除成功!");
                    sendApprovalGroup(set_id);
                },
                error: function (error) {
                    alert("刪除失敗!");
                    console.log("Error:", error);
                },
            });
        })
        newDiv.appendChild(label);
        newDiv.appendChild(span);
        newDiv.appendChild(a);
        stageDiv.appendChild(newDiv);
    }
}
var set_id = ""
function sendApprovalGroup(id) {
    set_id = id;
    $.ajax({
        type: "GET",
        url: "/restful/approval_group",
        data: {
            id: id
        },
        success: function (response) {
            jsonData = response.data;
            for (var key in jsonData) {
                console.log("key " + key)
                if(key == "name"){
                    var h5 = document.getElementById(key);
                    if (h5) {
                        h5.textContent = jsonData[key];
                    }
                }
                if(key == "approval_order"){
                    createApprovalStageElement(jsonData[key]);
                }
                if(key == "is_director"){
                    var is_director = document.getElementById(key);
                    if(jsonData[key]){
                        console.log("is_director.checked = true;")
                        is_director.checked = true;
                    }else{
                        console.log("is_director.checked = false;")
                        is_director.checked = false;
                    }
                }

            }
        },
        error: function (error) {
            console.error("錯誤", error);
        }
    });
}
document.getElementById("submitEmployeeBtn").onclick = submitEmployee;
function submitEmployee(){
    const new_stage_select = document.getElementById("new_stage");
    const new_stage_id = new_stage_select.value;
    $.ajax({
        type: 'POST',
        url: '/restful/approval_group',
        data: {
            new_stage_id: new_stage_id,
            set_id: set_id
        },
        headers: {
            "X-CSRFToken": csrftoken,
        },
        success: function(response) {
            console.log(response);
            sendApprovalGroup(set_id)
        },
        error: function(error) {
            console.log(error);
            // 員工已被選過錯誤處理
        }
    })
}


/* --- 監聽是否勾選直屬主管，發送post請求 --- */
var is_director_checkbox = document.getElementById("is_director")
is_director_checkbox.addEventListener("change",function(){
    $.ajax({
        type: "POST",
        url: "/restful/approval_group",
        data: {
            set_id:set_id,
            is_checked: is_director_checkbox.checked,
        },
        headers: {
            "X-CSRFToken": csrftoken,
        },
        success: function (response) {
            
        },
        error: function (error) {
            alert("錯誤", error);
        }
    });
})