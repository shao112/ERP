var start_hours_of_leave = document.querySelector("#start_hours_of_leave");
var end_hours_of_leave = document.querySelector("#end_hours_of_leave");

start_hours_of_leave.addEventListener("change", calHoursDifference);
end_hours_of_leave.addEventListener("change", calHoursDifference);

function calHoursDifference() {
    let value1 = parseInt(start_hours_of_leave.value);
    let value2 = parseInt(end_hours_of_leave.value);

    let difference = value2 - value1;

    document.querySelector("#leave_hours").value = difference;
}

var start_mins_of_leave = document.querySelector("#start_mins_of_leave");
var end_mins_of_leave = document.querySelector("#end_mins_of_leave");

start_mins_of_leave.addEventListener("change", calMinsDifference);
end_mins_of_leave.addEventListener("change", calMinsDifference);

function calMinsDifference() {
    let value1 = parseInt(start_mins_of_leave.value);
    let value2 = parseInt(end_mins_of_leave.value);

    let difference = value2 - value1;

    document.querySelector("#leave_mins").value = difference;
}