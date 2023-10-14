var year_moneys = [];

var yearMoneyStrInput = document.getElementById("year_money_str");

function addYearMoney() {
  var yearInput = document.getElementById("year");
  var priceInput = document.getElementById("price");

  if (!yearInput.checkValidity() || !priceInput.checkValidity()) {
    alert("請輸入有效的數字！");
    return;
  }

  var year = parseInt(yearInput.value);
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
  year_moneys.sort(function(a, b) {
      return b.year - a.year;
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
