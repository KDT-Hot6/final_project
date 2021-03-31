$(function(){
	$("#submit_btn").click(function(){
		callAjax();
	});
});

function callAjax(){
	$.ajax({
		type : "get",
		url : "/wb_web/AnswerController",
		data : {
			'ans_index' : $("#ans_index").val(),
			'answer' : $("#answer").val()
		},
		dataType: 'json',
		success : function(res){
			alert(res.res);
//			alert(res.result);
//			console.log(res);
		}
	});	
}