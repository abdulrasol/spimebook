/* global $, window */
/* jshint esversion: 6 */
$('document').ready(function () {
    'use strict';
    // Mobile Nav-bar
    var DOCUMENT = $('window');
    var mobile_navbar = $('#me-mobile-navbar');
    $(window).on('scroll', function (event) {
        var sc = $(window).scrollTop();
        if (sc >= 80) {
            mobile_navbar.addClass('fixed-mobile-bar');
        } else {
            mobile_navbar.removeClass('fixed-mobile-bar');
        }
    });
    // 1 registeration form validation
    var password = $('.me-form .me-form-password'),
        alertElement = $('.me-form .uk-alert-warning');
    password.on('keyup focus', function () {
        if ($(this).val().length < 6) {
            $('.me-form button').addClass('uk-disabled');
            alertElement.slideDown(400);
        } else {
            $('.me-form button').removeClass('uk-disabled');
            alertElement.slideUp(400);
        }
    });

    // search book fast
    var URL = $("#book-search-main").data('url');
    $("#book-search,#book-search-main,#book-search-mobile").autocomplete({
        source: URL,
        minLength: 2,
        select: function (event, ui) {
            console.log(ui.item.value);
            var book = ui.item.value;
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
        var URL = '/books/ajax/genre/' + genre_text;
        $.ajax({
            type: "POST",
            url: URL,
            data: {
                'name': genre_text,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data, textStatus, jqXHR) {
                console.log(data.content);
                let label = document.createElement("LABEL");
                let ele = document.createElement('INPUT');
                let label_text = document.createTextNode(' ' + genre_text);
                label.setAttribute('for', 'id_archived');
                ele.setAttribute("id", "id_archived");
                ele.setAttribute("type", "checkbox");
                ele.setAttribute("value", data.content.genre); //
                ele.setAttribute("class", "uk-checkbox");
                ele.setAttribute("name", "category");
                ele.setAttribute("checked", "true");
                label.appendChild(ele);
                label.appendChild(label_text);
                var genre_container = document.querySelector('#genre-container');
                genre_container.appendChild(label);
                UIkit.modal('#modal-add-genre').hide();
                $('#spinner').fadeOut();
                $('#modal-add-genre input[name=genre]').val('');
            },
            error: function (data, textStatus, jqXHR) {
                console.log(data.content);
                UIkit.notification({
                    message: 'Check your connections',
                    status: 'warning',
                    pos: 'top-right',
                    timeout: 3000
                });
            },
        });
    });

    // add new coomment
    $('.add-comment').click(function (e) {
        e.preventDefault();
        let comment_btn = $(this);
        let spinner = comment_btn.next();
        var comment = comment_btn.parents('.uk-card-footer').find('#comment input');
        URL = comment_btn.parents('form').attr('action');
        var post_type = comment_btn.data('type');
        let csrftoken = jQuery("#comment-form input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            url: URL,
            data: {
                'post_type': post_type,
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

    // add new post for books
    let post_on_book = $('#new-post-on-book');
    post_on_book.click(function () {
        var spinner = $('#spinner-post');
        var csrftoken = jQuery("#post-form input[name=csrfmiddlewaretoken]").val();
        var content = jQuery("#post-form textarea[name=content]").val();
        var type = $("#post-form input[name='type']:checked").val();
        let URL = $(this).data('url');
        let post_type = $(this).data('type');
        let data = {};
        if (post_type === 'bookpost') {
            data = {
                'csrfmiddlewaretoken': csrftoken,
                'content': content,
                'p_type': type,
                'type': post_type
            };
        } else {
            data = {
                'csrfmiddlewaretoken': csrftoken,
                'content': content,
                'p_type': 'P',
                'book': $('#post-form input[name="book"]:checked').val(),
                'title': $('#post-form input[name=title]').val(),
                'type': post_type
            };
        }
        $.ajax({
            type: "POST",
            url: URL,
            data: data,
            success: function (data) {
                if (data.content.type === 'post') {
                    window.location.replace(`/posts/post/${data.content.id}/`);
                } else {
                    window.location.replace(`/books/${spinner.data('book')}/`);
                }
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
            }
        });
    });

    // love post
    $('#love-post').click(function (e) {
        e.preventDefault();
        let counter = $(this).parents('.reaction-container').find('.love-count');

    });

});
document.addEventListener('click', event => {

    // love post
    if (event.target.parentNode.id == 'love-post') {
        let btn = event.target.parentNode;
        let URL = event.target.parentNode.dataset.post;
        let post_type = event.target.parentNode.dataset.type;
        $.ajax({
            type: "GET",
            url: URL,
            data: {
                'type': post_type,
            },
            success: function (data) {
                UIkit.notification({
                    message: data.content.msg,
                    status: 'success',
                    pos: 'top-right',
                    timeout: 3000
                });
                if (data.love == true) {
                    btn.style.color = "#e64f4f";

                } else {
                    btn.style.color = "#bcdbfb";
                }
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
        $.get(URL, function (data, state, xhr) {
            console.log(data.rating.rating__avg);
            document.querySelector('.show-rating').innerHTML = data.rating.rating__avg;
            document.querySelector('.ratings-num').innerHTML = data.ratings_num;
        });
    }
});