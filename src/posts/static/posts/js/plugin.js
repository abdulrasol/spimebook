/*global $, window */
/*jshint esversion: 6 */
'esversion: 6';
$('document').ready(function () {
    'use strict';
    // Mobile Nav-bar
    var DOCUMENT = $('window');
    var mobile_navbar = $('#me-mobile-navbar');
    var main_navbar = $('#me-main-navbar');
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
        } else {
            $('.me-form button').removeClass('uk-disabled');
            alertElement.slideUp(400);
        }
        //$('.me-form button').addClass('uk-disabled')
    });

    // search book fast
    var URL = $("#book-search-main").data('url');
    $("#book-search,#book-search-main,#book-search-mobile").autocomplete({
        source: URL,
        minLength: 2,
        select: function (event, ui) {
            //console.log(ui);
            //console.log(ui.item);
            console.log(ui.item.value);
            var book = ui.item.value;
            //var get_url = "lab".replace(/12345/, tmp.toString());
            var get_url = URL + '/' + ui.item.value;
            console.log(get_url);
            $(location).attr('href', get_url);
        },
    });

    // add new genres
    $('#modal-add-genre #add-genre-btn').click(function () {
        $('#spinner').fadeIn();
        let csrftoken = jQuery("#modal-add-genre input[name=csrfmiddlewaretoken]").val();
        let genre_text = $('#modal-add-genre input[name=genre]').val();
        let label = document.createElement("LABEL");
        let ele = document.createElement('INPUT');
        let label_text = document.createTextNode(' ' + genre_text);
        label.setAttribute('for', 'id_archived');
        ele.setAttribute("id", "id_archived");
        ele.setAttribute("type", "checkbox");
        ele.setAttribute("value", genre_text);
        ele.setAttribute("class", "uk-checkbox");
        ele.setAttribute("name", "category");
        label.appendChild(ele);
        label.appendChild(label_text);
        var URL = '/books/ajax/genre/' + genre_text;
        $.post(URL, {
            'name': genre_text,
            csrfmiddlewaretoken: csrftoken
        },
            function (data, textStatus, jqXHR) {
                console.log(data.state);
                if (textStatus === 'success') {
                    var genre_container = document.querySelector('#genre-container');
                    genre_container.appendChild(label);
                    UIkit.modal('#modal-add-genre').hide();
                    $('#spinner').fadeOut();
                    $('#modal-add-genre input[name=genre]').val('');
                } else {
                    UIkit.notification({
                        message: 'Check your connections',
                        status: 'warning',
                        pos: 'top-right',
                        timeout: 3000
                    });
                }
            }
        );
    });
    // add new coomment
    $('.add-comment').click(function (e) {
        e.preventDefault();
        let comment_btn = $(this);
        let spinner = comment_btn.next();
        var comment = comment_btn.parents('.uk-card-footer').find('#comment input');
        URL = comment_btn.parents('form').attr('action');
        let csrftoken = jQuery("#comment-form input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            url: URL,
            data: {
                'comment': comment.val(),
                'csrfmiddlewaretoken': csrftoken,
                'id': comment_btn.data('post')
            },
            success: function (data, textStatus, jqXHR) {
                var elemet = `
                            <article class="uk-comment uk-padding-small uk-padding-remove-horizontal">
                                <hr>
                                <header class="uk-comment-header uk-grid-medium uk-flex-middle" uk-grid>
                                    <div class="uk-width-auto">
                                        <a class="uk-link-reset" href="/${data.content.user}/">
                                            <img class="uk-comment-avatar uk-border-circle avatat-img"
                                                src="${data.content.img}" alt="${data.content.user}"
                                                width="30" height="30" alt="">
                                        </a>
                                    </div>
                                    <div class="uk-width-expand">
                                        <h4 class="uk-comment-title uk-margin-remove">
                                            <a class="uk-link-reset" href="/${data.content.user}/">
                                            ${data.content.user}
                                            </a>
                                        </h4>
                                        <ul class="uk-comment-meta uk-subnav uk-subnav-divider uk-margin-remove-top">
                                            <li>${data.content.time}</li>
                                        </ul>
                                    </div>
                                </header>
                                <div class="uk-comment-body">
                                    <p>${data.content.comment}</p>
                                </div>
                            </article>
                            `;
                var comment_container = comment_btn.parents('.uk-card-footer').find('.commnet-container');
                comment_container.append(elemet);
                UIkit.notification({
                    message: 'Your Comment added!',
                    status: 'success',
                    pos: 'top-right',
                    timeout: 3000
                });
            },
            error: function (data, textStatus, jqXHR) {
                UIkit.notification({
                    message: 'Check your connections',
                    status: 'warning',
                    pos: 'top-right',
                    timeout: 3000
                });
            },
            beforeSend: function () {
                spinner.show();
            },
            complete: function () {
                spinner.hide();
                comment.val('');
            }
        });
    });
});

document.addEventListener('click', event => {

    // love post
    if (event.target.parentNode.id == 'love-post') {
        let btn = event.target.parentNode;
        let URL = event.target.parentNode.dataset.post;
        $.get(URL, function (data, state, xhr) {
            UIkit.notification({
                message: data.msg,
                status: 'success',
                pos: 'top-right',
                timeout: 3000
            });
            if (data.love == true) {
                //btn.firstChild.firstChild.style.fill = '#e64f4f';
                btn.style.color = "#e64f4f";
                //btn.css('color', '');
                //console.log(btn.firstChild.style.fill);
            } else {
                //btn.firstChild.firstChild.style.fill = 'bcdbfb';
                btn.style.color = "#bcdbfb";
                //console.log(btn.firstChild.firstChild.style.fill);
                //btn.css('color', '#e64f4f');
            }
        });
    }

    // Add to readed Books
    if (event.target.id == 'add-to-readed-book') {
        let book = event.target,
            URL = book.dataset.book;
        let item = document.createElement("a");
        item.dataset.book = URL;
        item.id = 'add-to-readed-book';
        let sp = document.createElement('span');
        sp.classList.add("uk-margin-small-right");
        $.get(URL, function (data) {
            UIkit.notification({
                message: data.msg,
                status: 'success',
                pos: 'top-right',
                timeout: 3000
            });
            var node = document.createTextNode("Remove from readed Books");
            if (data.readed_book == true) {
                node = document.createTextNode("Remove from readed Books");
                sp.setAttribute('uk-icon', 'icon: trash');
                item.appendChild(sp);
                item.appendChild(node);
                book.parentNode.appendChild(item);
                book.remove();
            } else {
                node = document.createTextNode("Add to readed Books");
                sp.setAttribute('uk-icon', 'icon: plus');
                item.appendChild(sp);
                item.appendChild(node);
                book.parentNode.appendChild(item);
                book.remove();
            }
        });
    }

    //rating books
    if (event.target.classList.contains('book-rating')) {
        rate = event.target;
        URL = '/books/ajax/book/rate/' + rate.parentNode.dataset.book + '/' + rate.value;
        //console.log(URL);
        $.get(URL, function (data, state, xhr) {
            console.log(data.rating.rating__avg);
            document.querySelector('.show-rating').innerHTML = data.rating.rating__avg;
            document.querySelector('.ratings-num').innerHTML = data.ratings_num;
        });
    }

});