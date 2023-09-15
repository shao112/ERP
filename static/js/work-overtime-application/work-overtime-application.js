var start_hours_of_overtime = document.querySelector("#start_hours_of_overtime");
var end_hours_of_overtime = document.querySelector("#end_hours_of_overtime");

start_hours_of_overtime.addEventListener("change", calHoursDifference);
end_hours_of_overtime.addEventListener("change", calHoursDifference);

function calHoursDifference() {
    let value1 = parseInt(start_hours_of_overtime.value);
    let value2 = parseInt(end_hours_of_overtime.value);

    let difference = value2 - value1;

    document.querySelector("#overtime_hours").value = difference;
}

var start_mins_of_overtime = document.querySelector("#start_mins_of_overtime");
var end_mins_of_overtime = document.querySelector("#end_mins_of_overtime");

start_mins_of_overtime.addEventListener("change", calMinsDifference);
end_mins_of_overtime.addEventListener("change", calMinsDifference);

function calMinsDifference() {
    let value1 = parseInt(start_mins_of_overtime.value);
    let value2 = parseInt(end_mins_of_overtime.value);

    let difference = value2 - value1;

    document.querySelector("#overtime_mins").value = difference;
}