$(function() {

  // bind vim keys to page scroll
  $(document).bind('keypress', function (e) {
    switch (e.keyCode) {
      case 106:
        window.scrollBy(0, 100);
        break;
      case 107:
        window.scrollBy(0, -100);
        break;
      case 72:
        window.scrollTo(0, 0);
        break;
      case 4:
        window.scrollBy(0, screen.height - 10);
        break;
      case 21:
        window.scrollBy(0, -(screen.height - 10));
        break;
    }
  });

});