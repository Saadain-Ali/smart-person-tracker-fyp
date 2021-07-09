$(document).ready(function () {
    console.log('surv.js loaded ');
    
    var trigger = $('.hamburger'),
      overlay = $('.overlay'),
      isClosed = false;

    trigger.click(function () {
      hamburger_cross();
    });

    
    function hamburger_cross() {

      if (isClosed == true) {
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        $('.ham-arrow').removeClass('fa fa-chevron-left')
        $('.ham-arrow').addClass('fa fa-chevron-right')
        isClosed = false;
      } else {
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        $('.ham-arrow').removeClass('fa-chevron-right')
        $('.ham-arrow').addClass('fa-chevron-left')
        isClosed = true;
      }
    }

    $('[data-toggle="offcanvas"]').click(function () {
      $('#wrapper').toggleClass('toggled');
    });


    // show setting sidebar
    // document.getElementById("a").onclick = function (e) {
      $('#page a').click(function (e) {
        
     
        e.preventDefault();
        console.log('event')
        console.log(e)
        var isInit = true; // indicates if the popup already been initialized.
        var isClosed = false; // indicates the state of the popup
        document.getElementById("popup").style.display = "block";
        // $("#popup").addClass("col-lg-6 col-md-6 col-12");
    
        document.getElementById('cams').className = "";
        // $("#cams").addClass("col-6");
        var id = $(this).data("id")
        var url = $(this).data("url").toString();
        url = url.split('/video')[0]
        url = url + '/settings_window.html'
        console.log("url uis here " + url)
        document.getElementById('iframe').src = url //'http://192.168.0.80:8080/settings_window.html';
    
        // document.getElementById('wrapper').onclick = function () {
        document.getElementById('popup').onclick = function () {
          if (isInit) { isInit = false; return; }
          if (isClosed) { return; } //if the popup is closed, do nothing.
          document.getElementById("popup").style.display = "none";
    
        //   document.getElementById('cams').className = "";
        //   document.getElementById('cams').className = "col-12";
          isClosed = true;
        }
        return false;
      })


    // collabsible header camera
    $( ".card-header" ).on({
        click: function(e) {
          console.log(e.target.id)
          var id = e.target.id
          $('.card-body-' + id).slideToggle('slow');
        }
      });

    $('.bg').on({ 
      load: function (e) {
        // console.log(this)
        var id = $(this).data("id").toString();
        id = '.spinner-' + id
        // console.log('image id  is ' + id)
        $(id).fadeOut(500);
      }
    });


  });

  