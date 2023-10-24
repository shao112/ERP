var year_moneys = [];

var yearMoneyStrInput = document.getElementById("year_money_str");

function addYearMoney() {
  var yearInput = document.getElementById("year");
  var priceInput = document.getElementById("price");


  if (!yearInput.checkValidity() || !priceInput.checkValidity()) {
    alert("請輸入有效的數字！");
    return;
  }

  var year = yearInput.value;
  if (year==""){
    alert("請輸入調整日期")
    return
  }
  var date = new Date(year);
  var yearFormatted = date.getFullYear();
  var month = String(date.getMonth() + 1).padStart(2, "0"); // 月份从 0 开始，需要 +1
  var day = String(date.getDate()).padStart(2, "0");

  // 拼接成 YYYY-MM-DD 格式
  year = `${yearFormatted}/${month}/${day}`;
  console.log("year", year);

  var price = parseFloat(priceInput.value);

  var data = { year: year, price: price };
  year_moneys.push(data);

  yearInput.value = "";
  priceInput.value = "";

  renderTable();
}

function deleteYearMoney(index) {
  year_moneys.splice(index, 1);
  renderTable();
}

function renderTable() {
  year_moneys.sort(function (a, b) {
    return new Date(b.year).getTime() - new Date(a.year).getTime();
  });

  var yearMoneyJson = JSON.stringify(year_moneys);
  yearMoneyStrInput.value = yearMoneyJson;

  var tbody = document.getElementById("yearTable");
  tbody.innerHTML = "";

  for (var i = 0; i < year_moneys.length; i++) {
    var row = tbody.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = year_moneys[i].year;
    cell2.innerHTML = year_moneys[i].price;
    cell3.innerHTML =
      '<button onclick="deleteYearMoney(' + i + ')">刪除</button>';
  }
}
