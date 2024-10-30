$(function() {

    function clearClasses() {
      $('.shelf-bottles-moving').removeClass('moving-bottles');
      $('.machine-container').removeClass('grapping-bottle');
      $('.machine-container').removeClass(function (index, css) {
          return (css.match (/(^|\s)grab-bottle[^\s$]+/g) || []).join(' ')+ ' grapping-bottle';
      });
    };
  
    // Activate Coke Bottle
    $('.activator-coke').click(function() {
      clearClasses();
  
      setTimeout(function() {
        $('.machine-container').addClass('grab-bottle-coke grapping-bottle');
        $('.moving-coke').addClass('moving-bottles');
      }, 10);
    });
  
    // Activate Sprite Bottle
    $('.activator-sprite').click(function() {
      clearClasses();
      setTimeout(function() {
        $('.machine-container').addClass('grab-bottle-sprite grapping-bottle');
        $('.moving-sprite').addClass('moving-bottles');
      }, 10);
    });
  
    // Activate Diet Bottle
    $('.activator-diet').click(function() {
      clearClasses();
      setTimeout(function() {
        $('.machine-container').addClass('grab-bottle-diet grapping-bottle');
        $('.moving-diet').addClass('moving-bottles');
      }, 10);
    });
  
    // Activate Dasani Bottle
    $('.activator-dasani').click(function() {
      clearClasses();
      setTimeout(function() {
        $('.machine-container').addClass('grab-bottle-dasani grapping-bottle');
        $('.moving-dasani').addClass('moving-bottles');
      }, 10);
    });
  
    // Open Coke Overlay
    $('.bottle-coke').click(function() {
      clearClasses();
  
  
      $(this).addClass('hide-bottle');
      $('.machine-overlay').addClass('active');
      $('.machine-overlay-coke').addClass('active');
  
      setTimeout(function() {
        $('.machine-overlay').removeClass('active');
        $('.bottle-coke').removeClass('hide-bottle');
        $('.machine-overlay-inner').removeClass('active');
      }, 5000);
       // Linear interpolation helper
  
      // Activates SMIL animation when the bottle is clicked
      // This part is the only way to make the filling animation.
      var cokeFill = document.getElementById('cokeFillAnimation');
      cokeFill.beginElement();
    });
  
    // Open Coke Overlay
    $('.bottle-sprite').click(function() {
      clearClasses();
  
  
      $(this).addClass('hide-bottle');
      $('.machine-overlay').addClass('active');
      $('.machine-overlay-sprite').addClass('active');
  
      setTimeout(function() {
        $('.machine-overlay').removeClass('active');
        $('.bottle-sprite').removeClass('hide-bottle');
        $('.machine-overlay-inner').removeClass('active');
      }, 5000);
  
      // Activates SMIL animation when the bottle is clicked
      // This part is the only way to make the filling animation.
      var spriteFill = document.getElementById('spriteFillAnimation');
      spriteFill.beginElement();
    });
  
    // Open Coke Overlay
    $('.bottle-diet').click(function() {
      clearClasses();
  
  
      $(this).addClass('hide-bottle');
      $('.machine-overlay').addClass('active');
      $('.machine-overlay-diet').addClass('active');
  
      setTimeout(function() {
        $('.machine-overlay').removeClass('active');
        $('.bottle-diet').removeClass('hide-bottle');
        $('.machine-overlay-inner').removeClass('active');
      }, 5000);
  
      // Activates SMIL animation when the bottle is clicked
      // This part is the only way to make the filling animation.
      var dietFill = document.getElementById('dietFillAnimation');
      dietFill.beginElement();
    });
  
    // Open Coke Overlay
    $('.bottle-dasani').click(function() {
      clearClasses();
  
  
      $(this).addClass('hide-bottle');
      $('.machine-overlay').addClass('active');
      $('.machine-overlay-dasani').addClass('active');
  
      setTimeout(function() {
        $('.machine-overlay').removeClass('active');
        $('.bottle-dasani').removeClass('hide-bottle');
        $('.machine-overlay-inner').removeClass('active');
      }, 5000);
  
      // Activates SMIL animation when the bottle is clicked
      // This part is the only way to make the filling animation.
      var dasaniFill = document.getElementById('dasaniFillAnimation');
      dasaniFill.beginElement();
    });
  
  });