$(".delete-btn").on("click", function () {
    let qq = $(this).parent().prev().prev().prev().text();
    let tr = $(this).parent().parent();
    $.ajax("/blacklist/", {
        type: "DELETE",
        data: {
            QQ: qq
        },
        success: function (data) {
            let result = JSON.parse(data);
            if (result["status"] === 200)
            {
                tr.remove();
                mdui.snackbar({
                    message: "删除成功"
                });
            }
            else
            {
            mdui.snackbar({
                message: result["msg"]
            });
            }
        }
    })
})