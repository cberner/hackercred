$(document).ready(function() {
	function hideModal(modal, duration) {
		modal.hide(duration);
		var launcher = $("#launch-" + modal.attr('id'));
		launcher.show();
		return false
	}
	function hideModals(modals, duration) {
		modals.each(function(index, modal) {
			hideModal($(modal), duration);
		});
		return false;
	}
	
	$("body").bind("click", function(e) {
		$('a.menu').parent("li").removeClass("open");
		//Don't hide the modal(s), if this click is inside a modal
		if ($(e.target).parents("div.modal").length == 0) {
			hideModals($('div.modal'));
		}
	});

	$("a.menu").click(function(e) {
		var $li = $(this).parent("li").toggleClass('open');
		return false;
	});
	
	//Make modals closable, and show their launcher again
	$("a.close").click(function(e) {
		var p = $(this).parents("div.modal");
		hideModal(p, 200);
	});
	
	$("a.delete").click(function(e) {
		url = $(this).attr('href');
		url = url.substring(1, url.length);
		var p = $(this).parents('.deleteable');
		p.hide();
		$.post(url);
	});
	
	$("div.modal input.btn").submit(function(e) {
		var p = $(this).parents("div.modal");
		hideModal(p, 200);
		return false;
	});
	
	$("div.modal a.btn").click(function(e) {
		var p = $(this).parents("div.modal");
		hideModal(p, 200);
		return false;
	});
	
	//Make launchers launch their modal
	$("a.launcher").click(function(e) {
		var myid = $(this).attr('id');
		$("#" + myid.replace("launch-", "")).show(200);
		if ($(this).hasClass('hideable')) {
			$(this).hide();
		}
		return false
	});
});

//Enable csrf for ajax
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});



