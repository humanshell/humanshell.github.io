$(function() {

  // dark mode toggle: stored choice overrides system preference
  function currentTheme() {
    var stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function syncToggleIcon() {
    $('#theme-toggle i')
      .toggleClass('fa-moon-o', currentTheme() === 'light')
      .toggleClass('fa-sun-o', currentTheme() === 'dark');
  }

  $('#theme-toggle').on('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    document.documentElement.setAttribute('data-theme', next);
    syncToggleIcon();
  });

  syncToggleIcon();

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