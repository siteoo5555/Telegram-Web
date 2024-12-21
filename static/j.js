const { useState } = require("react");

$(document).ready(function(){

$(".trigger").click(function(){
    $(".overlay, .menuWrap").fadeIn(180);
            $(".menu").animate({opacity: '1', left: '0px'}, 180);
});
    

    $(".settings").click(function(){
            $(".config").animate({opacity: '1', right: '0px'}, 180);
        /* hide others */
            $(".menuWrap").fadeOut(180);
            $(".menu").animate({opacity: '0', left: '-320px'}, 180);
});


    $(".deskNotif").click(function(){
    $(".showSName, .showPreview, .playSounds").toggle();
});


    $(".overlay").click(function () {
            $(".overlay, .menuWrap").fadeOut(180);
    $(".menu").animate({opacity: '0', left: '-320px'}, 180);
            $(".config").animate({opacity: '0', right: '-200vw'}, 180);
});
    

    $(document).keydown(function(e) {
         if (e.keyCode == 27) {
            $(".overlay, .menuWrap").fadeOut(180);
    $(".menu").animate({opacity: '0', left: '-320px'}, 180);
            $(".config").animate({opacity: '0', right: '-200vw'}, 180);
        }
});


$(".DarkThemeTrigger").click(function(){
    $("body").toggleClass("DarkTheme")
}); 	


$(".otherOptions").click(function(){
    $(".moreMenu").slideToggle("fast");
});


$( ".search" ).click(function() {
    $( ".searchChats" ).focus();
});


$(".emoji").click(function(){
    $(".emojiBar").fadeToggle(120);
});
$(".convHistory, .replyMessage").click(function(){
    $(".emojiBar").fadeOut(120);
});
});