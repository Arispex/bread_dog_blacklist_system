
// router
$(window).on("load", function() {
    let content = $("#content")
    let path = window.location.pathname;
    $("#footer").load("/copyright/");
    if (path == "/user/panel/")
    {
        // user
        content.load("/user/panel/content/")
    }
    else if (path == "/user/all-bans/")
    {
        content.load("/user/all-bans/content/")
    }
    else if (path == "/user/my-bans/")
    {
        content.load("/user/my-bans/content/")
    }
    else if (path == "/user/add-ban/")
    {
        content.load("/user/add-ban/content/")
    }
})
let nav = new mdui.Drawer("#drawer");
$("#menu").on("click", function () {
    nav.toggle();
})

let account_menu = new mdui.Menu("#account-btn", "#account-menu")
$("#account-btn").on("click", function () {
    account_menu.open()
})
$("#logout-btn").on("click", function () {
    $.ajax("/logout/", {
        type: "POST",
        success: function () {
            location.assign("/login/")
        }
    })
})
$("#copy-token").on("click", function () {
    $.ajax("/user/info/", {
        type: "GET",
        success: function (data) {
            let result = JSON.parse(data)
            if (result["status"] === 200){
                navigator.clipboard.writeText(result["data"]["key"]).then(
                function () {
                    mdui.snackbar({
                        message: "复制成功"
                    })
                },
                function (err) {
                    mdui.snackbar({
                        message: err
                    })
                }
            )
            }
        }
    })
})