$(document).ready(function () {
    $('.like').click(function () {
        var target = event.target
        var item_pk = $(target).attr('data-id')

        if (item_pk) {
            $.ajax({
                url: "/posts/likes/" + item_pk + "/",
                success: function (data) {
                    if (data.is_like) {
                        var class_heart = "fas fa-heart"
                    } else {
                        class_heart = "far fa-heart"
                    }

                    var like_qnt = data.likes
                    var like_html = '<i class="' + class_heart + '" data-id="' + item_pk + '"></i> <span>' + like_qnt.toString() + '</span>'
                    var selector = '#' + item_pk

                    $(selector).html(like_html)
                }
            })
        }
    })
})


