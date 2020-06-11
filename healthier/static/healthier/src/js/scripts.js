(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

})(jQuery);

function redirect() {
  var referrer = document.referrer;
  location.replace(referrer);
  alert("Ce site requiert votre acceptation pour pouvoir fonctionner correctement. Nous allons vous rediriger vers la page précédente, Merci.");
}
$('#ModalScrollable').modal('show');

// function to retrieve CSRF Token
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');
//define AJAX request header
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});
//used to post a save request
$(".save").click(function(event)
        {
        event.preventDefault();
        $(".modal-error-title").remove();
        //sending request to server to save the requested food item,
        //toggles a modal if answre is false or server error.
        $.ajax(
            {
            url: document.location.pathname,
            data: {"value": event.target.attributes.value.value},
            type: 'POST',
            success: function(response) 
                {
                var answer_obj = JSON.parse(response)
                if (answer_obj.status == false && answer_obj.result == "already existing")
                    {              
                    $("#save-modal-header").append('<h5 class="modal-title modal-error-title" id="save-modal-title">Cet Aliment existe déjà dans vos favoris !</h5>');
                    $("#save-modal").modal('show');
                    }
                else if (answer_obj.status == false && answer_obj.result == "unforeseen exception")
                    {
                    $("#save-modal-header").append('<h5 class="modal-title modal-error-title" id="save-modal-title">Aliment non sauvegardé : une erreur inatendue s"est produite.</h5>');
                    $("#save-modal").modal('show');
                    }
                else if (answer_obj.status == true)
                    {
                    $("#save-modal-header").append('<h5 class="modal-title modal-error-title" id="save-modal-title">Aliment sauvegardé dans vos favoris.</h5>');
                    $("#save-modal").modal('show');
                    }
                
                },
            error: function(error) 
                {
                $("#save-modal-header").append('<h5 class="modal-title modal-error-title" id="save-modal-title">"La requette a échouée, veuillez vérifier votre connexion"</h5>');
                $("#save-modal").modal('show');
                }
            });

    });