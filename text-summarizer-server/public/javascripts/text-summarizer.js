function drawResults(sentence_data, features_data) {
    google.charts.load("current", {packages:['corechart']});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        console.log(features_data)
        drawChosenSentences(sentence_data);
        drawKeywordFeature(features_data[0]);
        drawTitleWordsFeature(features_data[1]);
        drawSentenceLocationFeature(features_data[2]);
        drawSentenceLengthFeature(features_data[3]);
        drawProperNounFeature(features_data[4]);
        drawNumericalDataFeature(features_data[5]);
        drawBonusPhraseFeature(features_data[6]);
        drawStigmaPhraseFeature(features_data[7]);
    }

    function drawChosenSentences(sentence_data) {
        data_array = [["Sentence", "Rank", { role: "style" } ]];
        for (var i = 0; i<sentence_data.length; i++) {
            data_array.push([sentence_data[i][0], sentence_data[i][1], (sentence_data[i][2] == 0) ? "opacity: 0.2" : "color: #76A7FA"]);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Selected Sentences by Rank",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("chart-div"));
        chart.draw(view, options);
    }

    function drawKeywordFeature(keyword_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<keyword_data.length; i++) {
            data_array.push([i+1, keyword_data[i], '#1abc9c']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Keyword feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("keyword"));
        chart.draw(view, options);
    }

    function drawTitleWordsFeature(title_words_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<title_words_data.length; i++) {
            data_array.push([i+1, title_words_data[i], '#d35400']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Title words feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("title-word"));
        chart.draw(view, options);
    }

    function drawSentenceLocationFeature(sentence_location_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<sentence_location_data.length; i++) {
            data_array.push([i+1, sentence_location_data[i], '#9b59b6']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Sentence location feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("sentence-location"));
        chart.draw(view, options);
    }

    function drawSentenceLengthFeature(sentence_length_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<sentence_length_data.length; i++) {
            data_array.push([i+1, sentence_length_data[i], '#f1c40f']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Sentence length feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("sentence-length"));
        chart.draw(view, options);
    }

    function drawProperNounFeature(proper_noun_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<proper_noun_data.length; i++) {
            data_array.push([i+1, proper_noun_data[i], '#f64747']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Proper noun feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("proper-noun"));
        chart.draw(view, options);
    }

    function drawNumericalDataFeature(numerical_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<numerical_data.length; i++) {
            data_array.push([i+1, numerical_data[i], '#27ae60']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Numerical data feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("numerical-data"));
        chart.draw(view, options);
    }

    function drawBonusPhraseFeature(bonus_phrase_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<bonus_phrase_data.length; i++) {
            data_array.push([i+1, bonus_phrase_data[i], '#E08283']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Bonus phrase feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("bonus-phrase"));
        chart.draw(view, options);
    }

    function drawStigmaPhraseFeature(stigma_phrase_data) {
        data_array = [["Sentence", "Feature score", { role: "style" } ]];
        for (var i = 0; i<stigma_phrase_data.length; i++) {
            data_array.push([i+1, stigma_phrase_data[i], '#81CFE0']);
        }
        var data = google.visualization.arrayToDataTable(data_array);

        var view = new google.visualization.DataView(data);

        var options = {
            title: "Stigma phrase feature score for each sentance",
            width: 700,
            height: 500,
            bar: {groupWidth: "80%"},
            legend: { position: "none" },
            hAxis: {format: "0"},
        };
        var chart = new google.visualization.ColumnChart(document.getElementById("stigma-phrase"));
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
            console.log(data)
            var sentences_data = eval(data[0]);
            var features_data = eval(data[1]);
            var title = data[2];
            var summary = '';
            for (var i=3; i<data.length; i++) {
                summary += data[i];
                summary += ' ';
            }
            $('#summary-title').text(title);
            $('#summary-text').text(summary);
            $('#header').text("Summary results")
            drawResults(sentences_data, features_data);
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