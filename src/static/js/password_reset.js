$(function () {
    var send = $('form .find'),
        check = $('form .check'),
        reset = $('form .next');
    csrf = jQuery("form input[name=csrfmiddlewaretoken]").val();
    $('.collapse').click(function (event) {
        $(this).parent().find('.according').slideToggle('slow');
    });
    send.click(function (e) {
        URL = $(this).data('url');
        $.ajax({
            type: "POST",
            url: URL,
            data: {
                'email': $('form input[name=email]').val(),
                'csrfmiddlewaretoken': csrf,
            },
            success: function (data) {
                if (data.content.state) {
                    send.parents('.according-parent').find('.according').slideUp('slow');
                    send.parents('.according-parent').next().removeClass('uk-disabled').find('.according').slideDown('slow');
                } else {
                    send.parents('.according-parent').find('.message').parent().fadeIn();
                }
            }
        });
    });
    check.click(function (e) {
        URL = $(this).data('url');
        console.log(URL);
        $.ajax({
            type: "POST",
            url: URL,
            data: {
                'token': $('form input[id=token]').val(),
                'email': $('form input[name=email]').val(),
                'csrfmiddlewaretoken': csrf,
            },
            success: function (data) {
                if (data.content.state) {
                    check.parents('.according-parent').find('.according').slideUp('slow');
                    check.parents('.according-parent').next().removeClass('uk-disabled').find('.according').slideDown('slow');
                    check.parents('.according-parent').find('.message').fadeOut();
                } else {
                    check.parents('.according-parent').find('.message').parent().fadeIn();
                }
            }
        });
    });
    reset.click(function (e) {
        URL = $(this).data('url');
        $.ajax({
            type: "POST",
            url: URL,
            data: {
                'token': $('form input[id=token]').val(),
                'email': $('form input[name=email]').val(),
                'password': $('form input[name=password]').val(),
                'csrfmiddlewaretoken': csrf,
            },
            success: function (data) {
                if (data.content.state) {
                    window.location.replace('/user/login');
                } else {
                    UIkit.notification({
                        message: data.content.msg,
                        status: 'warning',
                        pos: 'top-right',
                        timeout: 3000
                    });
                }
            }
        });
    });
    /*
 

    */
});