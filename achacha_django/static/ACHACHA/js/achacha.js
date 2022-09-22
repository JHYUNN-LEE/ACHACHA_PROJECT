$(function() {
    var count0 = count1 = count2 = 0;

    timeCounter();

    function timeCounter() {

        id0 = setInterval(count0Fn, 0.00001);

        function count0Fn() {
        count0++;
        if (count0 > 2356) {
            clearInterval(id0);
        } else {
            $(".number").eq(0).text(count0);
        }

        }

        id1 = setInterval(count1Fn, 0.00001);

        function count1Fn() {
        count1++;
        if (count1 > 1000) {
            clearInterval(id1);
        } else {
            $(".number").eq(1).text(count1);
        }
        }
    }
    new Chart(document.getElementById("line-chart"), {
        type: 'line',
        data: {
            labels: [2016,2017,2018,2019],
            datasets: [{ 
                data: [756,845,928,988],
                label: "분실물 (단위 : 천개)",
                borderColor: "#3e95cd",
                fill: false
            }
            ]
        },
    });
});
