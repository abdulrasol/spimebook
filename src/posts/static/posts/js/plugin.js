/*global $, window */
$('document').ready(function () {
    'use strict';

    // 1 registeration form validation
    var password = $('.me-form .me-form-password'),
        alertElement = $('.me-form .uk-alert-warning');
    password.on('keyup focus', function () {

        if ($(this).val().length < 6) {
            $('.me-form button').addClass('uk-disabled');
            alertElement.slideDown(400);
            //alert($(this).val().length);
        }
        else {
            $('.me-form button').removeClass('uk-disabled');
            alertElement.slideUp(400);
        }
        //$('.me-form button').addClass('uk-disabled')
    });

    // love Post 
    $('.reaction #love-post').on('click', function () {
        var btn = $(this);
        var URL = $(this).data('post');
        console.log($(this).data('post'));
        $.get(URL, function (data, state, xhr) {
            console.log(data)
            UIkit.notification({
                message: data.msg,
                status: 'success',
                pos: 'top-right',
                timeout: 3000
            });
            if (data.love == true) {
                btn.css('color', '#e64f4f');
            } else {
                btn.css('color', '#bcdbfb');
            }
        });
    });

    // add or remove readed books
    $('#add-to-readed-book-parent').on('click', '#add-to-readed-book', function () {
        var btn = $(this);
        var URL = $(this).data('book');
        $.get(URL, function (data, state, xhr) {
            //console.log(data)
            UIkit.notification({
                message: data.msg,
                status: 'success',
                pos: 'top-right',
                timeout: 3000
            });
            if (data.readed_book == true) {
                var str = `<li><a id='add-to-readed-book' data-book='${URL}'><span class='uk-margin-small-right' uk-icon='icon: trash'></span>Remove from readed Books</a>`
                btn.hide().parent().append(str)
            } else {
                var str = `<li><a id='add-to-readed-book' data-book='${URL}'><span class='uk-margin-small-right' uk-icon='icon: plus'></span>Add to readed Books</a>`
                //$('.me-context-menu-profile-page').offsetParent().remove();
                btn.hide().parent().append(str);
                console.log(data.msg)
                console.log(data.readed_book)
            }
        });
    });


    // Autocompelete author
    var availableTags = [
        "ActionScript",
        "AppleScript",
        "Asp",
        "BASIC",
        "C",
        "C++",
        "Clojure",
        "COBOL",
        "ColdFusion",
        "Erlang",
        "Fortran",
        "Groovy",
        "Haskell",
        "Java",
        "JavaScript",
        "Lisp",
        "Perl",
        "PHP",
        "Python",
        "Ruby",
        "Scala",
        "Scheme"
    ];

});
