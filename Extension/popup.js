function transfer(){	
	var tablink;
	chrome.tabs.getSelected(null,function(tab) {

	var xhr=new XMLHttpRequest();
	//alert("hii");
	//var tablink='';	
	//var safe = document.URL;
	params=document.getElementById('enteredURL').value;
	alert(params);
	var markup = "url="+tablink+"&html="+document.documentElement.innerHTML;
	xhr.open("POST","http://localhost/predict", true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.send(params);
	$.post( "/predict", {
    javascript_data: params 
	});
	alert(xhr.responseText);
	$("#result").text(xhr.responseText);	
	return xhr.responseText;
	/*if(xhr.responseText==6)
	{
		return "safe";
	}
	return "nooooo";*/
	});
}

$(function() {
    $('button').click(function() {
    	waiting = 'Loading, please wait...',
    	$("#loading").text(waiting);
        $.ajax({
        	waiting: 'Loading, please wait...',
            url: 'http://127.0.0.1:8000/predict2',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
            	var obj = JSON.parse(response);
                console.log(obj.res);
                $("#loading").text('');
                $("#result").text(obj.res);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

//$(document).ready(function(){
//    $("#bts").click(function(){	
//	var val = transfer();
//        });
//});
