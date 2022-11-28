function authjs(callback=function(un){},permissions=['username'],returnerror=true){
	data = undefined;
	var authwindow = window.open(`https://authjs.greatusername.repl.co/auth?un={{un}}&p=${encodeURIComponent(JSON.stringify(permissions))}&url=${window.location.hostname}`,'auth-window','modal =yes, toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width='+screen.width / 2+', height='+screen.height / 2+', top='+(screen.height / 2) / 2+', left='+(screen.width / 2) / 2);
	ret = false;
	done = function(data){
		if (!ret){
		callback(data);
			ret = true;
		}
	}
	if (returnerror){
	authwindow.addEventListener("beforeunload", function (e) {
		if (!ret){
  callback({'status':false,'error':'Window Closed.'}); 
			ret = true;
		}
});
	}
	return callback;
}