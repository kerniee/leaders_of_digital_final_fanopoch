var url_string = window.location.href;
var url = new URL(url_string);
var c = url.searchParams.get("uncl");
if (c === '1') {
    $("#navbarSupportedContent").addClass("show");
}
