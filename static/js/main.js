(function ($) {
    "use strict";

    // Dropdown on mouse hover
        $(document).ready(function () {
    var navbarVertical = $('#navbar-vertical');
    var categoryToggle = $('#category-toggle');
    var timeoutId;

    function showNavbar() {
        navbarVertical.collapse('show');
    }

    function hideNavbar() {
        timeoutId = setTimeout(function() {
            navbarVertical.collapse('hide');
        }, 200);  // Přidáme malé zpoždění, aby uživatel měl čas přesunout myš na navbar
    }

    categoryToggle.on('mouseenter', showNavbar);
    categoryToggle.on('mouseleave', hideNavbar);

    navbarVertical.on('mouseenter', function() {
        clearTimeout(timeoutId);
    });

    navbarVertical.on('mouseleave', hideNavbar);

    navbarVertical.on('show.bs.collapse', function () {
        $(this).css('position', 'absolute');
        $(this).css('width', 'calc(100% - 30px)');
        $(this).css('z-index', '999');
    });

    navbarVertical.on('hide.bs.collapse', function () {
        $(this).css('position', '');
        $(this).css('width', '');
        $(this).css('z-index', '');
    });

    // Zavření dropdown menu při kliknutí mimo
    $(document).on('click', function (e) {
        if (!navbarVertical.is(e.target) && navbarVertical.has(e.target).length === 0 && !categoryToggle.is(e.target)) {
            navbarVertical.collapse('hide');
        }
    });
});
    // Tlacitko vlozeni do kosiku
    $(document).ready(function() {
    $('#add-to-cart-form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        var quantity = form.find('input[name="quantity"]').val();

        // Přidáme quantity do URL
        url += (url.indexOf('?') > -1 ? '&' : '?') + 'quantity=' + quantity;

        // Přesměrujeme na upravenou URL
        window.location.href = url;
    });
});


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });

})(jQuery);

