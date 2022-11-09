$("#submit").on("click", function (e) {
    e.preventDefault()
    let username = $("#username").val()
    let password = $("#password").val()
    $.ajax("/login/", {
        type: "POST",
        data: {
            username: username,
            password: password
        },
        success: function (data) {
            let result = JSON.parse(data)
            if (result["status"] === 200)
            {
                location.assign("/user/panel/")
            }
            else {
                mdui.dialog({
                    title: "登入失败",
                    content: result["msg"],
                    buttons: [
                        {
                            text: "返回"
                        }
                    ]
                })
            }
        }
    })
})
$("#footer").load("/copyright/")