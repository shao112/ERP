function check_process(check_statu, csrftoken) {
    let clock_in_or_out = true;
    if (check_statu == "clock-out") {
        clock_in_or_out = false;
    }

    navigator.geolocation.getCurrentPosition(function (position) {
        var gps = position.coords.latitude + ',' + position.coords.longitude;

        // 建立傳送的資料物件
        var requestData = {
            gps: gps,
            clock_in_or_out: clock_in_or_out,
            clock_time : new Date().toISOString()
        };

        console.log("clock_time")
        console.log(clock_time)
        // 傳送資料到後端
        fetch('/restful/check', {
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
                    if (clock_in_or_out){
                        alert('打卡成功！');
                        location.reload();
                        // sweetAlert('簽到成功！');
                    }else{                        
                        alert('打卡成功！');
                        location.reload();
                        // sweetAlert('簽退成功！');
                    }
            })
            .catch(function (error) {
                console.log('錯誤：', error);
            });


    }), function (error) {
        if (error.code === error.PERMISSION_DENIED) {
            alert('請打開GPS存取權限，否則無法完成打卡/簽退！');
        }
    }
}
