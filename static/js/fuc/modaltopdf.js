function exportToPDF() {
    var modalContent = document.getElementById('modal-download_pdf');
    console.log(modalContent);
    var doc = new jsPDF();

    html2canvas(modalContent).then(function (canvas) {
        // 獲取canvas的圖像數據URL
        var imgData = canvas.toDataURL('image/png');

        // 設置PDF的尺寸，這裡使用A4尺寸，也可以自行調整
        var pdf = new jsPDF('p', 'mm', 'a4');

        // 添加圖像數據到PDF
        pdf.addImage(imgData, 'PNG', 5, 20, 200, 100);

        // 下載PDF文件
        pdf.save('工程確認單.pdf');
    });
}