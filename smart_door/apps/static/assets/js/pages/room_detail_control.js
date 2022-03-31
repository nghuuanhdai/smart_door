'use strict';
function GetDates(startDate, daysToAdd) {
    var aryDates = [];

    for (var i = 0; i < daysToAdd; i++) {
        var currentDate = new Date();
        currentDate.setDate(startDate.getDate() + i);
        aryDates.push(currentDate.getDate() + "/" + MonthAsString(currentDate.getMonth()) + "/" + currentDate.getFullYear());
    }

    return aryDates;
}

function MonthAsString(monthIndex) {
    var d = new Date();
    var month = new Array();
    month[0] = "01";
    month[1] = "02";
    month[2] = "03";
    month[3] = "04";
    month[4] = "05";
    month[5] = "06";
    month[6] = "07";
    month[7] = "08";
    month[8] = "09";
    month[9] = "10";
    month[10] = "11";
    month[11] = "12";

    return month[monthIndex];
}

$(document).ready(function() {
    var startDate = new Date();
    var aryDates = GetDates(startDate, 7);
    for (let i = 0; i < 7; i++) {
        $($(".th-timecell")[i]).find('span').html(aryDates[i]);
    }
    $(".timecell").click(function() {
        $(this).toggleClass("timecell-selected");
        let col_idx = $(this).index();
        let time = $(this).siblings("td:first").find('span').text();
        time = time.split(':')[0];
        let datetime = $($('th')[col_idx]).find('span').text();
        let room = window.location.pathname.split('/')[1];
        console.log("Time:", time);
        console.log("Datetime:", datetime);
        console.log("Room:", room);
        let data = {"room": room, "time": time, "datetime": datetime};
        if ($(this).hasClass('timecell-selected')) { // booked
            $.ajax({
                type: "POST",
                url: 'post/ajax/add_sched',
                data: data,
                success: (res) => {
                    alert("OK");
                },
                error: (res) => {
                    console.log(res);
                }
            });
        } else { // unbooked
            $.ajax({
                type: "POST",
                url: 'post/ajax/del_sched',
                data: data,
                success: (res) => {
                    alert("OK");
                },
                error: (res) => {
                    console.log(res);
                }
            });
        }
    });
});