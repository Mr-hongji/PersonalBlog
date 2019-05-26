$(function(){
    var clock = document.getElementById("clock");
    
    //获取时钟id
    var time_info = document.getElementById("time_info"),
        
        date_info = document.getElementById("date_info"),//获取date_info
       
        now_week = document.getElementById("now_week");
       
    //3、设置动态时间
    function setTime(){
        var nowdate = new Date();
        
        //获取年月日时分秒
        var year = nowdate.getFullYear(),
            month = nowdate.getMonth()+1,
            day = nowdate.getDay(),
            hours = nowdate.getHours(),
            minutes = nowdate.getMinutes(),
            seconds = nowdate.getSeconds(),
            date = nowdate.getDate();
        var weekday =["星期日","星期一","星期二","星期三","星期四","星期五","星期六"];
        // 获取日期id
        date_info.innerHTML=year+"年"+month+"月"+date+"日  ";
        now_week.innerHTML = weekday[day];
        time_info.innerHTML = (hours >=10 ? hours : "0"+hours) + ":" + (minutes >=10 ? minutes : "0"+minutes) +":"+ (seconds >=10 ? seconds : "0"+seconds);
        
        console.log(year+"年"+month+"月"+day+"日   "+weekday[day]);
        
    }
       setTime();
       
      setInterval(setTime, 1000);
    
    
});