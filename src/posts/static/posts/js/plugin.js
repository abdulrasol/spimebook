/*global $, window */
$('document').ready(function () {
    'use strict';

    // Mobile Nav-bar
    var DOCUMENT = $('window');
    var mobile_navbar = $('#me-mobile-navbar');
    var main_navbar = $('#me-main-navbar')
    $(window).on('scroll', function (event) {
        var sc = $(window).scrollTop();
        if (sc >= 80) {
            mobile_navbar.css({
                position: 'fixed',
                top: '0px',
                left: '0px'
            });
        } else {
            mobile_navbar.css({
                position: 'relative',
                top: '0px'
            });
        }

    });

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

    $('#add-to-readed-book').click(function () {
        var URL = $(this).data('book');
        console.log('URL');
    });

    // add or remove readed books
    $('#add-to-readed-book-parent').on('click', '#add-to-readed-book', function () {
        var btn = $(this);
        var URL = $(this).data('book');
        console.log(URL);
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

    // search book fast
    var URL = $("#book-search-main").data('url');
    //console.log(URL);
    $("#book-search,#book-search-main,#book-search-mobile").autocomplete({
        source: URL,
        minLength: 2,
        select: function (event, ui) {
            //console.log(ui);
            //console.log(ui.item);
            console.log(ui.item.value);
            var book = ui.item.value
            //var get_url = "lab".replace(/12345/, tmp.toString());
            var get_url = URL + '/' + ui.item.value
            console.log(get_url);
            $(location).attr('href', get_url);
        },
    });

});

document.addEventListener('click', event => {

    // love post
    if (event.target.parentNode.id == 'love-post') {
        let btn = event.target.parentNode;
        let URL = event.target.parentNode.dataset.post;
        console.log(URL);
        $.get(URL, function (data, state, xhr) {
            UIkit.notification({
                message: data.msg,
                status: 'success',
                pos: 'top-right',
                timeout: 3000
            });
            if (data.love == true) {
                btn.style.color = "#e64f4f";
                //btn.css('color', '');
            } else {
                btn.style.color = "#bcdbfb";
                //btn.css('color', '#e64f4f');
            }
        });
    }

});
