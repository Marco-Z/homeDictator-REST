$(document).ready(function(){ 
 
  String.prototype.replaceAll = function(search, replacement) {
      var target = this;
      return target.replace(new RegExp(search, 'g'), replacement);
  };

  $('#members').on('click', '#remove', function(){ 
    $(this).closest('.row').remove(); 
  }); 
  $('#tasks').on('click', '#remove', function(){ 
    $(this).closest('.row').remove(); 
  }); 
 
  var n = 2; 
  var m = 1; 
  $('#add_member').on('click', function(){ 
    var el = "<div class='row'>"+ 
    "<span>"+ 
    "<a id='remove' class='btn-floating btn waves-effect waves-light red'><i class='material-icons'>clear</i></a>"+ 
    "</span>"+ 
    "<div class='input-field col s6 offset-s3'>"+ 
    "<input id='member_id' name='member_id' class='member' type='text' class='validate'>"+ 
    "<label for='member_id'>Member Name</label>"+ 
    "</div>"+ 
    "</div>"; 
    el = el.replaceAll('member_id', 'member_name_'+ (++n)); 
    $(el).insertBefore($('#add_member').parent()); 
  }); 

  $('#add_task_entry').on('click', function(){ 
    var el ="<div class='row'>"+
              "<span>"+ 
                "<a id='remove' class='btn-floating btn waves-effect waves-light red'><i class='material-icons'>clear</i></a>"+ 
              "</span>"+ 
              "<div class='input-field col s10 offset-s1 m4 offset-m1'>"+
                "<input id='task_name_mynum' name='task_name_mynum' type='text' class='validate' >"+
                "<label for='task_name_mynum'>Task Name</label>"+
              "</div>"+
              "<div class='input-field col s10 offset-s1 m3'>"+
                "<input id='task_value_mynum' name='task_value_mynum' type='number' class='validate' >"+
                "<label for='task_value_mynum'>Task Value</label>"+
              "</div>"+
              "<div class='input-field col s10 offset-s1 m3'>"+
                "<input id='task_frequency_mynum' name='task_frequency_mynum' type='number' class='validate' >"+
                "<label for='task_frequency_mynum'>Task Frequency</label>"+
              "</div>"+
            "</div>";
    el = el.replaceAll('mynum', ++m); 
    $(el).insertBefore($('#add_task_entry').parent()); 
  }); 
 
}); 