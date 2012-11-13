function validateEmail(email) { 
	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(email);
}

function validatePhone(elementValue){  
	var phoneNumberPattern = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/;  
	if( phoneNumberPattern.test(elementValue)){
		return elementValue.replace(/[^0-9]/g, ''); 
	}else {return false;}
}

$(document).ready(function(){
	$("#deps").change(function(){
		$("#submit").removeAttr("disabled");
		department = $("#deps option:selected").attr("value");
		$.post("formselects.php", {department: department, dataType:"json"}, function(courses){
			var coursearray = $.parseJSON(courses);
			$("#courses").find("option").remove().end().append('<option value="0">Course</option>').val("0");
			for (var i = 0; i < coursearray.length; i++){
				var details = coursearray[i].split(":");
				var app = "<option value=\"" + details[0] + "\">" + details[1] + "</option>"
				$("#courses").append(app);	
			}
		});
	});

	$("#courses").change(function(){
		$("#submit").removeAttr("disabled");
		var department = $("#deps option:selected").attr("value");
		//console.log(department);
		var course = $("#courses option:selected").attr("value");
		var sec = $("#sects option:selected").attr("value");
		$.post("formselects.php", {department: department, course:course, dataType:"json"}, function(courses){
			var coursearray = $.parseJSON(courses);
			$("#sects").find("option").remove().end().append('<option value="0">Section</option>').val("0");
			for (var i = 0; i < coursearray.length; i++){
				if (course != 0){
					var details = coursearray[i].split(":");
					var app = "<option value=\"" + details[0] + "\">" + details[1] + "</option>";
					$("#sects").append(app);
				} 
			}
		});
	});

	$("#alert").submit(function(form){
		$("#submit").attr("disabled", "disabled");
		form.preventDefault();
		
		var department = $("#deps option:selected").attr("value");
		var course = $("#courses option:selected").attr("value");
		var sec = $("#sects option:selected").attr("value");
		var email = $("#email").val();
		var phone = $("#phone").val();
		phone = validatePhone(phone);
		console.log(phone);
		$(".alert").remove().end();
		if (!validateEmail(email)){
			$("#submit").removeAttr("disabled");
			$("#email").after("<div class=\"alert\">" +
				"Please enter a valid email address</div>");
		} else if (!phone){
			$("#submit").removeAttr("disabled");
			$("#phone").after("<div class=\"alert\">Please enter a valid ten-digit phone number</div>");
		} else {
			var user = 0;
			$.post("submit.php", {email: email, phone: phone}, function(ret){
				console.log(ret);
				user = parseInt(ret);
				console.log(user);
				if (sec != 0 && user) {
					console.log("sect:" + sec);
					$.post("submit.php", {department: department, course: course, section: sec, user:user}, function(retval){
						console.log(retval);
						if (retval == 0){
							console.log("lol");
							$("#submit").after("<div class=\"alert alert-success\">Alert created</div>");
							//Alert was created. Handle
						}
					});
				} else {
					//Alert wasn't created
					$("#submit").after("<div class=\"alert alert-error\">Something went wrong!</div>");
					$("#submit").removeAttr("disabled");
				}

			});
		}
	});
});

console.log("test2");

