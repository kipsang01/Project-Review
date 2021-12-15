$(document).ready(function(){
    $('form').submit(function(event){
      event.preventDefault()
      form = $("form")
    $.ajax({
      'url':'/rate/<post_id>',
      'type':'POST',
      'data':form.serialize(),
      'dataType':'json',
      'success': function(data){
        alert(data['success'])
      },
    })// END of Ajax method
    }) // End of submit event
  
  }) // End of document ready function


  $(function() {

    $(".progress").each(function() {
  
      var value = $(this).attr('data-value');
      var left = $(this).find('.progress-left .progress-bar');
      var right = $(this).find('.progress-right .progress-bar');
  
      if (value > 0) {
        if (value <= 5) {
          right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
        } else {
          right.css('transform', 'rotate(180deg)')
          left.css('-webkit-transform', 'rotate(' + percentageToDegrees(value - 5) + 'deg)')
        }
      }
  
    })
  
    function percentageToDegrees(percentage) {
  
      return percentage / 10 * 360
  
    }
  
  });