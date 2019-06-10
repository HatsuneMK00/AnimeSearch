function directToLogIn() {
    window.location.href = '/login'
}

function directToSignUp() {
        window.location.href='/signUp';
    }

function Values(e) {
    $('#m_name').val($(e).attr('id'))
}

function add_watch(index) {
    console.log(index);
    var a_index = "div#anime" + index;
    var name = $(a_index).text();
    var url = "http://127.0.0.1:5000/addAnimeToWatch/" + name;
    // console.log(url);
    $.get(
        url,
        function (data) {
            if (data == "not login yet") {
                window.location.href = '/login';
            }
            else if (data == "success") {
                window.alert("添加成功");
            } else if (data == "duplicated") {
                window.alert("已经添加过啦")
            }
        }
    )
}

function remove_watch(index) {
    console.log(index);
    var a_index = "div#anime" + index;
    var name = $(a_index).text();
    var url = "http://127.0.0.1:5000/removeAnimeFromWatch/" + name;
    // console.log(url);
    $.get(
        url,
        function (data) {
            if (data == "success") {
                window.location.reload();
            }
            else{
                console.log("something goes wrong")
            }
        }
    )
}

function modify_anime(e) {
    var a_index = "div#anime" + $(e).attr('id');
    var name = $(a_index).text();
    var url = "http://127.0.0.1:5000/modifyAnime/" + name;
    // console.log(url);
    window.location.href = url;
}

function callAPI(e) {
    var name = $('#m_name').val();
    name = name.replace('&', '^');
    var tag = $('#m_tag').val();
    console.log(name);
    console.log(tag);
    $.get(
        "http://127.0.0.1:5000/addTag",
        {
            tag: tag,
            name: name
        },
        function () {
            window.location.href = "http://127.0.0.1:5000/anime/" + name;
        }
    );
    $('#todoke').modal('hide');
}

$(function () {
    $('[data-toggle="popover"]').popover()
})
