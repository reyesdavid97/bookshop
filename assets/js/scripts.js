(function($) {
  "use strict";

  $("body").scrollspy({
    target: ".fixed-top",
    offset: 60
  });

  $('[data-toggle="tooltip"]').tooltip()

  $("#collapsingNavbar li a").click(function() {
    /* always close responsive nav after click */
    $(".navbar-toggler:visible").click();
  });

  /*lida code for phot popup*/
  $(".col-sm-3 img").click(function() {
    $(".show").fadeIn();
  });

  $("#close-overlay, .overlay").click(function() {
    $(".show").fadeOut();
  });

  $(".tab-panels .tabs li a").on("click", function(event) {
    event.preventDefault();
    $(".tab-panels .tabs li a.active").removeClass("active");
    $(this).addClass("active");

    var showPanel = $(this).attr("rel");

    $(".tab-panels .panel.active").hide(0, function() {
      $("#" + showPanel).show(0, function() {
        $(this).addClass("active");
      });
    });
  });

  $.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
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
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
  });
})(jQuery);