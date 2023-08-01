function exportAllOptionToExcel(fileName) {
    var fileName = fileName
    var exportUrl = document.querySelector('button[data-export-url]').getAttribute('data-export-url');
    var tableData = [];
    var rows = document.getElementById("table").rows;
    var headers = [];
    for (var i = 3; i < rows[0].cells.length; i++) {
        headers.push(rows[0].cells[i].innerText);
    }
    
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
            data: tableData,
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