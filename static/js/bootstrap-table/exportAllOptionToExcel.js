function exportAllOptionToExcel(fileName) {
    var fileName = fileName
    var exportUrl = document.querySelector('button[data-export-url]').getAttribute('data-export-url');
    // 1. 使用 BT 提供的 getData 取得所有分頁資料，回傳值為 Array
    var allTableData= $('#table').bootstrapTable('getData',{useCurrentPage:false,includeHiddenRows:false});
    // 2. 重組，篩選掉 data-force-hide="true" 欄位
    var tableColumns = $('#table').bootstrapTable('getVisibleColumns');
    var filteredData = allTableData.map(function(row) {
        var filteredRow = {};
        for (var i = 0; i < tableColumns.length; i++) {
            var column = tableColumns[i];
            var key = column.field;
            var forceHide = column.forceHide;
            if (!forceHide) {
                filteredRow[key] = row[key];
            }
        }
        return filteredRow;
    });
    // console.log("篩選過欄位的所有值: " + JSON.stringify(filteredData))

    // 把表頭存起來，排除掉有 data-no-print 屬性的
    var tableData = [];
    var rows = document.getElementById("table").rows;
    var headers = [];
    for (var i = 0; i < rows[0].cells.length; i++) {
        // console.log("rows[0].cells[i]: "+rows[0].cells[i].getAttribute("data-no-print"))
        // headers.push(rows[0].cells[i].innerText);
        var cell = rows[0].cells[i];
        if (!cell.getAttribute("data-no-print")) {
            headers.push(cell.innerText);
        }
    }
    // 3. 重新包裝 JSON 數據，透過 headers 將英文欄位名稱轉換為中文欄位名稱
    var translatedData = filteredData.map(function(row) {
        var translatedRow = {};
        var keys = Object.keys(row); // 獲取 row 的所有鍵
        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            var chineseKey = headers[i];
            translatedRow[chineseKey] = row[key];
            if (key === "attachment") {
                // 如果是連結欄位，則將 HTML 連結轉換為純文字
                var value = row[key];
                var temp = document.createElement("div");
                temp.innerHTML = value;
                translatedRow[chineseKey] = temp.textContent || temp.innerText || "";
            }
        }
        return translatedRow;
    });
    // console.log("translatedData: "+ JSON.stringify(translatedData))
    
    for (var i = 1; i < rows.length; i++) {
        var rowData = {};
        for (var j = 0, k = 3; j < headers.length; j++,k++) {
        rowData[headers[j]] = rows[i].cells[k].innerText;
        }
        tableData.push(rowData);
    }
    fetch(exportUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, 
        },
        body: JSON.stringify({
            headers: headers,
            // data: tableData,
            data: translatedData,
        }),
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
}