$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 50,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});