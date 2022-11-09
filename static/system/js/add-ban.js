$("#submit").on("click", function() {
    let QQ = $("#QQ").val();
    let reason = $("#reason").val();

    if (QQ === "" || reason === "") {
        mdui.snackbar({
            message: "请填写完整信息",
        });
    }
    else {
        $.ajax("/blacklist/", {
            type: "POST",
            data: {
                QQ: QQ,
                reason: reason,
            },
            success: function(data) {
                let result = JSON.parse(data);
                if (result["status"] === 200)
                {
                    mdui.snackbar({
                        message: "添加成功",
                    });
                    $("#QQ").val("")
                    $("#reason").val("")
                }
                else {
                    mdui.snackbar({
                        message: result["msg"],
                    });
                }
            }
        });
    }
});