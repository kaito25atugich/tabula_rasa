$(function(){
  // どなるどマクドナルド
  $('.hum').click(function(){
     $('.nav').toggleClass('open');
   });
   if ($('.nav').length){
     $('a').click(function(){
       $('.nav').removeClass('open');
     });
   }
   $(window).scroll(function(){
     if($(this).scrollTop() > 20){
       $('header').slideUp();
       $('.hum').slideUp();
     } else {
       $('header').slideDown();
       $('.hum').slideDown();
     }
   });
  // modal実装しなかった
  // $('.comment-reply').on('click', function(){
  //   $('.modal-reply-wrap').removeClass('disp');
  //   $('.overLay').addClass('is-open');
  // });
  // $('.close-button').on('click', function(){
  //   $('.modal-reply-wrap').addClass('disp');
  //   $('.overLay').removeClass('is-open');
  // });
  // $('.overLay').on('click', function(){
  //   $('.modal-reply-wrap').addClass('disp');
  //   $('.overLay').removeClass('is-open');
  // });
  // $('.comment-reply').on('click', 'a', function(){
  //   var ind = $(this).data('ind');
  //   $('.modal-reply').data('ind2') = ind;
  // });
});
