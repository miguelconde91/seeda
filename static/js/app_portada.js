function mouseFuera(id) {
    $(id).removeClass("app-icono-hover", 200);
}

$(document).ready(function () {
    var toolTipDef = {
        position: {
            my: "center",
            at: "bottom+65"
        }
    };

    $(".app-icono").hover(function () {
        $(this).toggleClass("app-icono-hover", 200);
    }).tooltip(toolTipDef);

});