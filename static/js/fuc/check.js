function check_process(check_statu, csrftoken) {
    let clock_in_or_out = true;
    if (check_statu == "clock-out") {
        clock_in_or_out = false;
    }

    navigator.geolocation.getCurrentPosition(function (position) {
        var gps = position.coords.latitude + ',' + position.coords.longitude;
        // console.log("gps", gps)

        // 建立傳送的資料物件
        var requestData = {
            gps: gps,
            clock_in_or_out: clock_in_or_out
        };

        // 傳送資料到後端
        fetch('/Backend/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(requestData)
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (responseData) {
                if (responseData.status === 'success') {
                    alert('打卡/簽退成功！');
                } else {
                    alert('打卡/簽退失敗！');
                }
            })
            .catch(function (error) {
                console.log('錯誤：', error);
            });


    }), function (error) {
        if (error.code === error.PERMISSION_DENIED) {
            alert('拒絕存取 GPS，無法完成打卡/簽退！');
        }
    }
}
