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

    // Add to readed Books
    if (event.target.id == 'add-to-readed-book') {
        let book = event.target, URL = book.dataset.book;
        let item = document.createElement("a"); item.dataset.book = URL; item.id = 'add-to-readed-book';
        let sp = document.createElement('span'); sp.classList.add("uk-margin-small-right");
        $.get(URL, function (data, state, xhr) {
            UIkit.notification({
                message: data.msg,
                status: 'success',
                pos: 'top-right',
                timeout: 3000
            });
            if (data.readed_book == true) {
                var node = document.createTextNode("Remove from readed Books");
                sp.setAttribute('uk-icon', 'icon: trash');
                item.appendChild(sp); item.appendChild(node);
                book.parentNode.appendChild(item); book.remove();
            } else {
                var node = document.createTextNode("Add to readed Books");
                sp.setAttribute('uk-icon', 'icon: plus');
                item.appendChild(sp);
                item.appendChild(node);
                book.parentNode.appendChild(item); book.remove();
            }
        });
    }

    //rating books
    if (event.target.classList.contains('book-rating')) {
        rate = event.target;
        'http://127.0.0.1:8000/ajax/book/rate/1/9'
        URL = '/ajax/book/rate/' + rate.parentNode.dataset.book + '/' + rate.value;
        //console.log(URL);
        $.get(URL, function (data, state, xhr) {
            console.log(data.rating.rating__avg);
            document.querySelector('.show-rating').innerHTML = data.rating.rating__avg;
            document.querySelector('.ratings-num').innerHTML = data.ratings_num;
        })
    }
});
