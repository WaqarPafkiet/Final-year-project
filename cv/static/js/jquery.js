$('a#apply_id').bind('click', function() {
    $.getJSON('/apply', {
        job_id: $('input[name="job_id"]').val(),
    }, function(data) {
        $("#result").html(data.result);
        $("#apply_btn").hide();
        if($("#sess").val()){
            $("#eval_btn").show();
        }

    });
    return false;
});

//$('a#eval_id').bind('click', function() {
//    $.getJSON('/applied_jobs', {
//        job_id: $('input[name="job_id"]').val(),
//    }, function(data) {
//        $("#result").html(data.result);
//        $("#eval_btn").hide();
//        //if($("#sess").val()){
//        //    $("#check_status").show();
//        //}
//
//    });
//    return false;
//});