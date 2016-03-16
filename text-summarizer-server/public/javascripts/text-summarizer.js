function drawResults(sentence_data) {
    google.charts.load("current", {packages:['corechart']});
    google.charts.setOnLoadCallback(drawChart);
    data_array = [["Sentence", "Rank", { role: "style" } ]];
    for (var i = 0; i<sentence_data.length; i++) {
        data_array.push([sentence_data[i][0], sentence_data[i][1], (sentence_data[i][2] == 0) ? "opacity: 0.2" : "color: #76A7FA"]);
    }
    function drawChart() {
      var data = google.visualization.arrayToDataTable(data_array);

      var view = new google.visualization.DataView(data);

      var options = {
        title: "Selected Sentences by Rank",
        width: 500,
        height: 400,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },
        hAxis: {format: "0"},
      };
      var chart = new google.visualization.ColumnChart(document.getElementById("chart-div"));
      chart.draw(view, options);
    }
}

function summarizeText() {
    var text = $('#text').val();
    var percentage = $('#percentage').val();
    $.ajax({
        url: '/summarize',
        method: 'POST',
        data: {
            'text': text,
            'compression': percentage
        },
        success: function(data) {
            var sentences_data = eval(data[0]);
            var title = data[1];
            var summary = '';
            for (var i=2; i<data.length; i++) {
                summary += data[i];
                summary += ' ';
            }
            $('#summary-title').text(title);
            $('#summary-text').text(summary);
            $('#header').text("Summary results")
            drawResults(sentences_data);
            $('#make-summary').hide();
            $('#summary-made').show();
            $('#wait-modal').modal('hide');
        },
        error: function(err) {
            
            console.log(err);
        }
    });
}

$(document).ready(function() {
    $('#submit-for-summary').click(function() {
        $('#wait-modal').modal('show');
        summarizeText();
    });
    $('#summarize-again').click(function() {
        location.reload();
    })
    $('#animate-load').on('click',function(){
        $(this).toggleClass('clicked');
        $('#principal').fadeIn(2000);
        $('#animate-load').hide(1000);
        $('footer').css('position','inherit');
    });
});
$(function(){
    $('#logo-load').hover(function() {
        $("#logo-load").removeClass("animated");
    });
  });