(function($){

     $(document).ready(function() {
        $('.show-price').hover(function() {
                $(this).find("em").animate({opacity: "show"}, "slow");
        }, function() {
                $(this).find("em").animate({opacity: "hide"}, "fast");
        })

    });



})(django.jQuery);