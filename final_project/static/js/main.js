$(".datepicker").datepicker(
{
    autoclose: true,
    disableTouchKeyboard: true,
    endDate: "0d",
    forceParse: true,
    format: "yyyy-mm-dd",
    immediateUpdates: true,
    multidate: false,
    orientation: "left bottom",
    startDate: "2000-01-01",
    templates: {
                    leftArrow: "<i class=\"fas fa-caret-left\"></i>",
                    rightArrow: "<i class=\"fas fa-caret-right\"></i>"
                },
    todayBtn: "linked",
    todayHighlight: true,
    toggleActive: true
});